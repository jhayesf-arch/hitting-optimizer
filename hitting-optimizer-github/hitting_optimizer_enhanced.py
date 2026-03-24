"""
REFINED HITTING OPTIMIZATION SYSTEM
Critical refinements based on biomechanics best practices:

✅ FIX #1: Shoulder inertia includes arms + bat (not just trunk)
✅ FIX #2: Savitzky-Golay filter for robust 2nd derivatives
✅ FIX #3: Kinematic event detection for stride (not mid_frame)

Auto-loads .mot files from Downloads folder
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Try to import scipy for Savitzky-Golay filtering (optional but recommended)
try:
    from scipy.signal import savgol_filter
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("⚠️  scipy not found - using basic smoothing (install scipy for better results)")

# ═══════════════════════════════════════════════════════════════════════════
# SMOOTHING & DIFFERENTIATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def smooth_data(data, window=11):
    """Moving average smoothing"""
    if len(data) < window:
        return data
    kernel = np.ones(window) / window
    padded = np.pad(data, (window//2, window//2), mode='edge')
    return np.convolve(padded, kernel, mode='valid')[:len(data)]

def savgol_smooth_and_diff(data, window=11, polyorder=3, deriv=0, dt=1.0):
    """
    Savitzky-Golay filter for smoothing and differentiation
    BEST PRACTICE in biomechanics for 2nd derivatives!
    
    deriv=0: smooth only
    deriv=1: velocity
    deriv=2: acceleration (much better than double np.gradient!)
    
    dt: time step for scaling derivatives
    """
    if not HAS_SCIPY:
        # Fallback to basic smoothing
        if deriv == 0:
            return smooth_data(data, window)
        elif deriv == 1:
            smoothed = smooth_data(data, window)
            return np.gradient(smoothed, dt)
        elif deriv == 2:
            smoothed = smooth_data(data, window)
            vel = np.gradient(smoothed, dt)
            return np.gradient(vel, dt)
    
    # Use Savitzky-Golay (best practice)
    if len(data) < window:
        window = len(data) if len(data) % 2 == 1 else len(data) - 1
        if window < polyorder + 2:
            polyorder = max(1, window - 2)
    
    # Savitzky-Golay returns derivatives scaled by dt already
    result = savgol_filter(data, window, polyorder, deriv=deriv, delta=dt)
    return result

# ═══════════════════════════════════════════════════════════════════════════
# ANTHROPOMETRIC BODY SEGMENT PARAMETERS
# ═══════════════════════════════════════════════════════════════════════════

SEGMENT_PARAMS = {
    'forearm': {'mass_pct': 0.016, 'length_pct': 0.146, 'com_pct': 0.430, 'rg_pct': 0.303},
    'upper_arm': {'mass_pct': 0.028, 'length_pct': 0.186, 'com_pct': 0.436, 'rg_pct': 0.322},
    'trunk': {'mass_pct': 0.497, 'length_pct': 0.288, 'com_pct': 0.500, 'rg_pct': 0.496},
    'thigh': {'mass_pct': 0.100, 'length_pct': 0.245, 'com_pct': 0.433, 'rg_pct': 0.323},
    'shank': {'mass_pct': 0.0465, 'length_pct': 0.246, 'com_pct': 0.433, 'rg_pct': 0.302},
}

@dataclass
class RefinedSwingMetrics:
    """Complete swing metrics with all refinements"""
    # Kinetics (with corrected inertias)
    peak_hip_torque_Nm: float
    peak_shoulder_torque_Nm: float
    peak_hip_power_W: float
    peak_shoulder_power_W: float
    
    # Inertia comparison
    hip_inertia_kg_m2: float
    shoulder_inertia_kg_m2: float
    inertia_ratio: float  # shoulder/hip
    
    # Body-normalized power
    hip_power_per_kg: float
    shoulder_power_per_kg: float
    
    # Rotation
    max_separation_deg: float
    sequence_timing_ms: float
    proper_sequence: bool
    
    # Stride (with event detection)
    stride_length_m: float
    stride_ratio: float
    stride_efficiency_pct: float
    plant_frame: int
    plant_method: str  # "velocity_threshold" or "fallback"
    
    # Exit velocity
    predicted_exit_velo: float
    
    # Efficiency score
    overall_efficiency: int

class RefinedHittingOptimizer:
    """
    REFINED hitting optimization with biomechanics best practices
    """
    
    def __init__(self, body_mass_kg: float, body_height_m: float):
        self.body_mass_kg = body_mass_kg
        self.body_height_m = body_height_m
        self.g = 9.81
        self.calculate_segment_properties()
        
        print(f"\n✅ Initialized for {self.body_height_m*100:.0f}cm, {self.body_mass_kg:.0f}kg hitter")
        if HAS_SCIPY:
            print("✅ Using Savitzky-Golay filter for derivatives (optimal)")
        else:
            print("⚠️  Using basic smoothing (install scipy for better acceleration)")
        
    def calculate_segment_properties(self):
        """Calculate segment-specific parameters"""
        self.segments = {}
        
        for segment_name, params in SEGMENT_PARAMS.items():
            self.segments[segment_name] = {
                'mass': self.body_mass_kg * params['mass_pct'],
                'length': self.body_height_m * params['length_pct'],
                'com_dist': self.body_height_m * params['length_pct'] * params['com_pct'],
                'I': self.body_mass_kg * params['mass_pct'] * 
                     (self.body_height_m * params['length_pct'] * params['rg_pct'])**2
            }
            
    def load_mot_file(self, filepath: str) -> pd.DataFrame:
        """Load OpenSim .mot file"""
        with open(filepath, 'r') as f:
            lines = f.readlines()
            
        header_end = 0
        for i, line in enumerate(lines):
            if 'endheader' in line.lower():
                header_end = i + 1
                break
                
        data = pd.read_csv(filepath, sep='\t', skiprows=header_end, skipinitialspace=True)
        data.columns = data.columns.str.strip()
        
        return data
        
    def calculate_rotational_torques_refined(self, data: pd.DataFrame) -> Dict:
        """
        REFINED: Correct inertias + Savitzky-Golay derivatives
        
        FIX #1: Shoulder inertia = trunk + 2×arms + bat
        FIX #2: Savitzky-Golay for acceleration (not double gradient)
        """
        dt = data['time'].diff().mean()
        
        if 'pelvis_rotation' not in data.columns or 'lumbar_rotation' not in data.columns:
            print("⚠️ Missing rotation data")
            return None
            
        # PELVIS (hip) rotation
        pelvis_angle = np.deg2rad(data['pelvis_rotation'].values)
        
        # FIX #2: Use Savitzky-Golay for derivatives
        if HAS_SCIPY:
            pelvis_omega = savgol_smooth_and_diff(pelvis_angle, window=11, polyorder=3, deriv=1, dt=dt)
            pelvis_alpha = savgol_smooth_and_diff(pelvis_angle, window=11, polyorder=3, deriv=2, dt=dt)
        else:
            pelvis_smooth = smooth_data(pelvis_angle, window=11)
            pelvis_omega = np.gradient(pelvis_smooth, dt)
            pelvis_alpha = np.gradient(pelvis_omega, dt)
        
        # SHOULDER rotation (pelvis + lumbar)
        lumbar_angle = np.deg2rad(data['lumbar_rotation'].values)
        shoulder_angle = pelvis_angle + lumbar_angle
        
        if HAS_SCIPY:
            shoulder_omega = savgol_smooth_and_diff(shoulder_angle, window=11, polyorder=3, deriv=1, dt=dt)
            shoulder_alpha = savgol_smooth_and_diff(shoulder_angle, window=11, polyorder=3, deriv=2, dt=dt)
        else:
            shoulder_smooth = smooth_data(shoulder_angle, window=11)
            shoulder_omega = np.gradient(shoulder_smooth, dt)
            shoulder_alpha = np.gradient(shoulder_omega, dt)
        
        # FIX #1: CORRECTED inertias
        # Hip: Just trunk
        trunk_I = self.segments['trunk']['I']
        hip_inertia = trunk_I
        hip_torque = hip_inertia * pelvis_alpha
        
        # Shoulder: Trunk + 2 arms + bat
        upper_arm_I = self.segments['upper_arm']['I']
        forearm_I = self.segments['forearm']['I']
        
        # Bat: 32 oz (0.91 kg) at ~0.6m from rotation axis
        bat_mass = 0.91  # kg
        bat_radius = 0.6  # m from body center
        bat_I = bat_mass * bat_radius**2
        
        shoulder_inertia = trunk_I + 2 * (upper_arm_I + forearm_I) + bat_I
        shoulder_torque = shoulder_inertia * shoulder_alpha
        
        # Inertia ratio (should be ~2-3×)
        inertia_ratio = shoulder_inertia / hip_inertia
        
        # Rotational POWER: P = τ × ω
        hip_power = hip_torque * pelvis_omega
        shoulder_power = shoulder_torque * shoulder_omega
        
        # Peaks
        peak_hip_torque = np.max(np.abs(hip_torque))
        peak_shoulder_torque = np.max(np.abs(shoulder_torque))
        peak_hip_power = np.max(np.abs(hip_power))
        peak_shoulder_power = np.max(np.abs(shoulder_power))
        
        # Body-normalized
        hip_power_per_kg = peak_hip_power / self.body_mass_kg
        shoulder_power_per_kg = peak_shoulder_power / self.body_mass_kg
        
        # Separation
        separation = (shoulder_angle - pelvis_angle) * 180/np.pi
        max_separation = np.max(np.abs(separation))
        
        # Sequencing
        peak_hip_frame = np.argmax(np.abs(pelvis_omega))
        peak_shoulder_frame = np.argmax(np.abs(shoulder_omega))
        sequence_timing_ms = (peak_shoulder_frame - peak_hip_frame) * dt * 1000
        proper_sequence = peak_hip_frame < peak_shoulder_frame
        
        return {
            'peak_hip_torque_Nm': peak_hip_torque,
            'peak_shoulder_torque_Nm': peak_shoulder_torque,
            'peak_hip_power_W': peak_hip_power,
            'peak_shoulder_power_W': peak_shoulder_power,
            'hip_inertia_kg_m2': hip_inertia,
            'shoulder_inertia_kg_m2': shoulder_inertia,
            'inertia_ratio': inertia_ratio,
            'hip_power_per_kg': hip_power_per_kg,
            'shoulder_power_per_kg': shoulder_power_per_kg,
            'max_separation_deg': max_separation,
            'sequence_timing_ms': sequence_timing_ms,
            'proper_sequence': proper_sequence,
            'pelvis_omega': pelvis_omega  # For stride calculation
        }
        
    def calculate_stride_refined(self, data: pd.DataFrame, rotation: Dict = None) -> Dict:
        """
        REFINED: Kinematic event detection instead of mid_frame
        
        FIX #3: Use hip rotation velocity to find foot plant
        """
        if 'pelvis_tx' not in data.columns or 'pelvis_ty' not in data.columns:
            print("⚠️ Missing pelvis position data")
            return None
            
        pelvis_x = data['pelvis_tx'].values
        pelvis_y = data['pelvis_ty'].values
        dt = data['time'].diff().mean()
        
        # FIX #3: Find foot plant using hip rotation velocity
        if rotation and 'pelvis_omega' in rotation:
            # Use already-calculated pelvis_omega
            pelvis_omega = rotation['pelvis_omega']
            pelvis_omega_deg = np.abs(pelvis_omega) * 180/np.pi
            
            # Threshold: when hips start rotating hard (>100°/s)
            threshold = 100  # °/s
            plant_candidates = np.where(pelvis_omega_deg > threshold)[0]
            
            if len(plant_candidates) > 0:
                plant_frame = plant_candidates[0]
                plant_method = "velocity_threshold"
            else:
                plant_frame = np.argmax(pelvis_omega_deg)
                plant_method = "peak_rotation"
                print(f"   ⚠️  Using peak rotation (no clear threshold crossing)")
        else:
            # Fallback to mid_frame
            plant_frame = len(data) // 2
            plant_method = "fallback_midframe"
            print(f"   ⚠️  Using mid_frame fallback (no rotation data)")
        
        # Stride = distance from start to plant
        start_pos = np.array([pelvis_x[0], pelvis_y[0]])
        plant_pos = np.array([pelvis_x[plant_frame], pelvis_y[plant_frame]])
        stride_length = np.linalg.norm(plant_pos - start_pos)
        
        # NORMALIZE by height
        stride_ratio = stride_length / self.body_height_m
        optimal_stride_ratio = 0.75
        stride_efficiency_pct = (stride_ratio / optimal_stride_ratio) * 100
        
        return {
            'stride_length_m': stride_length,
            'stride_length_ft': stride_length * 3.28084,
            'stride_ratio': stride_ratio,
            'stride_efficiency_pct': stride_efficiency_pct,
            'plant_frame': plant_frame,
            'plant_time': data['time'].iloc[plant_frame],
            'plant_method': plant_method
        }
        
    def predict_exit_velocity(self, rotation: Dict) -> Dict:
        """Predict exit velocity from mechanics"""
        if not rotation:
            return None
            
        power_per_kg = rotation['hip_power_per_kg']
        separation = rotation['max_separation_deg']
        proper_seq = rotation['proper_sequence']
        
        base_velo = 60 + (power_per_kg * 0.8)
        
        if 40 <= separation <= 60:
            sep_bonus = 5
        elif separation < 40:
            sep_bonus = -5
        else:
            sep_bonus = 0
            
        seq_bonus = 5 if proper_seq else -10
        predicted_exit_velo = base_velo + sep_bonus + seq_bonus
        
        return {'predicted_exit_velo': predicted_exit_velo}
        
    def comprehensive_diagnosis(self, kinematics: pd.DataFrame, filename: str) -> RefinedSwingMetrics:
        """Complete refined diagnosis"""
        
        print("\n" + "="*70)
        print(f"REFINED SWING ANALYSIS: {filename}")
        print("="*70)
        
        # Calculate all metrics
        rotation = self.calculate_rotational_torques_refined(kinematics)
        stride = self.calculate_stride_refined(kinematics, rotation)
        exit_velo = self.predict_exit_velocity(rotation)
        
        findings = []
        recommendations = []
        efficiency_score = 100
        
        # === ROTATIONAL MECHANICS ===
        if rotation:
            print(f"\n🔄 ROTATIONAL MECHANICS (Corrected Inertias):")
            print(f"   Hip Inertia:      {rotation['hip_inertia_kg_m2']:.4f} kg⋅m²")
            print(f"   Shoulder Inertia: {rotation['shoulder_inertia_kg_m2']:.4f} kg⋅m² ({rotation['inertia_ratio']:.1f}× hip)")
            print(f"   Peak Hip Torque:      {rotation['peak_hip_torque_Nm']:.1f} N⋅m")
            print(f"   Peak Shoulder Torque: {rotation['peak_shoulder_torque_Nm']:.1f} N⋅m")
            print(f"   Peak Hip Power:       {rotation['peak_hip_power_W']:.0f} W ({rotation['hip_power_per_kg']:.1f} W/kg)")
            print(f"   Peak Shoulder Power:  {rotation['peak_shoulder_power_W']:.0f} W ({rotation['shoulder_power_per_kg']:.1f} W/kg)")
            print(f"   Max Separation:       {rotation['max_separation_deg']:.1f}°")
            print(f"   Sequence Timing:      {rotation['sequence_timing_ms']:.0f} ms")
            print(f"   Proper Sequence:      {'YES ✅' if rotation['proper_sequence'] else 'NO ❌'}")
            
            # Diagnostics (same as before)
            if not rotation['proper_sequence']:
                findings.append("❌ REVERSED SEQUENCE")
                recommendations.append("URGENT: Fix kinetic chain")
                efficiency_score -= 25
            elif rotation['sequence_timing_ms'] < 20:
                findings.append("⚠️ Poor synchronization")
                efficiency_score -= 15
            else:
                findings.append("✅ Proper sequencing")
                
            if rotation['max_separation_deg'] < 30:
                findings.append("⚠️ Low separation")
                efficiency_score -= 20
            elif rotation['max_separation_deg'] > 70:
                findings.append("⚠️ Excessive separation")
                efficiency_score -= 10
            else:
                findings.append("✅ Good separation")
                
            if rotation['hip_power_per_kg'] < 20:
                findings.append("⚠️ Low rotational power")
                efficiency_score -= 15
            else:
                findings.append("✅ Good power")
                
        # === STRIDE ===
        if stride:
            print(f"\n🦵 STRIDE (Event Detection):")
            print(f"   Plant Frame: {stride['plant_frame']} at t={stride['plant_time']:.2f}s ({stride['plant_method']})")
            print(f"   Stride Length:    {stride['stride_length_ft']:.2f} ft ({stride['stride_ratio']:.2f} × height)")
            print(f"   Stride Efficiency: {stride['stride_efficiency_pct']:.0f}%")
            
            if stride['stride_efficiency_pct'] < 70:
                findings.append("⚠️ Short stride")
                efficiency_score -= 15
            elif stride['stride_efficiency_pct'] > 130:
                findings.append("⚠️ Over-striding")
                efficiency_score -= 10
            else:
                findings.append("✅ Optimal stride")
                
        # === EXIT VELO ===
        if exit_velo:
            print(f"\n⚡ EXIT VELOCITY: {exit_velo['predicted_exit_velo']:.1f} mph (predicted)")
            
        # === SUMMARY ===
        print(f"\n" + "="*70)
        print(f"OVERALL EFFICIENCY: {max(0, efficiency_score)}/100")
        print("="*70)
        
        for finding in findings:
            print(f"   {finding}")
            
        metrics = RefinedSwingMetrics(
            peak_hip_torque_Nm=rotation['peak_hip_torque_Nm'] if rotation else 0,
            peak_shoulder_torque_Nm=rotation['peak_shoulder_torque_Nm'] if rotation else 0,
            peak_hip_power_W=rotation['peak_hip_power_W'] if rotation else 0,
            peak_shoulder_power_W=rotation['peak_shoulder_power_W'] if rotation else 0,
            hip_inertia_kg_m2=rotation['hip_inertia_kg_m2'] if rotation else 0,
            shoulder_inertia_kg_m2=rotation['shoulder_inertia_kg_m2'] if rotation else 0,
            inertia_ratio=rotation['inertia_ratio'] if rotation else 0,
            hip_power_per_kg=rotation['hip_power_per_kg'] if rotation else 0,
            shoulder_power_per_kg=rotation['shoulder_power_per_kg'] if rotation else 0,
            max_separation_deg=rotation['max_separation_deg'] if rotation else 0,
            sequence_timing_ms=rotation['sequence_timing_ms'] if rotation else 0,
            proper_sequence=rotation['proper_sequence'] if rotation else False,
            stride_length_m=stride['stride_length_m'] if stride else 0,
            stride_ratio=stride['stride_ratio'] if stride else 0,
            stride_efficiency_pct=stride['stride_efficiency_pct'] if stride else 0,
            plant_frame=stride['plant_frame'] if stride else 0,
            plant_method=stride['plant_method'] if stride else "none",
            predicted_exit_velo=exit_velo['predicted_exit_velo'] if exit_velo else 0,
            overall_efficiency=max(0, efficiency_score)
        )
        
        return metrics

def find_mot_files() -> List[str]:
    """Auto-find .mot files"""
    current_dir = os.getcwd()
    local_files = glob.glob("*.mot")
    downloads_path = os.path.expanduser("~/Downloads")
    downloads_files = glob.glob(os.path.join(downloads_path, "*.mot"))
    all_files = local_files + downloads_files
    swing_files = [f for f in all_files if 'swing' in os.path.basename(f).lower()]
    return swing_files

def main():
    print("="*70)
    print("REFINED HITTING OPTIMIZATION SYSTEM")
    print("With Critical Biomechanics Refinements")
    print("="*70)
    print("\nREFINEMENTS:")
    print("  ✅ FIX #1: Shoulder inertia = trunk + 2×arms + bat")
    print("  ✅ FIX #2: Savitzky-Golay filter for acceleration")
    print("  ✅ FIX #3: Kinematic event detection for stride")
    print("="*70)
    
    swing_files = find_mot_files()
    if not swing_files:
        print("\n❌ No swing .mot files found in Downloads or current directory")
        return
        
    print(f"\n✅ Found {len(swing_files)} swing files")
    
    body_mass_kg = 82
    body_height_m = 1.83
    
    optimizer = RefinedHittingOptimizer(body_mass_kg, body_height_m)
    
    all_metrics = []
    for filepath in swing_files:
        filename = os.path.basename(filepath)
        kinematics = optimizer.load_mot_file(filepath)
        metrics = optimizer.comprehensive_diagnosis(kinematics, filename)
        
        all_metrics.append({
            'file': filename,
            'score': metrics.overall_efficiency,
            'inertia_ratio': metrics.inertia_ratio,
            'hip_power_W_kg': metrics.hip_power_per_kg,
            'plant_method': metrics.plant_method
        })
        
    if len(all_metrics) > 1:
        df = pd.DataFrame(all_metrics)
        print("\n" + "="*70)
        print("COMPARISON")
        print("="*70)
        print(df.to_string(index=False))
        df.to_csv('refined_swing_comparison.csv', index=False)
        print("\n✅ Saved: refined_swing_comparison.csv")
        
    print("\n" + "="*70)
    print("✅ REFINED ANALYSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
