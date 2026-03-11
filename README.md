# Deep Reinforcement Learning HW1-1: Grid Map

This repository contains the implementation for **HW1-1: Grid Map Development**.

## Features
- **Dynamic Dimension**: Choose grid size $n \times n$ where $n \in [5, 9]$.
- **Interactive Selection**:
  - Click to set **Start** cell (Green).
  - Click to set **End** cell (Red).
  - Click to set up to **$n-2$ Obstacles** (Gray).
- **Responsive UI**: Built with Flask and a modern CSS design.

## Installation & Local Execution

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
   - For Flask version: `python app.py`
   - For Streamlit version: `streamlit run streamlit_app.py`

4. **Streamlit Cloud Deployment**: 
   When deploying to Streamlit Cloud, set the **Main file path** to `streamlit_app.py`.

## Deployment to Streamlit
Although developed with Flask, to host on **Streamlit Cloud**, you would typically need a Streamlit version of the code (`streamlit_app.py`). 

> [!NOTE]
> If you strictly need to run a Flask app *inside* Streamlit, you might use `streamlit.components.v1.html`. However, the current code is optimized for standard Flask deployment (e.g., Render, Heroku) or local use.

## Author
[g114093002](https://github.com/g114093002)
