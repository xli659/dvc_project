import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
import pickle

# Load the model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Load the fixed test dataset
test_data = pd.read_csv("test_dataset.csv")
X_test = test_data["X_test"].values.reshape(-1, 1)
y_test = test_data["y_test"].values

# Validate the model
preds = model.predict(X_test)
f1 = f1_score(y_test, preds, average='macro')
print(f"Validation F1 score: {f1:.4f}")

# Save the validation metrics
import json
with open("validation_metrics.json", "w") as f:
    json.dump({"f1": f1}, f)