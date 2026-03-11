import streamlit as st

# Set page config for a better look
st.set_page_config(page_title="DRL HW1-1: Grid Map", layout="centered")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        height: 50px;
        border-radius: 8px;
        font-weight: bold;
    }
    .grid-start { background-color: #22c55e !important; color: white !important; box-shadow: 0 0 10px #22c55e; }
    .grid-end { background-color: #ef4444 !important; color: white !important; box-shadow: 0 0 10px #ef4444; }
    .grid-obstacle { background-color: #64748b !important; color: white !important; }
    .grid-empty { background-color: #334155 !important; color: #94a3b8 !important; }
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

# Mode Selection
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Set Start", type="primary" if st.session_state.mode == "Start" else "secondary"):
        st.session_state.mode = "Start"
with col2:
    if st.button("Set End", type="primary" if st.session_state.mode == "End" else "secondary"):
        st.session_state.mode = "End"
with col3:
    if st.button("Set Obstacles", type="primary" if st.session_state.mode == "Obstacle" else "secondary"):
        st.session_state.mode = "Obstacle"

st.info(f"Mode: **{st.session_state.mode}** | Obstacles: **{len(st.session_state.obstacles)} / {obs_limit}**")

# Grid Logic
def handle_click(idx):
    # Remove from other states if it exists there
    if idx == st.session_state.start_cell:
        st.session_state.start_cell = None
    if idx == st.session_state.end_cell:
        st.session_state.end_cell = None
    if idx in st.session_state.obstacles:
        st.session_state.obstacles.remove(idx)

    if st.session_state.mode == "Start":
        st.session_state.start_cell = idx
    elif st.session_state.mode == "End":
        st.session_state.end_cell = idx
    elif st.session_state.mode == "Obstacle":
        if len(st.session_state.obstacles) < obs_limit:
            st.session_state.obstacles.add(idx)
        else:
            st.warning(f"Maximum {obs_limit} obstacles allowed!")

# Draw Grid
for r in range(n):
    cols = st.columns(n)
    for c in range(n):
        idx = r * n + c
        
        label = ""
        css_class = "grid-empty"
        
        if idx == st.session_state.start_cell:
            label = "S"
            css_class = "grid-start"
        elif idx == st.session_state.end_cell:
            label = "E"
            css_class = "grid-end"
        elif idx in st.session_state.obstacles:
            label = "X"
            css_class = "grid-obstacle"
            
        # Use a button for each cell
        # Streamlit doesn't support direct CSS class injection on buttons easily without hacks, 
        # so we use conditional rendering or container styling.
        # For simplicity and "wow" factor, we'll use a unique key and st.button logic.
        
        button_type = "secondary"
        if idx == st.session_state.start_cell or idx == st.session_state.end_cell or idx in st.session_state.obstacles:
            button_type = "primary"
            
        if cols[c].button(label if label else " ", key=f"cell_{idx}"):
            handle_click(idx)
            st.rerun()

st.markdown("---")
st.caption("Click cells to place elements based on active mode. S = Start, E = End, X = Obstacle.")
