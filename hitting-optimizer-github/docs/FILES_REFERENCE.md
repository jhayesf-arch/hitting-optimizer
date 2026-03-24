# 📑 PROJECT FILES REFERENCE

## Core Application Files

### `app.py` (Flask Backend Server)
**Purpose**: REST API server that powers the web interface
**Key features**:
- Athlete profile management
- File upload/download handling
- Swing analysis orchestration
- Batch processing
- Results storage/retrieval
- CORS enabled for web requests

**How to use**: `python app.py` → serves on http://localhost:5000

**Key endpoints**:
- `GET /` - Main web interface
- `POST /api/athlete/create` - Create athlete
- `POST /api/analyze/swing` - Analyze single swing
- `POST /api/analyze/batch` - Batch analyze
- `GET /api/results/list` - List analyses

---

### `hitting_optimizer_enhanced.py` (Biomechanics Engine)
**Purpose**: Core biomechanics analysis with AI recommendations
**Key classes**:
- `EnhancedHittingOptimizer` - Main analysis engine
- `TrainingRecommendationEngine` - Generates training plans
- `TrainingRecommendation` - Dataclass for recommendations
- `EnhancedSwingMetrics` - Metrics dataclass

**Key methods**:
- `load_mot_file()` - Parse OpenSim .mot files
- `calculate_rotational_torques_enhanced()` - Actual torque calculation
- `calculate_stride_normalized()` - Height-normalized stride analysis
- `calculate_bat_speed_proxy()` - Wrist velocity to bat speed
- `comprehensive_diagnosis()` - Full swing analysis
- `generate_recommendations()` - AI training program generation

**How to use**: 
```python
from hitting_optimizer_enhanced import EnhancedHittingOptimizer
optimizer = EnhancedHittingOptimizer(body_mass_kg=82, body_height_m=1.83)
metrics, findings, recommendations = optimizer.comprehensive_diagnosis(data, filename)
```

---

### `templates/index.html` (Web Interface)
**Purpose**: Frontend UI for webapp
**Features**:
- Athlete profile management
- File upload with drag-and-drop
- Downloads folder auto-scan
- Real-time analysis feedback
- Results history browser
- Swing comparison dashboard
- Responsive design (mobile-friendly)

**Sections**:
1. Setup Tab - Create athlete profiles
2. Upload & Analyze Tab - Upload individual files
3. Auto-Scan Downloads Tab - Batch analyze
4. Results Tab - Browse analysis history  
5. Comparison Tab - Compare multiple swings

**Technology**: Vanilla JavaScript + Chart.js + CSS Grid

---

## Configuration & Setup Files

### `requirements.txt`
**Purpose**: Python package dependencies
**Packages**:
- Flask 2.3.0 - Web framework
- Flask-CORS 4.0.0 - Cross-origin requests
- numpy 1.24.0 - Numerical computing
- pandas 2.0.0 - Data analysis
- matplotlib 3.7.0 - Plotting (future use)
- python-dateutil 2.8.2 - Date handling

**How to use**: `pip install -r requirements.txt`

---

### `setup.py`
**Purpose**: Installation verification script
**Checks**:
- Python version (3.8+)
- Dependency installation
- Directory structure
- Project files integrity

**How to use**: `python setup.py`
**Output**: Confirms setup complete or identifies issues

---

### `start.sh`
**Purpose**: Quick-start launcher script (macOS/Linux)
**Does**:
1. Checks Python installation
2. Verifies dependencies
3. Creates directories
4. Launches Flask server

**How to use**: `bash start.sh`

---

## Documentation Files

### `README.md` (Full Documentation)
**Sections**:
- Features list
- Installation instructions
- Usage guide (web interface & CLI)
- File structure
- API endpoint reference
- Metrics explanation
- Troubleshooting guide
- Version history

**Who should read**: Everyone before getting started

---

### `QUICK_START.md` (Quick Start Guide)
**Sections**:
- One-time installation
- Starting the server
- First analysis walkthrough
- Understanding results
- Tips for best results
- Common Q&A
- Troubleshooting

**Who should read**: First-time users (read this first!)

---

### `PROJECT_SUMMARY.md` (High-Level Overview)
**Sections**:
- What's been created
- New features added
- Quick start (3 steps)
- How it works
- Key improvements
- Analysis output details
- Technical architecture

**Who should read**: Anyone wanting overview of what was built

---

### `TRAINING_RECOMMENDATIONS_GUIDE.md` (Detailed Training Guide)
**Sections**:
- How recommendation engine works
- Priority levels explained
- Exercise progressions
- Recovery & injury prevention
- Training timelines
- Example full training plan
- Key principles
- Making adjustments

**Who should read**: Athletes/trainers using the recommendations

---

## Directory Structure

### Automatic Directories (Created when running)

**`~/hitting_optimizer_uploads/`**
- Location: User's home directory
- Contents: Uploaded .mot files
- Purpose: Stores files users upload via web interface
- Cleanup: Safe to delete (re-uploaded files will recreate)

**`~/hitting_optimizer_results/`**
- Location: User's home directory
- Contents: JSON analysis results
- Purpose: Stores all analysis outputs
- Format: `{filename}_analysis_{timestamp}.json`
- Cleanup: Safe to delete (can be re-exported from web UI)

