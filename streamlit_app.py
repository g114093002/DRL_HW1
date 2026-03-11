import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DRL HW1-1: Grid Map", layout="centered")

# Embed the original Flask UI exactly
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --accent-color: #38bdf8;
            --text-color: #f1f5f9;
            --grid-bg: #1e293b;
            --start-color: #22c55e;
            --end-color: #ef4444;
            --obstacle-color: #64748b;
            --empty-color: #334155;
        }

        body {
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.15) 0, transparent 50%), 
                radial-gradient(at 50% 0%, rgba(129, 140, 248, 0.1) 0, transparent 50%);
            color: var(--text-color);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            margin: 0;
            padding-top: 20px;
            overflow-x: hidden;
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 1.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            text-align: center;
            max-width: 600px;
            width: 90%;
        }

        h1 {
            font-size: 2rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(to right, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }

        .controls {
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .slider-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
        }

        input[type="range"] {
            accent-color: var(--accent-color);
            width: 250px;
        }

        .mode-selector {
            display: flex;
            gap: 0.5rem;
            justify-content: center;
            flex-wrap: wrap;
        }

        .btn {
            padding: 0.6rem 1.2rem;
            border-radius: 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
            background: var(--empty-color);
            color: #94a3b8;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }

        .btn.active {
            color: white;
            border-color: transparent;
        }

        .btn-start.active { background: var(--start-color); box-shadow: 0 0 15px var(--start-color); }
        .btn-end.active { background: var(--end-color); box-shadow: 0 0 15px var(--end-color); }
        .btn-obstacle.active { background: var(--obstacle-color); box-shadow: 0 0 15px var(--obstacle-color); }
        .btn-reset { background: #475569; color: white !important; margin-top: 10px; }
        .btn-reset:hover { background: #64748b; }

        .grid {
            display: grid;
            gap: 8px;
            margin: 0 auto;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 1.5rem;
            width: fit-content;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .cell {
            width: 50px;
            height: 50px;
            background-color: var(--empty-color);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            color: white;
            font-size: 1.2rem;
        }

        .cell:hover {
            transform: scale(1.1);
            z-index: 10;
            border-color: var(--accent-color);
        }

        .cell.start { background-color: var(--start-color); box-shadow: 0 0 20px var(--start-color); border: none; }
        .cell.end { background-color: var(--end-color); box-shadow: 0 0 20px var(--end-color); border: none; }
        .cell.obstacle { background-color: var(--obstacle-color); box-shadow: 0 0 10px var(--obstacle-color); border: none; }

        .info {
            margin-top: 1.5rem;
            font-size: 0.95rem;
            color: #94a3b8;
        }
        
        #obs-count { font-weight: 800; color: var(--accent-color); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Grid Map Developer</h1>
        
        <div class="controls">
            <div class="slider-container">
                <label>Dimension (n): <span id="n-val" style="color: var(--accent-color); font-weight: 800;">7</span></label>
                <input type="range" id="grid-size" min="5" max="9" value="7">
            </div>

            <div class="mode-selector">
                <button class="btn btn-start active" onclick="setMode('start')">Set Start</button>
                <button class="btn btn-end" onclick="setMode('end')">Set End</button>
                <button class="btn btn-obstacle" onclick="setMode('obstacle')">Set Obstacles</button>
                <button class="btn btn-reset" onclick="resetGrid()">Reset Map</button>
            </div>
            
            <div class="info">
                Obstacles: <span id="obs-count">0</span> / <span id="obs-limit">5</span>
            </div>
        </div>

        <div id="grid" class="grid"></div>

        <p class="info">Instructions: Select mode and click grid cells. Max n-2 obstacles.</p>
    </div>

    <script>
        let n = 7;
        let mode = 'start';
        let startCell = null;
        let endCell = null;
        let obstacles = new Set();

        const gridEl = document.getElementById('grid');
        const sizeInput = document.getElementById('grid-size');
        const nValEl = document.getElementById('n-val');
        const obsCountEl = document.getElementById('obs-count');
        const obsLimitEl = document.getElementById('obs-limit');
        const modeButtons = document.querySelectorAll('.mode-selector .btn');

        function initGrid() {
            n = parseInt(sizeInput.value);
            nValEl.innerText = n;
            obsLimitEl.innerText = n - 2;
            
            resetGrid(); // Clear on size change or initial load
        }

        function resetGrid() {
            startCell = null;
            endCell = null;
            obstacles.clear();
            renderGrid();
        }

        function renderGrid() {
            gridEl.style.gridTemplateColumns = `repeat(${n}, 50px)`;
            gridEl.innerHTML = '';
            
            for (let i = 0; i < n * n; i++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                if (i === startCell) { cell.classList.add('start'); cell.innerText = 'S'; }
                else if (i === endCell) { cell.classList.add('end'); cell.innerText = 'E'; }
                else if (obstacles.has(i)) { cell.classList.add('obstacle'); cell.innerText = 'X'; }
                
                cell.onclick = () => handleCellClick(i);
                gridEl.appendChild(cell);
            }
            updateStats();
        }

        function setMode(newMode) {
            mode = newMode;
            modeButtons.forEach(btn => btn.classList.remove('active'));
            if (newMode !== 'reset') {
                document.querySelector(`.btn-${newMode}`).classList.add('active');
            }
        }

        function handleCellClick(index) {
            // Toggle Logic: If clicking the same thing, remove it
            if (index === startCell) startCell = null;
            else if (index === endCell) endCell = null;
            else if (obstacles.has(index)) obstacles.delete(index);
            else {
                // Otherwise clear its previous state and add new
                if (mode === 'start') {
                    startCell = index;
                } else if (mode === 'end') {
                    endCell = index;
                } else if (mode === 'obstacle') {
                    if (obstacles.size < (n - 2)) {
                        obstacles.add(index);
                    } else {
                        alert(`Maximum ${n-2} obstacles allowed!`);
                    }
                }
            }
            renderGrid();
        }

        function updateStats() {
            obsCountEl.innerText = obstacles.size;
        }

        sizeInput.oninput = initGrid;
        initGrid();
    </script>
</body>
</html>
"""

# Render the component
components.html(html_content, height=850, scrolling=True)
