from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime

ORG_DATA = {
    "company": "Glocal Organization",
    "tagline": "Regional impact with a global mindset",
    "metrics": [
        {"label": "Total Employees", "value": "1,248", "trend": "+8.4%", "tone": "purple"},
        {"label": "Active Projects", "value": "42", "trend": "+6", "tone": "green"},
        {"label": "On-time Delivery", "value": "96.2%", "trend": "+2.1%", "tone": "blue"},
        {"label": "Customer Satisfaction", "value": "4.8/5", "trend": "+0.3", "tone": "orange"},
    ],
    "departments": [
        {"name": "Operations", "headcount": 210, "completion": 88, "status": "Strong"},
        {"name": "Product", "headcount": 180, "completion": 82, "status": "Stable"},
        {"name": "Marketing", "headcount": 160, "completion": 79, "status": "Growing"},
        {"name": "Finance", "headcount": 120, "completion": 91, "status": "On track"},
        {"name": "People & Culture", "headcount": 90, "completion": 85, "status": "Healthy"},
    ],
    "initiatives": [
        {"title": "Digital transformation program", "owner": "Innovation Office", "progress": 74, "due": "Q4 2026"},
        {"title": "Regional expansion rollout", "owner": "Sales Ops", "progress": 62, "due": "Aug 2026"},
        {"title": "Sustainability roadmap", "owner": "Operations", "progress": 81, "due": "Sep 2026"},
    ],
    "activity": [
        {"time": "09:45", "text": "New hiring plan approved for the customer success team.", "type": "success"},
        {"time": "11:20", "text": "North America market launch reached 82% readiness.", "type": "info"},
        {"time": "13:10", "text": "Quarterly finance review completed without blockers.", "type": "neutral"},
        {"time": "15:05", "text": "Team morale pulse survey results are trending positive.", "type": "success"},
    ],
}


