# app.py
import streamlit as st
import impact_sim
import mitigation

st.title("🌍 Asteroid Impact Simulation")

# Inputs
diam = st.number_input("Asteroid Diameter (m)", value=50.0)
dens = st.number_input("Density (kg/m³)", value=3000.0)
vel = st.number_input("Velocity (km/s)", value=20.0)
lat = st.number_input("Impact Latitude", value=6.5)
lon = st.number_input("Impact Longitude", value=3.4)
pop = st.number_input("Population Density (people/km²)", value=1000.0)

if st.button("Simulate Impact"):
    res = impact_sim.simulate_impact(diam, dens, vel, lat, lon, pop)
    st.subheader("Simulation Results")
    st.write(res["narrative"])
    st.bar_chart(
        {"Energy (MT)": [res["energy_megatons"]], "Damage Index": [res["damage_index"]]}
    )

if st.button("Show Mitigation Strategies"):
    st.subheader("Pre-Impact Strategies")
    for m in mitigation.pre_impact_strategies():
        st.write(f"**{m['name']}**: {m['description']}")
    st.subheader("Post-Impact Strategies")
    for m in mitigation.post_impact_strategies():
        st.write(f"**{m['name']}**: {m['description']}")
