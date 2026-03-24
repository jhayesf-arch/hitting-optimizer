# 🚀 QUICK START GUIDE

## Installation (One-Time Setup)

### Step 1: Install Python Dependencies

```bash
# Navigate to your project directory
cd ~/hitting_optimizer

# Install required packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-2.3.0 Flask-CORS-4.0.0 numpy-1.24.0 pandas-2.0.0 ...
```

### Step 2: Verify Installation

```bash
python setup.py
```

This will confirm everything is set up correctly and create necessary directories.

---

## Using the Web Interface

### Start the Server

**Option 1: Use the start script (macOS/Linux)**
```bash
bash start.sh
```

**Option 2: Direct command**
```bash
python app.py
```

**Expected output:**
```
 * Running on http://localhost:5000
 * Press CTRL+C to quit
```

### Access the Web Interface

1. Open your browser
2. Go to **http://localhost:5000**
3. You should see the Enhanced Hitting Optimizer interface

---

## First Analysis (5 Minutes)

### Step 1: Create Your Profile

1. Click the **"Setup"** tab
2. Enter:
   - **Name**: Your name or athlete ID
   - **Height**: In meters (e.g., 1.83 for 6'0")
   - **Mass**: In kg (e.g., 82 for 180 lbs)
3. Click **"Create Profile"**

### Step 2: Upload a Swing File

1. Click **"Upload & Analyze"** tab
2. Select your athlete from the dropdown
3. Click the file upload area or drag-and-drop a .mot file
4. Wait for analysis (30 seconds - 2 minutes depending on file size)

### Step 3: Review Results

You'll see:
- ✅ **Efficiency Score** (0-100)
- 📊 **Key Metrics** (torque, power, bat speed, stride, etc.)
- 📋 **Findings** (what's working, what needs improvement)
- 💪 **Training Recommendations** (prioritized exercises with progressions)

---

## Auto-Analyze Downloads Folder

### One-Click Batch Analysis

1. **Copy** your .mot files to `~/Downloads`
2. Click **"Auto-Scan Downloads"** tab
3. Click **"Scan Downloads Folder"**
4. Click **"Analyze All Files"**
5. Get comparison across all swings

---

## Understanding Your Results

### Efficiency Score

| Score | Rating | Interpretation |
|-------|--------|-----------------|
| 85-100 | 🟢 EXCELLENT | Elite mechanics - minimize changes |
| 70-84 | 🟡 GOOD | Solid fundamentals - targeted improvements |
| 55-69 | 🟠 FAIR | Multiple areas needing work - structured plan |
| 0-54 | 🔴 POOR | Significant issues - overhaul mechanics |

### Key Metrics

**Rotational Mechanics**
- **Hip Power/kg**: 20+ W/kg is good, 30+ is elite
- **Hip-Shoulder Separation**: 40-60° is optimal
- **Sequence Timing**: <50ms delay is good

**Lower Body**
- **Stride Efficiency**: 100% = optimal for your height (75% of height)

**Bat Speed**
- **Wrist Speed**: 60+ mph average, 70+ mph is good
- **Exit Velocity**: Predicted from biomechanics

### Training Recommendations

**Priority Levels:**
- 🔴 **Priority 1**: CRITICAL - fix first (mechanical issue)
- 🟠 **Priority 2**: HIGH - impacts power/exit velo
- 🟡 **Priority 3**: MEDIUM - efficiency improvements
- 🟢 **Priority 4**: LOW - fine-tuning

**Each Recommendation Includes:**
- ✅ Why it matters
- 💪 Specific exercises (3-5 exercises per recommendation)
- 📈 Progression (beginner → intermediate → advanced)
- ⏱️ Estimated timeline (weeks to see results)
- 📊 Expected improvement percentage

---

## Example: Analyzing Your First Swing

### File: swing_001.mot

**Results:**

```
Efficiency Score: 72/100 (GOOD)

📊 Metrics:
  Hip Power: 28.5 W/kg (above-average)
  Separation: 38° (good)
  Bat Speed: 68 mph (good)
  Stride: 85% efficiency (over-striding slightly)
  Predicted EV: 88 mph

📋 Findings:
  ✅ Proper kinetic chain sequencing
  ✅ Good hip-shoulder separation
  ⚠️ Over-striding - losing stability

💡 Top Recommendations:
  1. Reduce stride length by 10% (add 2-3% more power)
  2. Increase hip rotation power (add 5-8% more exit velo)
  3. Improve lag retention in zone
```

→ **Action Plan**: Focus on Option 1 (stride control drills) first

---

## Tips for Best Results

### 1. Accurate Body Measurements
- Measure height without shoes, in meters
- Use actual body weight in kg at time of motion capture

### 2. Quality .mot Files
Your file should contain these column headers:
```
time, pelvis_tx, pelvis_ty, pelvis_rotation, lumbar_rotation,
R_WRA_tx, R_WRA_ty, R_WRA_tz  (or L_WRA for left-handed)
```

### 3. Multiple Analyses
- Analyze 3-5 swings initially to identify patterns
- Re-analyze every 2-4 weeks after training
- Use comparison dashboard to verify improvements

### 4. Training Progression
- Focus on **one priority at a time**
- Follow the progression scheme (weeks 1-2 beginner, etc.)
- Re-test and adjust plan every 4 weeks

---

## Common Questions

### Q: Where are my files stored?

**Uploaded files:** `~/hitting_optimizer_uploads/`
**Analysis results:** `~/hitting_optimizer_results/` (JSON format)
**Downloads folder:** `~/Downloads/` (auto-scanned)

### Q: Can I download my results?

Yes! Go to **"Results"** tab and click **"Download"** to save analysis as JSON.

### Q: What if I get an error?

**File not found:**
- Check .mot file is in the correct location
- Verify filename has .mot extension

**Analysis failed:**
- File might be corrupted
- Try a different .mot file

**Port 5000 in use:**
- Another program is using the port
- Change port in app.py: `port=5001`

### Q: Can I analyze multiple athletes?

Yes! Create separate profiles for each athlete in the Setup tab.

---

## Keyboard Shortcuts

| Action | Keyboard |
|--------|----------|
| Stop server | **Ctrl + C** |
| Focus bar | **Cmd + L** (Chrome) |
| Refresh page | **Cmd + R** |

---

## Troubleshooting

### Server won't start

```bash
# Check if Python is installed
python3 --version

# Check if dependencies are installed
python3 -c "import flask"

# Check if port 5000 is available
lsof -i :5000
```

### Files not found

```bash
# Verify Downloads folder
ls ~/Downloads/*.mot

# Verify upload folder
ls ~/hitting_optimizer_uploads/
```

### Slow analysis

- Large .mot files (>20MB) take longer
- Check CPU usage: click Activity Monitor
- Normal analysis time: 30 seconds - 2 minutes

---

## Next Steps

1. ✅ Install dependencies (`pip install -r requirements.txt`)
2. ✅ Start server (`python app.py`)
3. ✅ Create profile (http://localhost:5000)
4. ✅ Upload swing file
5. ✅ Review results and recommendations
6. ✅ Start training program (week 1 exercises)
7. ✅ Re-analyze in 4 weeks to measure progress

---

## Support & Documentation

- **Full ReadMe**: Open `README.md`
- **API Reference**: See comments in `app.py`
- **Biomechanics Details**: See `hitting_optimizer_enhanced.py`

---

**Estimated initial setup time: 5-10 minutes**
**First analysis time: 2-5 minutes**

**Ready to optimize your swing? 🎯**

```
Python 3.8+ ✅
Flask ✅
Dependencies ✅
→ Launch http://localhost:5000
```