def build_dashboard_html():
    cards = "".join(
        f"""
        <div class=\"card metric\" data-tone=\"{item['tone']}\">
            <span class=\"metric-label\">{item['label']}</span>
            <strong>{item['value']}</strong>
            <span class=\"trend\">{item['trend']}</span>
        </div>
        """ for item in ORG_DATA["metrics"]
    )

    departments_rows = "".join(
        f"""
        <tr>
            <td>{dept['name']}</td>
            <td>{dept['headcount']}</td>
            <td>
                <div class=\"progress\">
                    <span style=\"width: {dept['completion']}%;\"></span>
                </div>
            </td>
            <td>{dept['completion']}%</td>
            <td><span class=\"status\">{dept['status']}</span></td>
        </tr>
        """ for dept in ORG_DATA["departments"]
    )

    initiatives_rows = "".join(
        f"""
        <div class=\"initiative\">
            <div class=\"initiative-head\">
                <h4>{item['title']}</h4>
                <span>{item['due']}</span>
            </div>
            <p>{item['owner']}</p>
            <div class=\"progress\">
                <span style=\"width: {item['progress']}%;\"></span>
            </div>
            <small>{item['progress']}% complete</small>
        </div>
        """ for item in ORG_DATA["initiatives"]
    )

    activity_rows = "".join(
        f"""
        <div class=\"activity-item\">
            <span class=\"dot {item['type']}\"></span>
            <div>
                <strong>{item['time']}</strong>
                <p>{item['text']}</p>
            </div>
        </div>
        """ for item in ORG_DATA["activity"]
    )

    return f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
        <title>{ORG_DATA['company']} Dashboard</title>
        <style>
            :root {{
                --bg: #f4f7fb;
                --panel: #ffffff;
                --panel-alt: #eef4ff;
                --border: #e3e9f4;
                --text: #172033;
                --muted: #64748b;
                --purple: #7c3aed;
                --green: #16a34a;
                --blue: #2563eb;
                --orange: #f59e0b;
                --shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
            }}

            * {{ box-sizing: border-box; }}
            body {{
                margin: 0;
                font-family: Arial, Helvetica, sans-serif;
                background: linear-gradient(135deg, #eef3ff 0%, #f8fafc 100%);
                color: var(--text);
            }}

            .container {{
                max-width: 1280px;
                margin: 0 auto;
                padding: 32px 20px 48px;
            }}

            .topbar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 22px;
            }}

            .brand {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}

            .brand-mark {{
                width: 40px;
                height: 40px;
                border-radius: 12px;
                background: linear-gradient(135deg, var(--purple), var(--blue));
                color: white;
                display: grid;
                place-items: center;
                font-weight: 700;
            }}

            h1 {{
                margin: 0;
                font-size: clamp(1.8rem, 3vw, 2.6rem);
            }}

            .tagline {{
                margin: 6px 0 0;
                color: var(--muted);
                font-size: 0.95rem;
            }}

            .pill {{
                padding: 10px 16px;
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 999px;
                font-weight: 600;
                box-shadow: var(--shadow);
            }}

            .metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
                gap: 18px;
                margin: 28px 0;
            }}

            .card {{
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 18px;
                box-shadow: var(--shadow);
                padding: 22px 20px;
            }}

            .metric {{
                position: relative;
                overflow: hidden;
            }}

            .metric::before {{
                content: \"\";
                position: absolute;
                inset: 0 auto auto 0;
                width: 100%;
                height: 4px;
                background: var(--purple);
            }}

            .metric[data-tone=\"green\"]::before {{ background: var(--green); }}
            .metric[data-tone=\"blue\"]::before {{ background: var(--blue); }}
            .metric[data-tone=\"orange\"]::before {{ background: var(--orange); }}

            .metric-label {{
                display: block;
                color: var(--muted);
                font-size: 0.82rem;
                margin-bottom: 12px;
                letter-spacing: 0.03em;
                text-transform: uppercase;
            }}

            .metric strong {{
                display: block;
                font-size: clamp(1.6rem, 2vw, 2.2rem);
                margin-bottom: 10px;
            }}

            .trend {{
                color: var(--green);
                background: rgba(22, 163, 74, 0.1);
                padding: 6px 10px;
                border-radius: 999px;
                display: inline-block;
                font-weight: 700;
                font-size: 0.78rem;
            }}

            .content-grid {{
                display: grid;
                grid-template-columns: 1.5fr 1fr;
                gap: 22px;
                margin-top: 12px;
            }}

            .section {{
                background: var(--panel);
                border-radius: 18px;
                border: 1px solid var(--border);
                box-shadow: var(--shadow);
                padding: 22px;
            }}

            .section h2 {{
                margin: 0 0 18px;
                font-size: 1.18rem;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th, td {{
                text-align: left;
                padding: 14px 8px;
                border-bottom: 1px solid var(--border);
            }}

            th {{
                font-size: 0.78rem;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                color: var(--muted);
            }}

            .progress {{
                height: 10px;
                background: #edf2f7;
                border-radius: 999px;
                overflow: hidden;
            }}

            .progress span {{
                display: block;
                height: 100%;
                border-radius: inherit;
                background: linear-gradient(90deg, #7c3aed, #2563eb);
            }}

            .status {{
                background: rgba(37, 99, 235, 0.1);
                color: var(--blue);
                font-weight: 700;
                border-radius: 999px;
                padding: 6px 10px;
                display: inline-block;
                font-size: 0.76rem;
            }}

            .initiatives {{
                display: grid;
                gap: 16px;
            }}

            .initiative {{
                background: var(--panel-alt);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 16px;
            }}

            .initiative-head {{
                display: flex;
                justify-content: space-between;
                gap: 12px;
                align-items: center;
            }}

            .initiative h4 {{
                margin: 0;
                font-size: 1rem;
            }}

            .initiative p, .initiative small {{
                margin: 10px 0 12px;
                color: var(--muted);
            }}

            .activity-list {{
                display: flex;
                flex-direction: column;
                gap: 12px;
                margin-top: 6px;
            }}

            .activity-item {{
                display: flex;
                gap: 12px;
                align-items: flex-start;
                padding: 12px 0;
                border-bottom: 1px solid var(--border);
            }}

            .activity-item:last-child {{ border-bottom: none; }}

            .dot {{
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-top: 6px;
            }}

            .dot.success {{ background: var(--green); }}
            .dot.info {{ background: var(--blue); }}
            .dot.neutral {{ background: var(--orange); }}

            .activity-item strong {{
                display: block;
                margin-bottom: 5px;
                font-size: 0.8rem;
                color: var(--muted);
            }}

            .activity-item p {{
                margin: 0;
                line-height: 1.45;
            }}

            @media (max-width: 840px) {{
                .content-grid {{
                    grid-template-columns: 1fr;
                }}

                .topbar {{
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 14px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class=\"container\">
            <div class=\"topbar\">
                <div class=\"brand\">
                    <div class=\"brand-mark\">G</div>
                    <div>
                        <h1>{ORG_DATA['company']}</h1>
                        <p class=\"tagline\">{ORG_DATA['tagline']}</p>
                    </div>
                </div>
                <div class=\"pill\">Updated {datetime.now().strftime('%b %d, %Y')}</div>
            </div>

            <section class=\"metrics\">
                {cards}
            </section>

            <div class=\"content-grid\">
                <section class=\"section\">
                    <h2>Department performance</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Department</th>
                                <th>Team</th>
                                <th>Progress</th>
                                <th>Completion</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {departments_rows}
                        </tbody>
                    </table>
                </section>

                <section class=\"section\">
                    <h2>Priority initiatives</h2>
                    <div class=\"initiatives\">
                        {initiatives_rows}
                    </div>
                </section>
            </div>

            <section class=\"section\" style=\"margin-top: 22px;\">
                <h2>Recent organization activity</h2>
                <div class=\"activity-list\">
                    {activity_rows}
                </div>
            </section>
        </div>
    </body>
    </html>
    """


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            content = build_dashboard_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


def main():
    host = "127.0.0.1"
    port = 8000
    server = ThreadingHTTPServer((host, port), DashboardHandler)
    print(f"Glocal dashboard is running at http://{host}:{port}")
    print("Press Ctrl+C to stop the server.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down dashboard...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
