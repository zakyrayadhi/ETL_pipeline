import pandas as pd
from config import INITIAL_CSV_FILE, DELTA_CSV_FILE, CSV_FILE

# Default mode
CURRENT_MODE = "full"


def set_mode(mode):
    global CURRENT_MODE

    if mode not in ["full", "initial", "delta"]:
        raise ValueError(
            "Mode harus 'full', 'initial', atau 'delta'"
        )

    CURRENT_MODE = mode


def extract_data():

    if CURRENT_MODE == "full":
        csv_file = CSV_FILE

    elif CURRENT_MODE == "initial":
        csv_file = INITIAL_CSV_FILE

    else:  # delta
        csv_file = DELTA_CSV_FILE

    print(f"Reading file : {csv_file}")

    df = pd.read_csv(csv_file)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print(f"Extracted {len(df)} rows.")

    return df