#!/bin/bash

# Script to copy Step 1 files to your PyCharm competencias project
# Usage: bash copy_to_pycharm.sh

PYCHARM_PROJECT="/Users/brainseeg/PycharmProjects/competencias"

echo "================================================"
echo "Copying files to PyCharm project..."
echo "================================================"

# Check if PyCharm project directory exists
if [ ! -d "$PYCHARM_PROJECT" ]; then
    echo "❌ Error: PyCharm project directory not found at:"
    echo "   $PYCHARM_PROJECT"
    echo ""
    echo "Please update the PYCHARM_PROJECT variable in this script"
    echo "to match your actual project location."
    exit 1
fi

# Create the directory structure
echo "Creating directory: 12 - Simulacion de Senales EEG"
mkdir -p "$PYCHARM_PROJECT/12 - Simulacion de Senales EEG"

# Copy the notebook
echo "Copying Step1_Simulacion_SEEG.ipynb..."
cp "12 - Simulacion de Senales EEG/Step1_Simulacion_SEEG.ipynb" \
   "$PYCHARM_PROJECT/12 - Simulacion de Senales EEG/"

# Copy the requirements file
echo "Copying requirements.txt..."
cp requirements.txt "$PYCHARM_PROJECT/"

# Copy the setup guide
echo "Copying SETUP_GUIDE.md..."
cp SETUP_GUIDE.md "$PYCHARM_PROJECT/"

echo ""
echo "✅ Files copied successfully!"
echo ""
echo "📁 Files now in your PyCharm project:"
echo "   $PYCHARM_PROJECT/12 - Simulacion de Senales EEG/Step1_Simulacion_SEEG.ipynb"
echo "   $PYCHARM_PROJECT/requirements.txt"
echo "   $PYCHARM_PROJECT/SETUP_GUIDE.md"
echo ""
echo "🚀 Next steps:"
echo "   1. Open PyCharm with the competencias project"
echo "   2. Open Terminal in PyCharm (bottom panel)"
echo "   3. Run: pip install -r requirements.txt"
echo "   4. Open the notebook: 12 - Simulacion de Senales EEG/Step1_Simulacion_SEEG.ipynb"
echo "   5. Click 'Run All' or run cell by cell"
echo ""
echo "================================================"
