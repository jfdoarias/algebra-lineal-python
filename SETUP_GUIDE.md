# 🚀 Setup Guide for Competencias Project in PyCharm

## 📁 Files You Need to Copy

From this location to your PyCharm project (`/Users/brainseeg/PycharmProjects/competencias`):

### Required Files:
```
algebra-lineal-python/
└── 12 - Simulacion de Senales EEG/
    └── Step1_Simulacion_SEEG.ipynb  ← Copy this notebook
```

## 📋 Step-by-Step Instructions

### Step 1: Copy the Notebook to Your Project

**Option A - Using Finder (easiest):**
1. Open Finder
2. Navigate to where this file is located (ask me for the full path)
3. Copy the folder `12 - Simulacion de Senales EEG`
4. Paste it into `/Users/brainseeg/PycharmProjects/competencias/`

**Option B - Using Terminal in PyCharm:**
```bash
cd /Users/brainseeg/PycharmProjects/competencias
mkdir -p "12 - Simulacion de Senales EEG"
# I'll provide the copy command once you confirm the path
```

### Step 2: Set Up Python Virtual Environment in PyCharm

1. **Open PyCharm** with your competencias project
2. Go to: **PyCharm → Settings** (or `Cmd + ,` on Mac)
3. Navigate to: **Project: competencias → Python Interpreter**
4. Click the ⚙️ gear icon → **Add Interpreter** → **Add Local Interpreter**
5. Choose **Virtualenv Environment**
   - Location: `/Users/brainseeg/PycharmProjects/competencias/venv`
   - Base interpreter: Select Python 3.8 or higher (preferably 3.10+)
   - ✅ Check "Inherit global site-packages" if you have packages installed globally
6. Click **OK**

### Step 3: Install Required Packages

In PyCharm's **Terminal** (bottom panel), run:

```bash
# Activate virtual environment (should happen automatically)
# Then install packages:
pip install --upgrade pip
pip install numpy scipy matplotlib jupyter ipykernel
```

**Expected versions:**
- numpy >= 1.21.0
- scipy >= 1.7.0
- matplotlib >= 3.4.0
- jupyter >= 1.0.0

### Step 4: Configure Jupyter in PyCharm

1. After installing packages, PyCharm may prompt: **"Jupyter package not found"**
   - Click **"Install"** if prompted
2. Restart PyCharm to ensure Jupyter is recognized

### Step 5: Open and Run the Notebook

1. In Project panel: Navigate to `12 - Simulacion de Senales EEG/Step1_Simulacion_SEEG.ipynb`
2. Double-click to open
3. PyCharm will show the notebook interface
4. At the top, verify the **interpreter** is set to your venv (should show: Python 3.x (competencias))
5. Click **▶ Run All Cells** or run cell-by-cell with `Shift + Enter`

## 🔧 Recommended PyCharm Settings for Jupyter Notebooks

### Enable Scientific Mode:
1. `View → Scientific Mode` ✅
2. This gives you better visualization panels for plots

### Configure Plot Backend:
1. `Settings → Tools → Python Scientific`
2. ✅ Enable "Show plots in tool window"

### Increase Memory (for large datasets):
1. `Help → Edit Custom VM Options`
2. Add: `-Xmx4096m` (4GB RAM for PyCharm)

## 📊 Expected Output After Running Step 1

You should see:
1. ✅ "Librerias importadas correctamente"
2. ✅ Configuration summary (12 channels, 1024 Hz, etc.)
3. ✅ Channel-by-channel signal generation progress
4. ✅ Three visualization plots:
   - Full 60-second SEEG recording (12 channels)
   - Seizure onset detail (zoomed view of EZ/PZ/NIZ)
   - Power Spectral Density comparison
5. ✅ "Datos guardados en 'seeg_simulado.npz'"

## ❓ Troubleshooting

### Issue: "No module named 'scipy'"
**Solution:** Install in PyCharm terminal:
```bash
pip install scipy
```

### Issue: Plots not showing
**Solution:** Add this at the top of a cell:
```python
%matplotlib inline
```

### Issue: Kernel not starting
**Solution:**
```bash
pip install ipykernel
python -m ipykernel install --user --name=competencias
```
Then restart PyCharm and select the "competencias" kernel.

### Issue: "ModuleNotFoundError: No module named 'numpy'"
**Solution:** Make sure you're using the **venv** interpreter:
- Bottom-right corner of PyCharm → Check Python version
- Should show: `Python 3.x (competencias)`

## 🎯 Verification Checklist

Before running the notebook, verify:
- [x] Notebook copied to your project folder
- [x] Virtual environment created and activated
- [x] Packages installed (`pip list` shows numpy, scipy, matplotlib, jupyter)
- [x] PyCharm recognizes Jupyter (can open .ipynb files)
- [x] Python interpreter set to project venv

## 🚀 Next Steps After Step 1 Works

Once you successfully run Step 1 and see the plots:
1. Share the visualizations (screenshot the plots)
2. Review the comments in each cell to understand the concepts
3. Ask any questions about the signal generation or math behind it
4. I'll provide **Step 2** (Time-frequency analysis + Epileptogenicity Index)

---

**Need help?** Share your screen or error messages and I'll guide you through!
