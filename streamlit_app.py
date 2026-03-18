import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DRL HW1-2: Grid Map RL", layout="centered")

# Global CSS to unify background and remove Streamlit artifacts
st.markdown("""
<style>
    /* Force main app background to match our dark theme */
    [data-testid="stAppViewContainer"] {
        background-color: #0f172a !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.15) 0, transparent 50%), 
            radial-gradient(at 50% 0%, rgba(129, 140, 248, 0.1) 0, transparent 50%) !important;
        color: #f1f5f9 !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Remove padding and make the content center naturally */
    .block-container {
        padding: 0 !important;
        max-width: none !important;
        display: flex;
        justify-content: center;
    }

    /* Hide Streamlit footer and menu for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Embed the complete HTML/JS Web App
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: transparent; 
            --card-bg: rgba(30, 41, 59, 0.7);
            --accent-color: #38bdf8;
            --text-color: #f1f5f9;
            --grid-bg: #1e293b;
            --start-color: #22c55e;
            --end-color: #ef4444;
            --obstacle-color: #64748b;
            --empty-color: #334155;
            --policy-color: #818cf8;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            margin: 0;
            padding-top: 40px;
            overflow: hidden; 
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 1.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            text-align: center;
            max-width: 650px;
            width: 95%;
            animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
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
            border-color: var(--accent-color);
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

        /* RL Action Buttons */
        .action-container {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 0.5rem;
            flex-wrap: wrap;
        }
        .btn-action {
            background: #4f46e5;
            color: white !important;
            border-color: transparent;
            font-size: 0.9rem;
            padding: 0.5rem 1rem;
        }
        .btn-action:hover {
            background: #4338ca;
            box-shadow: 0 0 15px rgba(79, 70, 229, 0.6);
        }
        .btn-evaluate {
            background: #10b981;
        }
        .btn-evaluate:hover {
            background: #059669;
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.6);
        }
        .btn-optimize {
            background: #0ea5e9;
        }
        .btn-optimize:hover {
            background: #0284c7;
            box-shadow: 0 0 15px rgba(14, 165, 233, 0.6);
        }

        /* View Toggles */
        .view-toggles {
            display: flex;
            gap: 1rem;
            justify-content: center;
            align-items: center;
            margin-top: 0.5rem;
            background: rgba(0, 0, 0, 0.2);
            padding: 0.8rem 1rem;
            border-radius: 0.8rem;
        }
        .view-toggles label {
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-weight: 600;
            color: #cbd5e1;
            transition: color 0.2s;
        }
        .view-toggles label:hover {
            color: white;
        }
        .view-toggles input[type="radio"] {
            accent-color: var(--accent-color);
            transform: scale(1.2);
            cursor: pointer;
        }

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
            user-select: none;
            position: relative;
        }

        .cell:hover {
            transform: scale(1.1);
            z-index: 10;
            border-color: var(--accent-color);
            background-color: #475569;
        }

        .cell.start { background-color: var(--start-color); box-shadow: 0 0 15px var(--start-color); border: none; }
        .cell.end { background-color: var(--end-color); box-shadow: 0 0 15px var(--end-color); border: none; }
        .cell.obstacle { background-color: var(--obstacle-color); box-shadow: 0 0 10px var(--obstacle-color); border: none; }

        .cell.policy-view {
            font-size: 1.8rem;
            font-weight: 400;
            color: #94a3b8;
            background-color: rgba(255, 255, 255, 0.05);
        }

        .cell.optimal-path {
            background-color: #4ade80 !important;
            color: #0f172a !important;
            font-weight: 800 !important;
            border-color: #22c55e !important;
            box-shadow: 0 0 10px rgba(74, 222, 128, 0.4);
        }
        
        .cell.value-view {
            font-size: 0.85rem;
            font-weight: 600;
            color: #f1f5f9;
            background-color: rgba(56, 189, 248, 0.1);
            border: 1px solid rgba(56, 189, 248, 0.3);
        }

        .info {
            margin-top: 1rem;
            font-size: 0.95rem;
            color: #94a3b8;
        }
        
        #obs-count { font-weight: 800; color: var(--accent-color); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Grid Map & RL Evaluator</h1>
        
        <div class="controls">
            <div class="slider-container">
                <label>Dimension (n): <span id="n-val" style="color: var(--accent-color); font-weight: 800;">7</span></label>
                <input type="range" id="grid-size" min="5" max="9" value="7">
            </div>

            <div class="mode-selector">
                <button class="btn btn-start active" onclick="setMode('start')">Set Start (S)</button>
                <button class="btn btn-end" onclick="setMode('end')">Set End (E)</button>
                <button class="btn btn-obstacle" onclick="setMode('obstacle')">Set Obstacles (X)</button>
                <button class="btn btn-reset" onclick="resetGrid()">Reset Map</button>
            </div>
            
            <div class="info" style="margin-top: 0;">
                Obstacles: <span id="obs-count">0</span> / <span id="obs-limit">5</span>
            </div>

            <div class="action-container">
                <button class="btn btn-action" onclick="generateRandomPolicy()">🎲 1. Random Policy</button>
                <button class="btn btn-action btn-evaluate" onclick="evaluatePolicy()">🎯 2. Evaluate Policy</button>
                <button class="btn btn-action btn-optimize" onclick="optimizePolicy()">✨ 3. Value Iteration</button>
            </div>

            <div class="view-toggles">
                <label><input type="radio" name="view" value="map" checked onchange="changeView('map')"> 🗺️ Map</label>
                <label><input type="radio" name="view" value="policy" onchange="changeView('policy')"> 🧭 Policy</label>
                <label><input type="radio" name="view" value="value" onchange="changeView('value')"> 📊 Value</label>
            </div>
        </div>

        <div id="grid" class="grid"></div>
        <p class="info" id="status-text" style="color: var(--accent-color);">Instructions: Design your map, generate a random policy, evaluate it, or run Value Iteration.</p>
    </div>

    <script>
        let n = 7;
        let mode = 'start';
        let startCell = null;
        let endCell = null;
        let obstacles = new Set();
        
        let policy = {};
        let values = {};
        let optimalPath = new Set();
        let displayMode = 'map'; // 'map', 'policy', 'value'

        const directions = ['↑', '↓', '←', '→'];
        const dr = [-1, 1, 0, 0];
        const dc = [0, 0, -1, 1];

        const gridEl = document.getElementById('grid');
        const sizeInput = document.getElementById('grid-size');
        const nValEl = document.getElementById('n-val');
        const obsCountEl = document.getElementById('obs-count');
        const obsLimitEl = document.getElementById('obs-limit');
        const modeButtons = document.querySelectorAll('.mode-selector .btn');
        const statusText = document.getElementById('status-text');

        function initGrid() {
            n = parseInt(sizeInput.value);
            nValEl.innerText = n;
            obsLimitEl.innerText = n - 2;
            
            resetGrid();
        }

        function resetGrid() {
            startCell = null;
            endCell = null;
            obstacles.clear();
            policy = {};
            values = {};
            optimalPath.clear();
            document.querySelector(`input[value="map"]`).checked = true;
            displayMode = 'map';
            statusText.innerText = "Instructions: Click cells to place S/E/X. Then evaluate.";
            statusText.style.color = 'var(--text-color)';
            renderGrid();
        }
        
        function changeView(newMode) {
            displayMode = newMode;
            renderGrid();
        }

        function generateRandomPolicy() {
            policy = {};
            optimalPath.clear();
            for (let i = 0; i < n * n; i++) {
                if (!obstacles.has(i) && i !== endCell) {
                    policy[i] = Math.floor(Math.random() * 4);
                }
            }
            document.querySelector(`input[value="policy"]`).checked = true;
            changeView('policy');
            statusText.innerText = "Status: Random Policy Generated.";
            statusText.style.color = 'var(--accent-color)';
        }

        function evaluatePolicy() {
            if (Object.keys(policy).length === 0) {
                generateRandomPolicy(); // Auto-generate if not present
            }

            // Init values
            for (let i = 0; i < n * n; i++) {
                values[i] = 0.0;
            }

            // --- RL Parameters ---
            const gamma = 0.9;
            const stepReward = -1;
            const goalReward = 10;
            const theta = 1e-4;

            let delta = 1;
            let iterations = 0;
            
            while (delta > theta && iterations < 2000) {
                delta = 0;
                let newValues = {...values};

                for (let i = 0; i < n * n; i++) {
                    if (obstacles.has(i)) continue;
                    
                    if (i === endCell) {
                        newValues[i] = 0.0;
                        continue;
                    }

                    let act = policy[i];
                    if (act === undefined) {
                        act = Math.floor(Math.random() * 4);
                        policy[i] = act;
                    }

                    let r = Math.floor(i / n);
                    let c = i % n;
                    let nr = r + dr[act];
                    let nc = c + dc[act];
                    let next_i = nr * n + nc;

                    if (nr < 0 || nr >= n || nc < 0 || nc >= n || obstacles.has(next_i)) {
                        next_i = i; 
                    }

                    let reward = stepReward;
                    if (next_i === endCell) {
                        reward = goalReward;
                    }

                    let v = reward + gamma * values[next_i];
                    delta = Math.max(delta, Math.abs(v - values[i]));
                    newValues[i] = v;
                }
                values = newValues;
                iterations++;
            }
            
            computeOptimalPath();
            document.querySelector(`input[value="value"]`).checked = true;
            changeView('value');
            statusText.innerText = `Status: Policy Evaluated in ${iterations} iters. (Values might be low if actions are random).`;
            statusText.style.color = '#f59e0b'; // warning color
        }

        function optimizePolicy() {
            // Value Iteration
            for (let i = 0; i < n * n; i++) values[i] = 0.0;

            const gamma = 0.9;
            const stepReward = -1;
            const goalReward = 10;
            const theta = 1e-4;

            let delta = 1;
            let iterations = 0;
            
            while (delta > theta && iterations < 2000) {
                delta = 0;
                let newValues = {...values};

                for (let i = 0; i < n * n; i++) {
                    if (obstacles.has(i)) continue;
                    
                    if (i === endCell) {
                        newValues[i] = 0.0;
                        continue;
                    }

                    let max_v = -Infinity;
                    let best_act = 0;
                    
                    let r = Math.floor(i / n);
                    let c = i % n;

                    for (let act = 0; act < 4; act++) {
                        let nr = r + dr[act];
                        let nc = c + dc[act];
                        let next_i = nr * n + nc;

                        if (nr < 0 || nr >= n || nc < 0 || nc >= n || obstacles.has(next_i)) {
                            next_i = i;
                        }

                        let reward = stepReward;
                        if (next_i === endCell) {
                            reward = goalReward;
                        }

                        let v = reward + gamma * values[next_i];
                        if (v > max_v) {
                            max_v = v;
                            best_act = act;
                        }
                    }

                    delta = Math.max(delta, Math.abs(max_v - values[i]));
                    newValues[i] = max_v;
                    policy[i] = best_act; // Update to greedy policy
                }
                values = newValues;
                iterations++;
            }
            
            computeOptimalPath();
            document.querySelector(`input[value="policy"]`).checked = true;
            changeView('policy');
            statusText.innerText = `Status: Optimal Policy Found! V*(s) converged in ${iterations} operations. Displaying optimal paths.`;
            statusText.style.color = '#22c55e'; // success color
        }

        function computeOptimalPath() {
            optimalPath.clear();
            if (startCell === null || endCell === null) return;
            
            let current = startCell;
            let visited = new Set();
            
            while (current !== endCell) {
                if (visited.has(current)) break; // prevent infinite loops
                
                let act = policy[current];
                if (act === undefined) break;
                
                optimalPath.add(current);
                visited.add(current);
                
                let r = Math.floor(current / n);
                let c = current % n;
                let nr = r + dr[act];
                let nc = c + dc[act];
                
                let next_i = nr * n + nc;
                if (nr < 0 || nr >= n || nc < 0 || nc >= n || obstacles.has(next_i)) {
                    break;
                }
                current = next_i;
            }
            if (current === endCell) {
                optimalPath.add(current);
            }
        }

        function renderGrid() {
            gridEl.style.gridTemplateColumns = `repeat(${n}, 50px)`;
            gridEl.innerHTML = '';
            
            for (let i = 0; i < n * n; i++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                
                if (displayMode === 'map') {
                    if (i === startCell) { cell.classList.add('start'); cell.innerText = 'S'; }
                    else if (i === endCell) { cell.classList.add('end'); cell.innerText = 'E'; }
                    else if (obstacles.has(i)) { cell.classList.add('obstacle'); cell.innerText = 'X'; }
                } 
                else if (displayMode === 'policy') {
                    if (obstacles.has(i)) { 
                        cell.classList.add('obstacle'); 
                    } else {
                        cell.classList.add('policy-view');
                        if (optimalPath.has(i)) {
                            cell.classList.add('optimal-path');
                        }
                        
                        let content = '';
                        if (i === startCell) {
                            content += '<div style="font-size: 0.45rem; position: absolute; top: 4px; left: 4px; font-weight: 800; color: inherit;">START</div>';
                        }
                        
                        if (i in policy) {
                            content += `<span>${directions[policy[i]]}</span>`;
                        } else if (i === endCell) {
                            content += `<span>E</span>`;
                        } else {
                            content += `<span>-</span>`;
                        }
                        
                        if (i === endCell) {
                            content += '<div style="font-size: 0.45rem; position: absolute; bottom: 4px; right: 4px; font-weight: 800; color: inherit;">END</div>';
                        }
                        
                        cell.innerHTML = content;
                    }
                } 
                else if (displayMode === 'value') {
                    if (obstacles.has(i)) { cell.classList.add('obstacle'); }
                    else if (i === endCell) { 
                        cell.classList.add('end'); 
                        cell.innerText = '0.0'; 
                    }
                    else {
                        cell.classList.add('value-view');
                        if (i in values) {
                            cell.innerText = values[i].toFixed(2);
                            if (i === startCell) cell.style.color = 'var(--start-color)';
                        }
                    }
                }
                
                cell.onclick = () => {
                    if (displayMode !== 'map') {
                        document.querySelector(`input[value="map"]`).checked = true;
                        changeView('map');
                    }
                    handleCellClick(i);
                };
                gridEl.appendChild(cell);
            }
            updateStats();
        }

        function setMode(newMode) {
            mode = newMode;
            modeButtons.forEach(btn => btn.classList.remove('active'));
            if (newMode !== 'reset') {
                const activeBtn = document.querySelector(`.btn-${newMode}`);
                if (activeBtn) activeBtn.classList.add('active');
            }
            if (displayMode !== 'map') {
                document.querySelector(`input[value="map"]`).checked = true;
                changeView('map');
            }
        }

        function handleCellClick(index) {
            if (index === startCell) startCell = null;
            else if (index === endCell) endCell = null;
            else if (obstacles.has(index)) obstacles.delete(index);
            else {
                if (mode === 'start') {
                    startCell = index;
                } else if (mode === 'end') {
                    endCell = index;
                } else if (mode === 'obstacle') {
                    if (obstacles.size < (n - 2)) {
                        obstacles.add(index);
                    } else {
                        alert(`Maximum ${n - 2} obstacles allowed!`);
                    }
                }
            }
            
            // Clear evaluation results on edit
            policy = {};
            values = {};
            optimalPath.clear();
            statusText.innerText = "Status: Map modified. Please re-generate policy and evaluate.";
            statusText.style.color = 'var(--text-color)';

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

# Render the component with no borders and increased height for extra UI
components.html(html_content, height=1000, scrolling=False)
