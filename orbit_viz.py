# orbit_viz.py
import numpy as np
import plotly.graph_objects as go
import webbrowser, os

HTML_OUT = os.path.join(os.path.dirname(__file__), "orbit_plot.html")


def make_simple_orbit_plot(asteroid_params=None):
    theta = np.linspace(0, 2 * np.pi, 400)
    r = 1.0
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Earth Orbit"))
    if asteroid_params:
        angle = np.deg2rad(asteroid_params.get("approach_angle_deg", 0))
        xs = np.linspace(1.5 * np.cos(angle), -0.2 * np.cos(angle), 3)
        ys = np.linspace(1.5 * np.sin(angle), -0.2 * np.sin(angle), 3)
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", name="Asteroid"))
    fig.add_trace(go.Scatter(x=[1.0], y=[0.0], mode="markers+text", text=["Earth"]))
    fig.write_html(HTML_OUT, auto_open=False)
    webbrowser.open("file://" + os.path.realpath(HTML_OUT))
    return HTML_OUT
