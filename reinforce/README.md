[//]: # (Image References)

[image1]: https://user-images.githubusercontent.com/10624937/42135683-dde5c6f0-7d13-11e8-90b1-8770df3e40cf.gif "Trained Agent"

# REINFORCE

This project implements REINFORCE (Monte Carlo Policy Gradients) algorithm for reinforcement learning tasks.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install 'gymnasium[atari,accept-rom-license]'
pip install ale-py
pip install torch torchvision
pip install numpy matplotlib
pip install cloudpickle
pip install jupyter ipython
pip install JSAnimation
pip install progressbar2
```

### 2. Available Notebooks

- **`REINFORCE.ipynb`**: Implementation of REINFORCE with Gymnasium's CartPole environment
- **`pong-REINFORCE.ipynb`**: REINFORCE implementation for Atari Pong with parallel environments

### 3. Key Files

- **`parallelEnv.py`**: Parallel environment wrapper for training multiple agents simultaneously
- **`pong_utils.py`**: Utility functions for Pong preprocessing, policy network, and training helpers

## Usage

1. Open either notebook in Jupyter:
   ```bash
   jupyter notebook REINFORCE.ipynb
   # or
   jupyter notebook pong-REINFORCE.ipynb
   ```

2. Run the cells sequentially to train the agent

3. Experiment with different hyperparameters to improve training speed and performance!

## Key Changes from Original

- **Updated to Gymnasium**: Migrated from deprecated OpenAI Gym to maintained Gymnasium
- **Fixed API compatibility**: Updated for Gymnasium's new API (reset returns tuple, step returns 5 values)
- **Modern dependencies**: Updated package versions and installation instructions
- **Improved error handling**: Better error messages and dependency checks

## Troubleshooting

- **Atari ROM issues**: Ensure you have `pip install 'gymnasium[atari,accept-rom-license]'` and `ale-py`
- **Import errors**: Install missing dependencies from requirements.txt
- **GPU support**: PyTorch will automatically use CUDA if available

### Results

![Trained Agent][image1]
