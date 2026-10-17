import os
import json

def get_portal_html():
    json_path = os.path.join(os.path.dirname(__file__), "telemetry_data.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            telemetry_json = f.read()
    else:
        telemetry_json = "[]"

    # Supabase credentials (retrieved via environment variable or client config)
    sb_url = os.environ.get("SUPABASE_URL", "https://neeovxcrbsigbnkoimcd.supabase.co")
    sb_key = os.environ.get("SUPABASE_KEY", "")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WardWatch AI - Silent Deterioration Engine</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <style>
        :root {{
            --bg: #ffffff;
            --surface: #ffffff;
            --surface-subtle: #f8fafc;
            --border: #e2e8f0;
            --border-hover: #cbd5e1;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #0284c7;
            --btn-bg: #38bdf8;
            --btn-text: #0c4a6e;
            --btn-hover: #0ea5e9;
            --success-bg: #dcfce7;
            --success-text: #15803d;
            --warning-bg: #fef3c7;
            --warning-text: #b45309;
            --danger-bg: #fee2e2;
            --danger-text: #b91c1c;
            --card-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            --active-shadow: 0 4px 16px rgba(2, 132, 199, 0.18);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }}

        /* Header */
        header {{
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            padding: 12px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .brand-icon {{
            font-size: 1.8rem;
            line-height: 1;
        }}

        .brand-text h1 {{
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: var(--text-main);
        }}

        .brand-text p {{
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 700;
            background: rgba(16, 185, 129, 0.1);
            color: #047857;
            border: 1px solid #a7f3d0;
        }}

        .status-pill .dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 8px #10b981;
            animation: pulse-dot 1.8s infinite;
        }}

        @keyframes pulse-dot {{
            0% {{ transform: scale(0.95); opacity: 0.8; }}
            50% {{ transform: scale(1.2); opacity: 1; }}
            100% {{ transform: scale(0.95); opacity: 0.8; }}
        }}

        /* Light Blue Action Buttons */
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            border: none;
        }}

        .btn-primary {{
            background: var(--btn-bg);
            color: var(--btn-text);
            border: 1px solid #7dd3fc;
            box-shadow: 0 2px 6px rgba(56, 189, 248, 0.25);
        }}

        .btn-primary:hover {{
            background: var(--btn-hover);
            color: #ffffff;
            border-color: #0284c7;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.35);
            transform: translateY(-1px);
        }}

        .btn-danger {{
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fca5a5;
        }}

        .btn-danger:hover {{
            background: #ef4444;
            color: #ffffff;
        }}

        .btn-outline {{
            background: #ffffff;
            color: var(--text-main);
            border: 1px solid var(--border);
        }}

        .btn-outline:hover {{
            background: var(--surface-subtle);
            border-color: var(--border-hover);
        }}

        /* App Container */
        .app-body {{
            max-width: 1440px;
            margin: 0 auto;
            width: 100%;
            padding: 20px 28px 40px 28px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        /* Timeline & Controls Bar */
        .controls-card {{
            background: var(--surface-subtle);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 22px;
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: center;
            justify-content: space-between;
        }}

        .timeline-controls {{
            display: flex;
            align-items: center;
            gap: 14px;
            flex: 1;
            min-width: 340px;
        }}

        .time-badge {{
            font-family: 'JetBrains Mono', monospace;
            background: #ffffff;
            border: 1px solid var(--border);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--primary);
            min-width: 90px;
            text-align: center;
        }}

        .slider-wrapper {{
            flex: 1;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        input[type="range"] {{
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: #cbd5e1;
            outline: none;
            cursor: pointer;
            accent-color: var(--primary);
        }}

        .ward-stats {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .stat-chip {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 5px 12px;
            border-radius: 6px;
            background: #ffffff;
            border: 1px solid var(--border);
        }}

        .chip-critical {{
            background: #fef2f2;
            border-color: #fecaca;
            color: #991b1b;
        }}

        .chip-moderate {{
            background: #fffbeb;
            border-color: #fde68a;
            color: #92400e;
        }}

        .chip-stable {{
            background: #f0fdf4;
            border-color: #bbf7d0;
            color: #166534;
        }}

        /* Floor Grid */
        .grid-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}

        .grid-header h2 {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-main);
        }}

        .bed-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
            gap: 16px;
        }}

        .bed-card {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px 16px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: var(--card-shadow);
            display: flex;
            flex-direction: column;
            gap: 10px;
            position: relative;
        }}

        .bed-card:hover {{
            transform: translateY(-2px);
            border-color: var(--border-hover);
            box-shadow: 0 6px 14px rgba(0, 0, 0, 0.08);
        }}

        .bed-card.active {{
            border: 2px solid var(--primary);
            box-shadow: var(--active-shadow);
            background: #f0f9ff;
        }}

        .bed-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .bed-name {{
            font-size: 0.98rem;
            font-weight: 700;
            color: var(--text-main);
        }}

        .bed-room {{
            font-size: 0.76rem;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
        }}

        .tier-badge {{
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }}

        .tier-low {{ background: var(--success-bg); color: var(--success-text); border: 1px solid #86efac; }}
        .tier-moderate {{ background: var(--warning-bg); color: var(--warning-text); border: 1px solid #fcd34d; }}
        .tier-high {{
            background: var(--danger-bg);
            color: var(--danger-text);
            border: 1px solid #fca5a5;
            animation: pulse-danger 2s infinite;
        }}

        @keyframes pulse-danger {{
            0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.3); }}
            70% {{ box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
        }}

        .patient-info {{
            font-size: 0.8rem;
            color: var(--text-muted);
            line-height: 1.35;
        }}

        .patient-dx {{
            font-weight: 600;
            color: var(--text-main);
        }}

        .vitals-mini-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
            background: #f8fafc;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid #f1f5f9;
        }}

        .vital-mini {{
            text-align: center;
        }}

        .vital-mini .lbl {{
            font-size: 0.65rem;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .vital-mini .val {{
            font-size: 0.85rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-main);
        }}

        /* Selected Patient Deep Dive */
        .patient-drilldown {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 22px 24px;
            box-shadow: var(--card-shadow);
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .drilldown-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 14px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }}

        .drilldown-title h3 {{
            font-size: 1.3rem;
            font-weight: 800;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .drilldown-title p {{
            font-size: 0.86rem;
            color: var(--text-muted);
            margin-top: 4px;
        }}

        .vital-metrics-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
        }}

        .metric-tile {{
            background: var(--surface-subtle);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .metric-tile .label {{
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--text-muted);
            letter-spacing: 0.4px;
        }}

        .metric-tile .value {{
            font-size: 1.4rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-main);
        }}

        .metric-tile .sub {{
            font-size: 0.72rem;
            color: var(--text-muted);
        }}

        /* Plotly Telemetry Section */
        .charts-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
            gap: 18px;
        }}

        .chart-box {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px 14px;
            min-height: 280px;
        }}

        /* SBAR & Interventions */
        .clinical-workflow {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}

        @media (max-width: 960px) {{
            .clinical-workflow {{ grid-template-columns: 1fr; }}
        }}

        .workflow-card {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 20px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}

        .workflow-card h4 {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .sbar-block {{
            background: var(--surface-subtle);
            border-left: 4px solid var(--primary);
            border-radius: 0 8px 8px 0;
            padding: 10px 14px;
            font-size: 0.85rem;
            line-height: 1.45;
        }}

        .sbar-block strong {{
            color: var(--primary);
        }}

        /* Nurse Checklist */
        .checklist {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .check-item {{
            display: flex;
            align-items: flex-start;
            gap: 10px;
            font-size: 0.86rem;
            line-height: 1.35;
        }}

        .check-item input[type="checkbox"] {{
            margin-top: 3px;
            width: 17px;
            height: 17px;
            accent-color: var(--primary);
            cursor: pointer;
        }}

        /* Audit Sign-off Form */
        .audit-form {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 10px;
            padding-top: 12px;
            border-top: 1px solid var(--border);
        }}

        .audit-form input, .audit-form textarea {{
            width: 100%;
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid var(--border);
            font-family: inherit;
            font-size: 0.85rem;
            outline: none;
        }}

        .audit-form input:focus, .audit-form textarea:focus {{
            border-color: var(--primary);
        }}

        /* Audit Stream Expander */
        .audit-stream {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 20px;
        }}

        .audit-stream h4 {{
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 12px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
            text-align: left;
        }}

        th {{
            background: var(--surface-subtle);
            padding: 8px 12px;
            border-bottom: 1px solid var(--border);
            font-weight: 700;
            color: var(--text-muted);
        }}

        td {{
            padding: 8px 12px;
            border-bottom: 1px solid #f1f5f9;
        }}

        /* Toast */
        #toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #0f172a;
            color: #ffffff;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 0.88rem;
            font-weight: 600;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
            pointer-events: none;
            z-index: 9999;
        }}

        #toast.show {{
            opacity: 1;
            transform: translateY(0);
        }}

        footer {{
            text-align: center;
            font-size: 0.78rem;
            color: var(--text-muted);
            padding: 20px;
            border-top: 1px solid var(--border);
            margin-top: auto;
        }}
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <div class="brand-icon">🛡️</div>
            <div class="brand-text">
                <h1>WardWatch AI</h1>
                <p>Silent Deterioration & Early Sepsis Telemetry Surveillance &bull; Unit: 4-East Med-Surg</p>
            </div>
        </div>
        <div class="header-actions">
            <div class="status-pill">
                <span class="dot"></span>
                <span>Real-Time Telemetry Streaming</span>
            </div>
            <button class="btn btn-danger" onclick="triggerRRT()">🚨 Code Sepsis RRT</button>
            <a href="https://share.streamlit.io/deploy?repository=TEAM-NEXORA00/medical-sepsis&branch=main&mainModule=app.py" target="_blank" class="btn btn-outline">
                ☁️ Streamlit Cloud Deploy
            </a>
        </div>
    </header>

    <div class="app-body">
        <!-- Controls Bar -->
        <div class="controls-card">
            <div class="timeline-controls">
                <button class="btn btn-primary" id="btnPlay" onclick="togglePlay()">▶ Live Play</button>
                <button class="btn btn-outline" onclick="stepHour(-1)">◀ -1h</button>
                <div class="slider-wrapper">
                    <input type="range" id="hourSlider" min="1" max="24" value="14" oninput="onHourChange(this.value)">
                </div>
                <button class="btn btn-outline" onclick="stepHour(1)">+1h ▶</button>
                <div class="time-badge" id="timeLabel">T+14:00</div>
            </div>
            <div class="ward-stats">
                <div class="stat-chip chip-critical" id="chipCrit">🚨 2 Critical</div>
                <div class="stat-chip chip-moderate" id="chipMod">⚠️ 2 Elevated</div>
                <div class="stat-chip chip-stable" id="chipStab">🟢 4 Stable</div>
            </div>
        </div>

        <!-- 8-Bed Floor Grid -->
        <div>
            <div class="grid-header">
                <h2>Clinical Telemetry Floor Grid (4-East Unit)</h2>
                <span style="font-size: 0.8rem; color: var(--text-muted);">Click any bed to inspect continuous multi-trajectory vitals</span>
            </div>
            <div class="bed-grid" id="bedGrid"></div>
        </div>

        <!-- Selected Patient Drilldown -->
        <div class="patient-drilldown">
            <div class="drilldown-header">
                <div class="drilldown-title">
                    <h3 id="drillName">Bed 04 - Eleanor Wright (72F)</h3>
                    <p id="drillSub">Acute Pyelonephritis (Occult Sepsis) &bull; Room 402-B &bull; Attending: Dr. S. Reynolds</p>
                </div>
                <div id="drillBadge"></div>
            </div>

            <div class="vital-metrics-row" id="metricRow"></div>

            <div class="charts-container">
                <div class="chart-box" id="chartHR"></div>
                <div class="chart-box" id="chartMAP"></div>
                <div class="chart-box" id="chartSI"></div>
            </div>

            <!-- SBAR & Nurse Intervention Workflow -->
            <div class="clinical-workflow">
                <div class="workflow-card">
                    <h4>📋 SBAR Clinical Communication Protocol</h4>
                    <div class="sbar-block"><strong>Situation (S):</strong> <span id="sbarS"></span></div>
                    <div class="sbar-block"><strong>Background (B):</strong> <span id="sbarB"></span></div>
                    <div class="sbar-block"><strong>Assessment (A):</strong> <span id="sbarA"></span></div>
                    <div class="sbar-block"><strong>Recommendation (R):</strong> <span id="sbarR"></span></div>
                </div>

                <div class="workflow-card">
                    <h4>🩺 Nurse Clinical Intervention Checklist</h4>
                    <div class="checklist">
                        <label class="check-item"><input type="checkbox" id="chkLactate"> Stat Serum Lactate (repeat at 2-4h)</label>
                        <label class="check-item"><input type="checkbox" id="chkCultures"> Blood Cultures x2 (aerobic & anaerobic) prior to antibiotics</label>
                        <label class="check-item"><input type="checkbox" id="chkAntibiotics"> Broad-Spectrum Empiric IV Antibiotics</label>
                        <label class="check-item"><input type="checkbox" id="chkCrystalloid"> 30 mL/kg IV Crystalloid bolus for hypotension or lactate &ge; 4.0</label>
                        <label class="check-item"><input type="checkbox" id="chkArterial"> Arterial Line placement / Norepinephrine vasopressor titration</label>
                    </div>

                    <div class="audit-form">
                        <input type="text" id="nurseSig" placeholder="Nurse Digital Signature (e.g., Jane Doe, RN - BSN #4489)">
                        <textarea id="nurseNotes" rows="2" placeholder="Clinical observations and titration notes..."></textarea>
                        <button class="btn btn-primary" onclick="signAndCommit()">✍️ Sign & Commit to Hospital EHR</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- EHR Audit Stream Table -->
        <div class="audit-stream">
            <h4>🏥 Hospital EHR Audit Repository & Signed Interventions</h4>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Bed</th>
                            <th>Patient</th>
                            <th>Risk (%)</th>
                            <th>Risk Tier</th>
                            <th>Signed Actions</th>
                            <th>Nurse Signature</th>
                        </tr>
                    </thead>
                    <tbody id="auditTableBody"></tbody>
                </table>
            </div>
        </div>
    </div>

    <footer>
        WardWatch AI &bull; Clinically Calibrated Against Non-ICU Occult Decompensation Criteria &bull; Shock Index Normal Range: 0.5–0.7; Elevated: &gt;0.90 &bull; qSOFA Threshold: &ge;2 points.
    </footer>

    <div id="toast"></div>

    <script>
        const TELEMETRY_DATA = {telemetry_json};
        const SB_URL = "{sb_url}";
        const SB_KEY = "{sb_key}";

        let currentHour = 14;
        let selectedBedId = 4;
        let isPlaying = false;
        let playInterval = null;

        // In-memory audit trail with defaults
        let localAuditLogs = [
            {{
                timestamp: "2026-10-17 14:15:00",
                bed_str: "BED-04",
                patient_name: "Eleanor Wright",
                risk_score: 91.2,
                risk_tier: "High Risk / Sepsis Alert",
                actions: "Lactate, Blood Cultures x2, 30 mL/kg Crystalloid Bolus",
                signature: "Sarah Jenkins, RN #4028"
            }},
            {{
                timestamp: "2026-10-17 12:40:00",
                bed_str: "BED-05",
                patient_name: "Arthur Brooks",
                risk_score: 84.5,
                risk_tier: "High Risk",
                actions: "BiPAP titration, Sputum culture, IV Ceftriaxone",
                signature: "David Vance, RN #1192"
            }}
        ];

        function initApp() {{
            renderFloorGrid();
            renderPatientDrilldown();
            renderAuditTable();
        }}

        function getRecordsForHour(h) {{
            return TELEMETRY_DATA.filter(r => r.hour === parseInt(h));
        }}

        function getBedRecord(bId, h) {{
            return TELEMETRY_DATA.find(r => r.bed_id === parseInt(bId) && r.hour === parseInt(h)) || TELEMETRY_DATA[0];
        }}

        function getBedTrajectory(bId) {{
            return TELEMETRY_DATA.filter(r => r.bed_id === parseInt(bId)).sort((a,b) => a.hour - b.hour);
        }}

        function onHourChange(val) {{
            currentHour = parseInt(val);
            document.getElementById('timeLabel').innerText = "T+" + (currentHour < 10 ? "0" : "") + currentHour + ":00";
            renderFloorGrid();
            renderPatientDrilldown();
        }}

        function stepHour(delta) {{
            let nextH = currentHour + delta;
            if (nextH < 1) nextH = 1;
            if (nextH > 24) nextH = 24;
            document.getElementById('hourSlider').value = nextH;
            onHourChange(nextH);
        }}

        function togglePlay() {{
            isPlaying = !isPlaying;
            const btn = document.getElementById('btnPlay');
            if (isPlaying) {{
                btn.innerText = "⏸ Pause";
                btn.style.background = "#f59e0b";
                playInterval = setInterval(() => {{
                    let next = currentHour + 1;
                    if (next > 24) next = 1;
                    document.getElementById('hourSlider').value = next;
                    onHourChange(next);
                }}, 1800);
            }} else {{
                btn.innerText = "▶ Live Play";
                btn.style.background = "var(--btn-bg)";
                clearInterval(playInterval);
            }}
        }}

        function selectBed(bId) {{
            selectedBedId = parseInt(bId);
            renderFloorGrid();
            renderPatientDrilldown();
        }}

        function renderFloorGrid() {{
            const records = getRecordsForHour(currentHour);
            const container = document.getElementById('bedGrid');
            container.innerHTML = "";

            let crit = 0, mod = 0, stab = 0;

            records.forEach(r => {{
                let tierClass = "tier-low";
                if (r.risk_score >= 70) {{
                    tierClass = "tier-high";
                    crit++;
                }} else if (r.risk_score >= 40) {{
                    tierClass = "tier-moderate";
                    mod++;
                }} else {{
                    stab++;
                }}

                const isSelected = r.bed_id === selectedBedId ? "active" : "";
                const card = document.createElement('div');
                card.className = `bed-card ${{isSelected}}`;
                card.onclick = () => selectBed(r.bed_id);

                card.innerHTML = `
                    <div class="bed-card-header">
                        <div>
                            <div class="bed-name">${{r.bed_str}} - ${{r.name}}</div>
                            <div class="bed-room">${{r.room}} &bull; ${{r.age}}${{r.sex}}</div>
                        </div>
                        <span class="tier-badge ${{tierClass}}">${{r.risk_tier}}</span>
                    </div>
                    <div class="patient-info">
                        <span class="patient-dx">${{r.dx}}</span>
                    </div>
                    <div class="vitals-mini-grid">
                        <div class="vital-mini"><div class="lbl">HR</div><div class="val">${{Math.round(r.hr)}}</div></div>
                        <div class="vital-mini"><div class="lbl">MAP</div><div class="val">${{Math.round(r.map)}}</div></div>
                        <div class="vital-mini"><div class="lbl">SI</div><div class="val">${{r.shock_index.toFixed(2)}}</div></div>
                        <div class="vital-mini"><div class="lbl">qSOFA</div><div class="val">${{r.qsofa}}</div></div>
                    </div>
                `;
                container.appendChild(card);
            }});

            document.getElementById('chipCrit').innerText = `🚨 ${{crit}} Critical`;
            document.getElementById('chipMod').innerText = `⚠️ ${{mod}} Elevated`;
            document.getElementById('chipStab').innerText = `🟢 ${{stab}} Stable`;
        }}

        function renderPatientDrilldown() {{
            const r = getBedRecord(selectedBedId, currentHour);
            const traj = getBedTrajectory(selectedBedId);

            document.getElementById('drillName').innerText = `${{r.bed_str}} - ${{r.name}} (${{r.age}}${{r.sex}})`;
            document.getElementById('drillSub').innerText = `${{r.dx}} &bull; Room ${{r.room}} &bull; Attending: ${{r.md}}`;

            let tierClass = "tier-low";
            if (r.risk_score >= 70) tierClass = "tier-high";
            else if (r.risk_score >= 40) tierClass = "tier-moderate";

            document.getElementById('drillBadge').innerHTML = `<span class="tier-badge ${{tierClass}}" style="font-size: 0.85rem; padding: 6px 12px;">${{r.risk_tier}} (${{r.risk_score.toFixed(1)}}%)</span>`;

            // Vital Metrics Row
            const metricRow = document.getElementById('metricRow');
            metricRow.innerHTML = `
                <div class="metric-tile">
                    <div class="label">Heart Rate</div>
                    <div class="value">${{Math.round(r.hr)}} <span style="font-size: 0.8rem; font-weight: normal;">bpm</span></div>
                    <div class="sub">Normal: 60-100</div>
                </div>
                <div class="metric-tile">
                    <div class="label">Blood Pressure</div>
                    <div class="value">${{Math.round(r.sbp)}}/${{Math.round(r.dbp)}}</div>
                    <div class="sub">MAP: ${{Math.round(r.map)}} mmHg</div>
                </div>
                <div class="metric-tile">
                    <div class="label">Shock Index</div>
                    <div class="value" style="color: ${{r.shock_index > 0.9 ? '#ef4444' : 'inherit'}};">${{r.shock_index.toFixed(2)}}</div>
                    <div class="sub">Alert threshold: &gt; 0.90</div>
                </div>
                <div class="metric-tile">
                    <div class="label">SpO2 / Temp</div>
                    <div class="value">${{r.spo2.toFixed(1)}}%</div>
                    <div class="sub">${{r.temp.toFixed(1)}} &deg;C &bull; RR: ${{r.rr}}/min</div>
                </div>
                <div class="metric-tile">
                    <div class="label">Serum Lactate</div>
                    <div class="value" style="color: ${{r.lactate > 2.0 ? '#ef4444' : 'inherit'}};">${{r.lactate.toFixed(2)}} <span style="font-size: 0.75rem;">mmol/L</span></div>
                    <div class="sub">qSOFA: ${{r.qsofa}} points</div>
                </div>
            `;

            // Plotly Charts
            renderPlotlyCharts(traj, r);

            // SBAR Content
            document.getElementById('sbarS').innerText = `Patient in ${{r.bed_str}} (${{r.name}}) exhibits a sepsis risk of ${{r.risk_score.toFixed(1)}}% at simulation hour T+${{currentHour < 10 ? '0' : ''}}${{currentHour}}:00 with Shock Index = ${{r.shock_index.toFixed(2)}} and MAP = ${{Math.round(r.map)}} mmHg.`;
            document.getElementById('sbarB').innerText = `${{r.age}}-year-old ${{r.sex === 'M' ? 'male' : 'female'}} admitted with ${{r.dx}}. Under the care of ${{r.md}} in room ${{r.room}}.`;
            document.getElementById('sbarA').innerText = `Occult decompensation risk score is ${{r.risk_score.toFixed(1)}}% (${{r.risk_tier}}). 3-hour MAP delta is ${{r.delta_map_3h.toFixed(1)}} mmHg. qSOFA score is ${{r.qsofa}} points.`;
            document.getElementById('sbarR').innerText = r.risk_score >= 70
                ? "Immediate clinical escalation: Stat repeat lactate, 30 mL/kg IV crystalloid fluid challenge, blood cultures x2 prior to antibiotics, and Rapid Response Team alert."
                : (r.risk_score >= 40 ? "Intensified nursing telemetry surveillance: repeat vitals q1h, ensure vascular access, notify attending physician." : "Maintain routine ward surveillance protocol.");
        }}

        function renderPlotlyCharts(traj, currentRec) {{
            const hours = traj.map(d => d.hour);
            const hrs = traj.map(d => d.hr);
            const maps = traj.map(d => d.map);
            const sis = traj.map(d => d.shock_index);

            const commonLayout = (title, yTitle, threshVal, threshName) => ({{
                title: {{ text: `<b>${{title}}</b>`, font: {{ size: 13, color: '#0f172a' }}, x: 0.05 }},
                margin: {{ l: 45, r: 25, t: 35, b: 95 }},
                autosize: true,
                height: 270,
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                xaxis: {{
                    title: {{ text: 'Simulation Timeline (Hours)', font: {{ size: 10, color: '#64748b' }}, standoff: 12 }},
                    tickmode: 'linear',
                    dtick: 4,
                    range: [1, 24],
                    gridcolor: '#f1f5f9'
                }},
                yaxis: {{
                    title: {{ text: yTitle, font: {{ size: 10, color: '#64748b' }} }},
                    gridcolor: '#f1f5f9'
                }},
                legend: {{
                    orientation: 'h',
                    y: -0.4,
                    x: 0,
                    font: {{ size: 9, color: '#475569' }}
                }},
                shapes: [
                    {{
                        type: 'line',
                        x0: currentHour,
                        x1: currentHour,
                        y0: 0,
                        y1: 1,
                        yref: 'paper',
                        line: {{ color: '#0284c7', width: 2, dash: 'dot' }}
                    }},
                    threshVal ? {{
                        type: 'line',
                        x0: 1,
                        x1: 24,
                        y0: threshVal,
                        y1: threshVal,
                        line: {{ color: '#ef4444', width: 1.5, dash: 'dash' }}
                    }} : null
                ].filter(Boolean)
            }});

            // 1. HR Chart
            Plotly.newPlot('chartHR', [
                {{
                    x: hours,
                    y: hrs,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'HR (bpm)',
                    line: {{ color: '#0284c7', width: 2.5 }},
                    marker: {{ size: 5, color: '#0284c7' }}
                }},
                {{
                    x: [1, 24],
                    y: [100, 100],
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Tachycardia (100 bpm)',
                    line: {{ color: '#ef4444', width: 1.5, dash: 'dash' }}
                }}
            ], commonLayout('Heart Rate Trajectory', 'bpm', null, null), {{ responsive: true, displayModeBar: false }});

            // 2. MAP Chart
            Plotly.newPlot('chartMAP', [
                {{
                    x: hours,
                    y: maps,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'MAP (mmHg)',
                    line: {{ color: '#10b981', width: 2.5 }},
                    marker: {{ size: 5, color: '#10b981' }}
                }},
                {{
                    x: [1, 24],
                    y: [65, 65],
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Hypotension (<65 mmHg)',
                    line: {{ color: '#ef4444', width: 1.5, dash: 'dash' }}
                }}
            ], commonLayout('Mean Arterial Pressure (MAP)', 'mmHg', null, null), {{ responsive: true, displayModeBar: false }});

            // 3. Shock Index Chart
            Plotly.newPlot('chartSI', [
                {{
                    x: hours,
                    y: sis,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'Shock Index (SI)',
                    line: {{ color: '#f59e0b', width: 2.5 }},
                    marker: {{ size: 5, color: '#f59e0b' }}
                }},
                {{
                    x: [1, 24],
                    y: [0.90, 0.90],
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Occult Shock (>0.90)',
                    line: {{ color: '#ef4444', width: 1.5, dash: 'dash' }}
                }}
            ], commonLayout('Shock Index (SI = HR / SBP)', 'SI Ratio', null, null), {{ responsive: true, displayModeBar: false }});
        }}

        function signAndCommit() {{
            const nurse = document.getElementById('nurseSig').value.trim();
            const notes = document.getElementById('nurseNotes').value.trim();

            if (!nurse) {{
                showToast("⚠️ Please enter Nurse Digital Signature before signing.");
                return;
            }}

            const r = getBedRecord(selectedBedId, currentHour);
            const actions = [];
            if (document.getElementById('chkLactate').checked) actions.push("Stat Lactate");
            if (document.getElementById('chkCultures').checked) actions.push("Blood Cultures x2");
            if (document.getElementById('chkAntibiotics').checked) actions.push("IV Antibiotics");
            if (document.getElementById('chkCrystalloid').checked) actions.push("30 mL/kg Crystalloid");
            if (document.getElementById('chkArterial').checked) actions.push("Arterial Line");

            const actionStr = actions.length > 0 ? actions.join(", ") : "Bedside Assessment Documented";

            const nowStr = new Date().toISOString().replace('T', ' ').substring(0, 19);
            const record = {{
                timestamp: nowStr,
                bed_str: r.bed_str,
                patient_name: r.name,
                risk_score: r.risk_score,
                risk_tier: r.risk_tier,
                actions: actionStr,
                signature: nurse
            }};

            localAuditLogs.unshift(record);
            renderAuditTable();

            // Direct push to Supabase REST if credentials available
            if (SB_KEY) {{
                try {{
                    fetch(SB_URL + "/rest/v1/wardwatch_audit_logs", {{
                        method: "POST",
                        headers: {{
                            "apikey": SB_KEY,
                            "Authorization": "Bearer " + SB_KEY,
                            "Content-Type": "application/json",
                            "Prefer": "return=minimal"
                        }},
                        body: JSON.stringify({{
                            simulation_hour: currentHour,
                            bed_id: r.bed_id,
                            bed_str: r.bed_str,
                            patient_id: r.patient_id,
                            patient_name: r.name,
                            risk_score: r.risk_score,
                            risk_tier: r.risk_tier,
                            completed_interventions: actions.length,
                            stat_lactate: document.getElementById('chkLactate').checked,
                            blood_cultures: document.getElementById('chkCultures').checked,
                            antibiotics: document.getElementById('chkAntibiotics').checked,
                            crystalloid_bolus: document.getElementById('chkCrystalloid').checked,
                            telemetry_escalate: document.getElementById('chkArterial').checked,
                            nurse_notes: notes + " | Signed by: " + nurse
                        }})
                    }}).catch(() => {{}});
                }} catch(e) {{}}
            }}

            document.getElementById('nurseSig').value = "";
            document.getElementById('nurseNotes').value = "";
            showToast("✅ Interventions signed and recorded to Hospital EHR Audit Repository!");
        }}

        function renderAuditTable() {{
            const tbody = document.getElementById('auditTableBody');
            tbody.innerHTML = "";
            localAuditLogs.slice(0, 8).forEach(a => {{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;">${{a.timestamp}}</td>
                    <td><strong>${{a.bed_str}}</strong></td>
                    <td>${{a.patient_name}}</td>
                    <td>${{a.risk_score.toFixed(1)}}%</td>
                    <td><span class="tier-badge ${{a.risk_score >= 70 ? 'tier-high' : (a.risk_score >= 40 ? 'tier-moderate' : 'tier-low')}}">${{a.risk_tier}}</span></td>
                    <td style="max-width: 250px;">${{a.actions}}</td>
                    <td style="font-style: italic; color: #475569;">${{a.signature}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function triggerRRT() {{
            const r = getBedRecord(selectedBedId, currentHour);
            showToast(`🚨 Rapid Response Team (Code Sepsis) dispatched for ${{r.bed_str}} (${{r.name}})!`);
        }}

        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.className = "show";
            setTimeout(() => {{ t.className = ""; }}, 3500);
        }}

        window.onload = initApp;
    </script>
</body>
</html>"""
    return html
