# main.py
import gui
import os

def ensure_sample():
    from data_loader import generate_sample_data, SAMPLE_PATH
    if not os.path.exists(SAMPLE_PATH):
        generate_sample_data()

if __name__ == "__main__":
    ensure_sample()
    gui.run_app()
