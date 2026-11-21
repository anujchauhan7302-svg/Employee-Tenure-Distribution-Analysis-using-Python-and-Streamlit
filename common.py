from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "employees.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    return df
