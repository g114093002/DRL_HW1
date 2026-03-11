import streamlit as st

# Set page config for a better look
st.set_page_config(page_title="DRL HW1-1: Grid Map", layout="centered")

# Aggressive CSS to force premium dark theme and square grid
st.markdown("""
<style>
    /* Dark Theme Background */
    [data-testid="stAppViewContainer"] {
        background-color: #0f172a;
        background-image: 
            radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.15) 0, transparent 50%), 
            radial-gradient(at 50% 0%, rgba(129, 140, 248, 0.1) 0, transparent 50%);
    }
    
    [data-testid="stHeader"] { background: transparent; }

    /* Hide default Streamlit padding */
    .block-container {
        padding-top: 2rem !important;
        max-width: 600px !important;
    }

    h1 {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800 !important;
    }

    /* Selection Modes Info */
    .stInfo {
        background-color: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f1f5f9 !important;
    }

    /* Force Grid Buttons to be Square and Dark */
    .stButton>button {
        aspect-ratio: 1 / 1;
        width: 100% !important;
        height: auto !important;
        min-height: 0px !important;
        padding: 0 !important;
        margin: 0 !important;
        font-size: 1.2rem !important;
        border-radius: 4px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background-color: #334155 !important;
        color: #94a3b8 !important;
        transition: all 0.2s !important;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        border-color: #38bdf8 !important;
    }

    /* Specialized Cell Colors */
    /* We use the key to target buttons specifically if possible, 
       but for Streamlit we'll rely on our python logic and primary/secondary types */
    
    /* Primary buttons are used for Start/End/Obstacles */
    div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        box-shadow: 0 0 15px currentColor;
    }
    
    /* Column gaps */
    div[data-testid="stColumn"] {
        padding: 1px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Grid Map Developer")

# Initialize session state
if 'start_cell' not in st.session_state:
    st.session_state.start_cell = None
if 'end_cell' not in st.session_state:
    st.session_state.end_cell = None
if 'obstacles' not in st.session_state:
    st.session_state.obstacles = set()
if 'mode' not in st.session_state:
    st.session_state.mode = "Start"

# Dimensions
n = st.slider("Dimension (n)", 5, 9, 7)
obs_limit = n - 2

# Reset obstacles if n changes and exceeds limit
if len(st.session_state.obstacles) > obs_limit:
    st.session_state.obstacles = set()

# Mode Selection
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Set Start", key="mode_start", use_container_width=True, 
                 type="primary" if st.session_state.mode == "Start" else "secondary"):
        st.session_state.mode = "Start"
with col2:
    if st.button("Set End", key="mode_end", use_container_width=True, 
                 type="primary" if st.session_state.mode == "End" else "secondary"):
        st.session_state.mode = "End"
with col3:
    if st.button("Set Obstacles", key="mode_obs", use_container_width=True, 
                 type="primary" if st.session_state.mode == "Obstacle" else "secondary"):
        st.session_state.mode = "Obstacle"

st.info(f"📍 Mode: **{st.session_state.mode}** | 🚧 Obstacles: **{len(st.session_state.obstacles)} / {obs_limit}**")

# Grid Logic
def handle_click(idx):
    if idx == st.session_state.start_cell:
        st.session_state.start_cell = None
    elif idx == st.session_state.end_cell:
        st.session_state.end_cell = None
    elif idx in st.session_state.obstacles:
        st.session_state.obstacles.remove(idx)
    else:
        if st.session_state.mode == "Start":
            st.session_state.start_cell = idx
        elif st.session_state.mode == "End":
            st.session_state.end_cell = idx
        elif st.session_state.mode == "Obstacle":
            if len(st.session_state.obstacles) < obs_limit:
                st.session_state.obstacles.add(idx)
            else:
                st.toast(f"Limit Reached: Max {obs_limit} obstacles!", icon="⚠️")

# Injection of cell-specific CSS (Hack for dynamic colors in Streamlit)
color_css = "<style>"
if st.session_state.start_cell is not None:
    color_css += f'div[data-testid="stColumn"] button[key="cell_{st.session_state.start_cell}"] {{ background-color: #22c55e !important; color: white !important; }}'
if st.session_state.end_cell is not None:
    color_css += f'div[data-testid="stColumn"] button[key="cell_{st.session_state.end_cell}"] {{ background-color: #ef4444 !important; color: white !important; }}'
for obs in st.session_state.obstacles:
    color_css += f'div[data-testid="stColumn"] button[key="cell_{obs}"] {{ background-color: #64748b !important; color: white !important; }}'
color_css += "</style>"
st.markdown(color_css, unsafe_allow_html=True)

# Draw Grid
grid_container = st.container()
with grid_container:
    for r in range(n):
        cols = st.columns(n, gap="small")
        for c in range(n):
            idx = r * n + c
            
            label = ""
            btn_type = "secondary"
            
            if idx == st.session_state.start_cell:
                label = "S"
                btn_type = "primary"
            elif idx == st.session_state.end_cell:
                label = "E"
                btn_type = "primary"
            elif idx in st.session_state.obstacles:
                label = "X"
                btn_type = "primary"
                
            if cols[c].button(label if label else " ", key=f"cell_{idx}", use_container_width=True, type=btn_type):
                handle_click(idx)
                st.rerun()

st.markdown("---")
st.caption("Click cells to place elements. S=Start, E=End, X=Obstacle. Grid is restricted to $n-2$ obstacles.")
