import streamlit as st

# Set page config for a better look
st.set_page_config(page_title="DRL HW1-1: Grid Map", layout="centered")

# Aggressive and robust CSS to force premium dark theme and square grid
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
        padding: 0.5rem 1rem !important;
    }

    /* Grid Buttons styling */
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
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
    }

    /* Target specific cell colors by their content S, E, X */
    /* Note: Streamlit buttons often wrap the text in a p tag or similar */
    button:has(div p:contains("S")) {
        background-color: #22c55e !important;
        color: white !important;
        box-shadow: 0 0 15px #22c55e !important;
    }
    button:has(div p:contains("E")) {
        background-color: #ef4444 !important;
        color: white !important;
        box-shadow: 0 0 15px #ef4444 !important;
    }
    button:has(div p:contains("X")) {
        background-color: #64748b !important;
        color: white !important;
        box-shadow: 0 0 10px #64748b !important;
    }
    
    /* Mode buttons - Primary type coloring */
    div[data-testid="stColumn"] button[kind="primary"] {
        background-color: #38bdf8 !important;
        color: white !important;
        box-shadow: 0 0 15px #38bdf8 !important;
        border-color: #38bdf8 !important;
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

# Reset obstacles if n changes significantly (optional logic improvement)
# st.session_state.obstacles = {o for o in st.session_state.obstacles if o < n*n}

# Mode Selection
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("SET START", key="mode_start", use_container_width=True, 
                 type="primary" if st.session_state.mode == "Start" else "secondary"):
        st.session_state.mode = "Start"
with col2:
    if st.button("SET END", key="mode_end", use_container_width=True, 
                 type="primary" if st.session_state.mode == "End" else "secondary"):
        st.session_state.mode = "End"
with col3:
    if st.button("SET OBSTACLES", key="mode_obs", use_container_width=True, 
                 type="primary" if st.session_state.mode == "Obstacle" else "secondary"):
        st.session_state.mode = "Obstacle"

st.info(f"📍 Mode: **{st.session_state.mode}** | 🚧 Obstacles: **{len(st.session_state.obstacles)} / {obs_limit}**")

# Grid Logic
def handle_click(idx):
    # Check if we are clicking a cell that is already something
    is_start = idx == st.session_state.start_cell
    is_end = idx == st.session_state.end_cell
    is_obs = idx in st.session_state.obstacles

    # If it's already what the current mode is, we REMOVE it (toggle off)
    if (st.session_state.mode == "Start" and is_start) or \
       (st.session_state.mode == "End" and is_end) or \
       (st.session_state.mode == "Obstacle" and is_obs):
        if is_start: st.session_state.start_cell = None
        if is_end: st.session_state.end_cell = None
        if is_obs: st.session_state.obstacles.remove(idx)
        return

    # Otherwise, clear its existing state and apply the new one
    if is_start: st.session_state.start_cell = None
    if is_end: st.session_state.end_cell = None
    if is_obs: st.session_state.obstacles.remove(idx)

    if st.session_state.mode == "Start":
        st.session_state.start_cell = idx
    elif st.session_state.mode == "End":
        st.session_state.end_cell = idx
    elif st.session_state.mode == "Obstacle":
        if len(st.session_state.obstacles) < obs_limit:
            st.session_state.obstacles.add(idx)
        else:
            st.toast(f"Limit Reached: Max {obs_limit} obstacles!", icon="⚠️")

# Draw Grid
grid_container = st.container()
with grid_container:
    for r in range(n):
        cols = st.columns(n, gap="small")
        for c in range(n):
            idx = r * n + c
            
            label = " "
            if idx == st.session_state.start_cell: label = "S"
            elif idx == st.session_state.end_cell: label = "E"
            elif idx in st.session_state.obstacles: label = "X"
                
            if cols[c].button(label, key=f"cell_{idx}", use_container_width=True):
                handle_click(idx)
                st.rerun()

if st.button("RESET MAP", use_container_width=True):
    st.session_state.start_cell = None
    st.session_state.end_cell = None
    st.session_state.obstacles = set()
    st.rerun()

st.markdown("---")
st.caption("Instructions: Click to toggle elements. Max $n-2$ obstacles. S=Start, E=End, X=Obstacle.")
