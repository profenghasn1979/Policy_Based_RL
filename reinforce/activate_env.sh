#!/bin/bash
# Activation script for REINFORCE virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate the virtual environment
source "$SCRIPT_DIR/reinforce_env/bin/activate"

echo "🚀 REINFORCE virtual environment activated!"
echo ""
echo "📦 Installed packages:"
echo "  • PyTorch $(python -c "import torch; print(torch.__version__)")"
echo "  • Gymnasium $(python -c "import gymnasium; print(gymnasium.__version__)")"
echo "  • Matplotlib, Jupyter, JSAnimation, ProgressBar2"
echo ""
echo "📓 To run the notebooks:"
echo "  jupyter notebook REINFORCE.ipynb"
echo "  jupyter notebook pong-REINFORCE.ipynb"
echo ""
echo "📋 To deactivate when done:"
echo "  deactivate"