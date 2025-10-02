# impact_sim.py
import numpy as np

def sphere_volume(radius_m):
    return (4/3) * np.pi * radius_m**3

def kinetic_energy_joules(diameter_m, density_kg_m3, velocity_km_s):
    r = diameter_m / 2.0
    m = density_kg_m3 * sphere_volume(r)
    v = velocity_km_s * 1000.0
    return 0.5 * m * v**2

def joules_to_megatons(energy_j):
    return energy_j / 4.184e15

def estimate_crater_diameter_km(megatons):
    return 0.01 * (megatons**(1/3)) if megatons>0 else 0

def seismic_magnitude_from_energy(megatons):
    if megatons <= 0:
        return 0.0
    return 1.5 + (1/3.0) * np.log10(megatons)

def tsunami_risk_flag(diameter_m, velocity_km_s, impact_lat):
    return diameter_m >= 50

def infrastructure_damage_index(megatons, population_density):
    energy_score = np.tanh(np.log1p(megatons)) * 5.0
    pop_score = np.tanh(population_density / 1000.0) * 5.0
    return float(min(10.0, energy_score + pop_score))

def simulate_impact(diameter_m, density_kg_m3, velocity_km_s, lat, lon, population_density):
    E_j = kinetic_energy_joules(diameter_m, density_kg_m3, velocity_km_s)
    MT = joules_to_megatons(E_j)
    crater_km = estimate_crater_diameter_km(MT)
    seismic_M = seismic_magnitude_from_energy(MT)
    tsunami_risk = tsunami_risk_flag(diameter_m, velocity_km_s, lat)
    damage_index = infrastructure_damage_index(MT, population_density)
    narrative = f"""Estimated yield: {MT:.3f} MT TNT
Crater diameter: {crater_km:.3f} km
Seismic magnitude: {seismic_M:.2f}
Tsunami risk: {'High' if tsunami_risk else 'Low'}
Damage index: {damage_index:.2f}"""
    return {
        "energy_joules": E_j,
        "energy_megatons": MT,
        "crater_km": crater_km,
        "seismic_mag": seismic_M,
        "tsunami_risk": tsunami_risk,
        "damage_index": damage_index,
        "narrative": narrative
    }
