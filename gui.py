# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import impact_sim, orbit_viz, mitigation, data_loader
import matplotlib.pyplot as plt


class App:
    def __init__(self, root):
        self.root = root
        root.title("Asteroid Impact Simulation Suite")
        self.build_ui()

    def build_ui(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.grid()
        self.diam = tk.DoubleVar(value=50.0)
        self.dens = tk.DoubleVar(value=3000.0)
        self.vel = tk.DoubleVar(value=20.0)
        self.lat = tk.DoubleVar(value=6.5)
        self.lon = tk.DoubleVar(value=3.4)
        self.pop = tk.DoubleVar(value=1000.0)
        entries = [
            ("Diameter (m)", self.diam),
            ("Density (kg/m³)", self.dens),
            ("Velocity (km/s)", self.vel),
            ("Latitude", self.lat),
            ("Longitude", self.lon),
            ("Population Density", self.pop),
        ]
        for i, (label, var) in enumerate(entries):
            ttk.Label(frm, text=label).grid(column=0, row=i, sticky="w")
            ttk.Entry(frm, textvariable=var).grid(column=1, row=i)
        ttk.Button(frm, text="Simulate Impact", command=self.run_sim).grid(
            column=0, row=6
        )
        ttk.Button(frm, text="Show Orbit Viz", command=self.show_orbit).grid(
            column=1, row=6
        )
        ttk.Button(frm, text="Show Mitigation", command=self.show_mitigation).grid(
            column=0, row=7
        )
        self.result_box = tk.Text(frm, width=70, height=15)
        self.result_box.grid(column=0, row=8, columnspan=2)

    def run_sim(self):
        # d, rho, v, lat, lon, pop = [
        #     float(x.get())
        #     for x in (self.diam, self.dens, self.vel, self.lat, self.lon, self.pop)
        # ]
        d = float(self.diam.get())
        rho = float(self.dens.get())
        v = float(self.vel.get())
        lat = float(self.lat.get())
        lon = float(self.lon.get())
        pop = float(self.pop.get())

        # def task():
        #     res = impact_sim.simulate_impact(d, rho, v, lat, lon, pop)
        #     self.display_result(res)
        #     self.show_charts(res)

        # threading.Thread(target=task).start()
        def task():
            res = impact_sim.simulate_impact(d, rho, v, lat, lon, pop)
            # Update GUI safely in main thread
            self.root.after(0, lambda: self.display_result(res))
            self.root.after(0, lambda: self.show_charts(res))

        threading.Thread(target=task).start()

    def display_result(self, res):
        txt = f"""Energy: {res['energy_megatons']:.4f} MT
Crater: {res['crater_km']:.4f} km
Seismic M: {res['seismic_mag']:.2f}
Tsunami risk: {'YES' if res['tsunami_risk'] else 'NO'}
Damage Index: {res['damage_index']:.2f}
{res['narrative']}"""
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, txt)

    def show_orbit(self):
        orbit_viz.make_simple_orbit_plot({"approach_angle_deg": 45})

    def show_mitigation(self):
        s = "Pre-Impact:\n"
        for m in mitigation.pre_impact_strategies():
            s += f"- {m['name']}: {m['description']}\n"
        s += "\nPost-Impact:\n"
        for m in mitigation.post_impact_strategies():
            s += f"- {m['name']}: {m['description']}\n"
        messagebox.showinfo("Mitigation", s)

    # def show_charts(self, res):
    #     keys = ["Energy (MT)", "Damage Index"]
    #     vals = [res["energy_megatons"], res["damage_index"]]
    #     plt.bar(keys, vals)
    #     plt.show()

    def show_charts(self, res):
        # small bar chart: energy_megatons vs damage index
        import matplotlib.pyplot as plt

        keys = ["Energy (MT)", "Damage Index"]
        vals = [res["energy_megatons"], res["damage_index"]]
        plt.figure(figsize=(6, 4))
        plt.bar(keys, vals)
        plt.title("Impact Energy vs Damage Index")
        plt.tight_layout()
        plt.show()


def run_app():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
