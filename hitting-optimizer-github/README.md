# ⚾ Enhanced Hitting Optimizer

> **Advanced biomechanical analysis tool for baseball swing optimization using motion capture data**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Features

- **Body-Normalized Metrics** - Fair comparison across different athlete sizes
- **AI Training Recommendations** - Personalized exercise programs with progressions
- **Batch Analysis** - Auto-scan Downloads folder for multiple swings
- **Professional Web Interface** - Modern dashboard with real-time feedback
- **Progress Tracking** - Compare swings over time to measure improvement
- **Exit Velocity Prediction** - Physics-based model using momentum transfer

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/hitting-optimizer.git
cd hitting-optimizer

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py

# Open your browser
open http://localhost:5000
```

## 📸 Screenshots

[Web interface showing analysis dashboard]

## 🔬 How It Works

1. **Create athlete profile** (height/weight for body normalization)
2. **Upload .mot file** from OpenSim motion capture
3. **Get instant analysis** with efficiency score + metrics
4. **Receive training plan** with specific exercises and progressions
5. **Track progress** over time with comparison tools

## 📊 Metrics Calculated

- **Rotational Power** (W/kg) - Hip and shoulder torque generation
- **Hip-Shoulder Separation** (°) - Optimal: 40-60°
- **Bat Speed** (mph) - From lead wrist 3D velocity
- **Exit Velocity** (mph) - Predicted from biomechanics
- **Stride Efficiency** (%) - Normalized by height
- **Sequence Timing** (ms) - Kinetic chain synchronization

## 📁 Project Structure

```
hitting-optimizer/
├── app.py                              # Flask API server
├── hitting_optimizer_enhanced.py       # Biomechanics engine
├── requirements.txt                    # Python dependencies
├── templates/
│   └── index.html                      # Web interface
├── docs/
│   ├── INSTALLATION.md                 # Detailed setup guide
│   ├── API.md                          # API documentation
│   └── TRAINING_GUIDE.md               # Exercise explanations
└── tests/
    └── test_optimizer.py               # Unit tests
```

## 🛠️ Requirements

- **Python 3.8+**
- **Flask 2.3.0+**
- **NumPy, Pandas**
- **OpenSim .mot files** (motion capture data)

## 📖 Documentation

- [Quick Start Guide](QUICK_START.md) - Get started in 5 minutes
- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [API Documentation](docs/API.md) - REST API endpoints
- [Training Guide](docs/TRAINING_GUIDE.md) - Exercise progressions explained

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Body segment parameters from **Winter (2009)** and **de Leva (1996)**
- Biomechanics methodology from **Fleisig et al. (1995)**
- OpenSim motion capture data format

## 📧 Contact

Questions or feedback? Open an issue on GitHub!

## 🔗 Related Projects

- [OpenSim](https://simtk.org/projects/opensim) - Musculoskeletal modeling
- [Driveline Baseball](https://www.drivelinebaseball.com/) - Data-driven player development

---

**Made with ⚾ for athletes and coaches**
