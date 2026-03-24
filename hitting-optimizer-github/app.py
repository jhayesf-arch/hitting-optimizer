"""
Flask API for Enhanced Hitting Optimizer
Provides REST endpoints for swing analysis with web upload and Downloads folder integration
"""

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import json
from pathlib import Path
import traceback
from datetime import datetime
import io

from hitting_optimizer_enhanced import (
    EnhancedHittingOptimizer,
    find_mot_files,
    to_json_serializable,
    TrainingRecommendationEngine
)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.expanduser('~/hitting_optimizer_uploads')
DOWNLOADS_FOLDER = os.path.expanduser('~/Downloads')
RESULTS_FOLDER = os.path.expanduser('~/hitting_optimizer_results')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Store optimizer instances (one per athlete profile)
optimizers = {}

# ═══════════════════════════════════════════════════════════════════════════
# MAIN ROUTES
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """Serve main web interface"""
    return render_template('index.html')

# ═══════════════════════════════════════════════════════════════════════════
# ATHLETE PROFILE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/athlete/create', methods=['POST'])
def create_athlete():
    """Create athlete profile"""
    try:
        data = request.json
        name = data.get('name', 'default')
        height_m = float(data.get('height_m'))
        mass_kg = float(data.get('mass_kg'))
        
        optimizer = EnhancedHittingOptimizer(mass_kg, height_m)
        optimizers[name] = {
            'optimizer': optimizer,
            'height_m': height_m,
            'mass_kg': mass_kg,
            'created_at': datetime.now().isoformat(),
            'swings_analyzed': 0
        }
        
        return jsonify({
            'success': True,
            'athlete_name': name,
            'height_m': height_m,
            'mass_kg': mass_kg,
            'message': f'✅ Athlete profile created: {height_m*100:.0f}cm, {mass_kg:.0f}kg'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/athlete/list', methods=['GET'])
def list_athletes():
    """List all athlete profiles"""
    try:
        athletes = []
        for name, profile in optimizers.items():
            athletes.append({
                'name': name,
                'height_m': profile['height_m'],
                'mass_kg': profile['mass_kg'],
                'created_at': profile['created_at'],
                'swings_analyzed': profile['swings_analyzed']
            })
        return jsonify({'athletes': athletes})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ═══════════════════════════════════════════════════════════════════════════
# MOTION CAPTURE FILE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/files/scan-downloads', methods=['GET'])
def scan_downloads():
    """Scan Downloads folder for .mot files"""
    try:
        files = find_mot_files()
        
        file_list = []
        for f in files:
            file_list.append({
                'filename': os.path.basename(f),
                'path': f,
                'size_kb': os.path.getsize(f) / 1024
            })
        
        return jsonify({
            'success': True,
            'count': len(file_list),
            'files': file_list
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/files/upload', methods=['POST'])
def upload_file():
    """Upload .mot file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.mot'):
            return jsonify({'success': False, 'error': 'Only .mot files allowed'}), 400
        
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'path': filepath,
            'message': '✅ File uploaded successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/files/list-uploaded', methods=['GET'])
def list_uploaded_files():
    """List uploaded files"""
    try:
        files = os.listdir(UPLOAD_FOLDER)
        mot_files = [f for f in files if f.endswith('.mot')]
        
        file_list = []
        for f in mot_files:
            filepath = os.path.join(UPLOAD_FOLDER, f)
            file_list.append({
                'filename': f,
                'size_kb': os.path.getsize(filepath) / 1024,
                'uploaded': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
            })
        
        return jsonify({'success': True, 'files': file_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ═══════════════════════════════════════════════════════════════════════════
# SWING ANALYSIS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/analyze/swing', methods=['POST'])
def analyze_swing():
    """Analyze single swing"""
    try:
        data = request.json
        athlete_name = data.get('athlete_name', 'default')
        file_path = data.get('file_path')
        
        if athlete_name not in optimizers:
            return jsonify({'success': False, 'error': f'Athlete {athlete_name} not found'}), 400
        
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': f'File not found: {file_path}'}), 404
        
        optimizer = optimizers[athlete_name]['optimizer']
        
        # Load and analyze
        kinematics = optimizer.load_mot_file(file_path)
        metrics, findings, recommendations = optimizer.comprehensive_diagnosis(
            kinematics, 
            os.path.basename(file_path)
        )
        
        # Generate training recommendations
        training_recs = optimizer.recommendation_engine.generate_recommendations(metrics)
        recovery_recs = optimizer.recommendation_engine.get_recovery_recommendations(metrics)
        
        # Update profile
        optimizers[athlete_name]['swings_analyzed'] += 1
        
        # Save results
        results_data = {
            'timestamp': datetime.now().isoformat(),
            'athlete': athlete_name,
            'file': os.path.basename(file_path),
            'metrics': to_json_serializable(metrics),
            'findings': findings,
            'recommendations': recommendations,
            'training_program': [to_json_serializable(r) for r in training_recs],
            'recovery_tips': recovery_recs
        }
        
        result_file = os.path.join(
            RESULTS_FOLDER,
            f"{os.path.basename(file_path).replace('.mot', '')}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(result_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        return jsonify({
            'success': True,
            'metrics': to_json_serializable(metrics),
            'findings': findings,
            'recommendations': recommendations,
            'training_program': [to_json_serializable(r) for r in training_recs],
            'recovery_tips': recovery_recs,
            'result_file': result_file
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/analyze/batch', methods=['POST'])
def analyze_batch():
    """Analyze multiple swings from Downloads folder"""
    try:
        data = request.json
        athlete_name = data.get('athlete_name', 'default')
        
        if athlete_name not in optimizers:
            return jsonify({'success': False, 'error': f'Athlete {athlete_name} not found'}), 400
        
        optimizer = optimizers[athlete_name]['optimizer']
        
        # Find .mot files
        files = find_mot_files()
        if not files:
            return jsonify({'success': False, 'error': 'No .mot files found'}), 404
        
        results = []
        for filepath in files:
            try:
                kinematics = optimizer.load_mot_file(filepath)
                metrics, findings, recommendations = optimizer.comprehensive_diagnosis(
                    kinematics,
                    os.path.basename(filepath)
                )
                training_recs = optimizer.recommendation_engine.generate_recommendations(metrics)
                
                results.append({
                    'file': os.path.basename(filepath),
                    'success': True,
                    'metrics': to_json_serializable(metrics),
                    'efficiency_score': metrics.overall_efficiency,
                    'training_recommendations': [to_json_serializable(r) for r in training_recs]
                })
                
                optimizers[athlete_name]['swings_analyzed'] += 1
            except Exception as e:
                results.append({
                    'file': os.path.basename(filepath),
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'total_files': len(files),
            'successful_analyses': len([r for r in results if r['success']]),
            'results': results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ═══════════════════════════════════════════════════════════════════════════
# RESULTS & HISTORY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/results/list', methods=['GET'])
def list_results():
    """List all analysis results"""
    try:
        if not os.path.exists(RESULTS_FOLDER):
            return jsonify({'success': True, 'results': []})
        
        files = os.listdir(RESULTS_FOLDER)
        json_files = [f for f in files if f.endswith('.json')]
        
        results = []
        for f in json_files:
            filepath = os.path.join(RESULTS_FOLDER, f)
            with open(filepath, 'r') as file:
                data = json.load(file)
                results.append({
                    'filename': f,
                    'timestamp': data.get('timestamp'),
                    'athlete': data.get('athlete'),
                    'file': data.get('file'),
                    'efficiency_score': data.get('metrics', {}).get('overall_efficiency', 0)
                })
        
        results.sort(key=lambda x: x['timestamp'], reverse=True)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/results/get/<filename>', methods=['GET'])
def get_result(filename):
    """Get specific analysis result"""
    try:
        filepath = os.path.join(RESULTS_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'Result not found'}), 404
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/results/download/<filename>', methods=['GET'])
def download_result(filename):
    """Download analysis result as JSON"""
    try:
        filepath = os.path.join(RESULTS_FOLDER, filename)
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ═══════════════════════════════════════════════════════════════════════════
# HEALTH CHECK & INFO ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0',
        'features': [
            'body-normalized metrics',
            'torque-based analysis',
            'rotational power (W/kg)',
            'bat speed proxy',
            'exit velocity prediction',
            'advanced training recommendations',
            'batch swing analysis',
            'downloads folder integration'
        ]
    })

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get system info"""
    return jsonify({
        'upload_folder': UPLOAD_FOLDER,
        'downloads_folder': DOWNLOADS_FOLDER,
        'results_folder': RESULTS_FOLDER,
        'athletes_configured': len(optimizers),
        'total_swings_analyzed': sum(p['swings_analyzed'] for p in optimizers.values())
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting Enhanced Hitting Optimizer API Server")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"📁 Downloads folder: {DOWNLOADS_FOLDER}")
    print(f"📁 Results folder: {RESULTS_FOLDER}")
    print("\n🌐 Visit http://localhost:5000 to access the web interface")
    app.run(debug=True, host='localhost', port=5000)
