import json
import pickle
import numpy as np
import pandas as pd
import os

class PricePredictionService:
    def __init__(self):
        self.model = None
        self.data_columns = None
        self.locations = None
        self.column_lookup = None  # NEW

    def load_artifacts(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        artifacts_dir = os.path.join(base_dir, "artifacts")

        with open(os.path.join(artifacts_dir, "columns.json"), "r") as f:
            self.data_columns = json.load(f)["data_columns"]

        # Build lowercase → original column name map
        self.column_lookup = {col.lower(): col for col in self.data_columns}

        self.locations = self.data_columns[3:]

        with open(os.path.join(artifacts_dir, "real_state_price_prediction.pickle"), "rb") as f:
            self.model = pickle.load(f)

    def predict_price(self, location, sqft, bhk, bath):
        x = np.zeros(len(self.data_columns))

        x[0] = sqft
        x[1] = bath
        x[2] = bhk

        # CASE-INSENSITIVE MATCHING (SAFE)
        loc_key = location.lower()
        if loc_key in self.column_lookup:
            col_name = self.column_lookup[loc_key]
            idx = self.data_columns.index(col_name)
            x[idx] = 1

        x_df = pd.DataFrame([x], columns=self.data_columns)
        return round(self.model.predict(x_df)[0], 2)