**`~/Downloads/`** (Existing)
- Location: Standard Downloads folder
- Contents: Your .mot files
- Purpose: Auto-scanned by batch analyzer
- No changes made by system

---

## File Dependencies

```
app.py
├── Requires: hitting_optimizer_enhanced.py
├── Requires: templates/index.html
└── Uses: Flask, Flask-CORS

hitting_optimizer_enhanced.py
├── Requires: numpy, pandas
└── Standalone (can run directly)

templates/index.html
├── Requires: app.py running
├── Uses: Chart.js (CDN)
└── Standalone (can open locally but no backend)

requirements.txt
└── Lists all Python dependencies

setup.py, start.sh
├── Require: app.py, hitting_optimizer_enhanced.py
└── Helpers (not critical)
```

---

## Which File to Edit

### If you want to...

**Add new metrics**
→ Edit `hitting_optimizer_enhanced.py` - Method: `comprehensive_diagnosis()`

**Change training exercises**
→ Edit `hitting_optimizer_enhanced.py` - Class: `TrainingRecommendationEngine`

**Modify web interface**
→ Edit `templates/index.html` - All UI code

**Add new API endpoint**
→ Edit `app.py` - Add `@app.route()` function

**Change server settings**
→ Edit `app.py` - Modify `UPLOAD_FOLDER`, port, etc.

**Update documentation**
→ Edit `.md` files - These are just text files

---

## File Sizes

```
app.py                          ~15 KB
hitting_optimizer_enhanced.py   ~40 KB
templates/index.html            ~60 KB
requirements.txt               ~0.2 KB
README.md                       ~15 KB
QUICK_START.md                  ~12 KB
PROJECT_SUMMARY.md              ~8 KB
TRAINING_RECOMMENDATIONS_GUIDE  ~18 KB
setup.py                        ~3 KB
start.sh                        ~2 KB
```

**Total**: ~173 KB initial + dependencies

---

## How Files Work Together

```
User opens browser
    ↓
[Flask Server: app.py]
    ↓
Serves [Web UI: index.html]
    ↓
User clicks "Upload"
    ↓
[Frontend JavaScript]
    ↓
API call to [app.py]
    ↓
Creates [EnhancedHittingOptimizer]  
    ↓
Loads [hitting_optimizer_enhanced.py]
    ↓
Analyzes .mot file
    ↓
Generates [TrainingRecommendations]
    ↓
Returns JSON to [Frontend]
    ↓
Displays results in [UI]
    ↓
Saves result to [~/hitting_optimizer_results/]
```

---

## Backup/Version Control

### Important Files to Back Up
```
~/hitting_optimizer_uploads/*          # Your uploaded files
~/hitting_optimizer_results/*          # Your analysis results
~/hitting_optimizer/                   # All application files
```

### Safe to Delete (Can be recreated)
```
__pycache__/
*.pyc
.DS_Store
~/.hitting_optimizer_*/(directory structure, not data)
```

### Version Control Setup
```bash
# If using Git:
git init
git add *.py *.md templates/ requirements.txt
git add .gitignore
git commit -m "Initial commit"
git remote add origin <repo-url>
git push -u origin main
```

---

## Running Different Ways

### 1. Web Interface (Recommended)
```bash
python app.py
# Open http://localhost:5000
```

### 2. Command Line (Original)
```bash
python hitting_optimizer_enhanced.py
# Analyzes all .mot files in Downloads
```

### 3. Direct Python Script
```bash
python3 -c "
from hitting_optimizer_enhanced import *
opt = EnhancedHittingOptimizer(82, 1.83)
data = opt.load_mot_file('swing.mot')
metrics, findings, recs = opt.comprehensive_diagnosis(data, 'swing.mot')
"
```

### 4. Setup Verification
```bash
python setup.py
```

### 5. Fast Start Script
```bash
bash start.sh
```

---

## Troubleshooting File Issues

**"ModuleNotFoundError: No module named 'hitting_optimizer_enhanced'"**
→ Make sure both .py files are in same directory

**"404 Not Found" on http://localhost:5000**
→ Check `templates/index.html` exists in `templates/` subfolder

**"CORS error" in browser console**
→ Verify `Flask-CORS` installed: `pip install Flask-CORS`

**"Permission denied" when running**
→ Make executable: `chmod +x start.sh setup.py`

**"Port 5000 already in use"**
→ Change port in `app.py`: `app.run(..., port=5001)`

---

## File Editing Guide

### Python Files (.py)
- Use any text editor (VS Code, PyCharm, Sublime)
- Syntax highlighting recommended
- Save and restart server to apply changes

### HTML/JavaScript (index.html)
- Use VS Code or similar
- Refresh browser to see changes  
- Chrome DevTools (F12) for debugging

### Markdown Files (.md)
- Just text files - edit in any editor
- https://www.markdownguide.org/ for syntax

### Configuration (requirements.txt, .sh)
- Text files - edit normally
- Be careful with formatting

---

## File Permissions

```bash
# Make scripts executable:
chmod +x start.sh setup.py

# Make directories writable:
chmod 755 ~/hitting_optimizer_uploads
chmod 755 ~/hitting_optimizer_results

# Verify permissions:
ls -la app.py start.sh
```

---

That's it! You now have everything needed to run your enhanced hitting optimizer with a professional web interface and AI-powered training recommendations. 🎯

**Next step**: Run `python app.py` and open http://localhost:5000!
