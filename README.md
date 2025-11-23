# Policy-Based Reinforcement Learning

This repository contains implementations of policy-based reinforcement learning algorithms, focusing on the REINFORCE algorithm applied to Atari Pong.

## 🎯 Project Overview

This project demonstrates policy gradient methods in reinforcement learning, specifically:
- **REINFORCE Algorithm**: Vanilla policy gradient method
- **Parallel Environment Training**: Multiple Pong environments for efficient learning
- **Neural Network Policy**: Deep learning approach to policy approximation

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Virtual environment support

### Quick Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/profenghasn/Policy_Based_RL.git
   cd Policy_Based_RL
   ```

2. Set up the environment:
   ```bash
   cd reinforce
   chmod +x activate_env.sh
   ./activate_env.sh
   ```

3. Launch Jupyter and run the notebook:
   ```bash
   jupyter notebook pong-REINFORCE.ipynb
   ```

## 📁 Project Structure

```
reinforce/
├── pong-REINFORCE.ipynb    # Main training notebook (streamlined)
├── REINFORCE.ipynb         # Original full notebook
├── pong_utils.py           # REINFORCE utilities and neural network
├── parallelEnv.py          # Parallel environment wrapper
├── requirements.txt        # Dependencies
├── activate_env.sh         # Environment setup script
└── README.md              # Detailed documentation
```

## 🎮 What You'll Learn

- **Policy Gradients**: How REINFORCE learns through trial and error
- **Parallel Training**: Efficient RL training with multiple environments
- **Deep RL**: Neural network policies for complex state spaces
- **Atari Games**: Classic RL benchmark with visual observations

## 📊 Results

The trained agent achieves:
- **Performance**: ~-11.4 average reward (vs ~-21 random)
- **Training Time**: ~15 minutes for 500 episodes
- **Improvement**: 46% better than random policy

## 🛠 Technical Details

- **Algorithm**: REINFORCE with baseline
- **Environment**: Atari Pong via Gymnasium
- **Network**: CNN + FC layers for visual processing
- **Optimization**: Adam optimizer with policy gradients

## 🔧 Key Features

- ✅ Modern Gymnasium API compatibility
- ✅ Parallel environment training
- ✅ Progress visualization and monitoring
- ✅ Model saving and testing framework
- ✅ Clean, educational code structure

## 📈 Training Progress

The notebook includes visualization of:
- Episode rewards over time
- Smoothed performance trends
- Training statistics and metrics

## 🎯 Next Steps

- Experiment with different hyperparameters
- Try other Atari games
- Implement Actor-Critic methods
- Add advanced policy gradient techniques

## 📚 References

- [Sutton & Barto - Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book.html)
- [Policy Gradient Methods](https://papers.nips.cc/paper/1713-policy-gradient-methods-for-reinforcement-learning-with-function-approximation.pdf)
- [REINFORCE Algorithm](https://link.springer.com/article/10.1007/BF00992696)

---

**Happy Learning!** 🚀 This project provides a hands-on introduction to policy-based reinforcement learning with practical, working code.