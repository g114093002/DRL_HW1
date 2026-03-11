# HW1: GridWorld

This repository contains the complete implementation for **Deep Reinforcement Learning HW1: GridWorld Development**, encompassing both HW1-1 (Grid Map Construction) and HW1-2 (Policy Display and Value Evaluation).

The application is built with a premium, responsive dark theme and deployed seamlessly on **Streamlit**.

🌍 **Live Demo:** [Streamlit Cloud App](https://drlhw1-ctsrpnmdrajmvdjlrybwz9.streamlit.app/)

## 🚀 Features

### HW1-1: Grid Map Construction
- **Dynamic Grid Sizing**: Interactively adjust the grid dimension $n \times n$ where $n \in [5, 9]$ using a smooth slider.
- **Interactive Element Placement**:
  - **Start (S)**: Click to place the starting position (Glowing Green).
  - **End (E)**: Click to place the target destination (Glowing Red).
  - **Obstacles (X)**: Click to place up to **$n-2$** obstacles (Minimalist Gray). Built-in logic prevents exceeding this limit.
- **Toggle & Reset Mechanics**: Clicking an existing element removes it. A dedicated "Reset Map" button clears the entire board instantly.
- **Premium UI/UX**: Features a glassmorphism card design, radial gradient backgrounds, hover animations, and a unified global dark theme that eliminates native Streamlit borders.

### HW1-2: Policy Display and Value Evaluation Evaluator
- **Random Policy Generation**: Click `🎲 1. Random Policy` to visualize a randomly generated policy. The system assigns a random action (↑, ↓, ←, →) to every navigable cell and displays it on the grid.
- **Policy Evaluation V(s)**: Click `🧮 2. Evaluate V(s)` to run standard Policy Evaluation on the random policy. The grid switches to the **Value Matrix** view, displaying the iteratively calculated expected returns $V(s)$ for each state.
- **Policy Optimization V*(s)**: Click `🎯 2. Evaluate V(s)` (Optimized) to execute **Value Iteration**. This algorithm definitively solves the Markov Decision Process (MDP), converging to the optimal policy where the **End (E)** state acts as the absolute maximal target ($V=0.0$, surrounding $V=10.0$).
- **Multi-View Toggles**: Clean radio buttons allow instant, zero-latency switching between:
  - `🗺️ Map`: The base grid editor.
  - `🧭 Policy`: The current directional action arrows.
  - `📊 Value`: The numerical Value Matrix (rounded to 2 decimal places).
- **Core RL Parameters Used (V*(s))**:
  - Discount Factor ($\gamma$): `0.9`
  - Step Reward: `-1`
  - Goal Reward: `+10`
  - Convergence Threshold ($\theta$): `1e-4`

## 🛠️ Technology Stack
- **Frontend / Graphics**: HTML5, Vanilla CSS3, Vanilla JavaScript (embedded via Streamlit components for zero-latency RL computation).
- **Deployment Platform**: Streamlit (`streamlit.components.v1.html`)
- **Backend**: Python 3.x

## 💻 Installation & Local Execution

1. **Clone the repository**:
   ```bash
   git clone https://github.com/g114093002/DRL_HW1.git
   cd DRL_HW1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

## 📸 Screenshots

### The Unified Premium Grid Editor (HW1-1)
*Interactive map builder with glowing state markers.*

### The Optimized Value Matrix (HW1-2 Value Iteration)
*Convergent gradient values leading directly to the End goal.*

## 👤 Author
**[g114093002](https://github.com/g114093002)**
