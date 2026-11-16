
import pandas as pd
import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer


def detect_anomalies(
    df: pd.DataFrame,
    contamination: float = 0.05
):
    """
    Detect anomalies using Isolation Forest.
    """

    if not 0 < contamination <= 0.5:
        raise ValueError(
            "Contamination must be greater than 0 and at most 0.5."
        )

    if len(df) < 5:
        raise ValueError(
            "At least 5 records are required for anomaly detection."
        )

    # Select numerical columns
    numeric_df = df.select_dtypes(include=["number"]).copy()

    if numeric_df.empty:
        raise ValueError(
            "No numerical columns found in the dataset."
        )

    # Replace infinite values with missing values
    numeric_df = numeric_df.replace(
        [np.inf, -np.inf], np.nan
    )

    # Remove columns containing only missing values
    numeric_df = numeric_df.dropna(axis=1, how="all")

    if numeric_df.empty:
        raise ValueError(
            "No usable numerical features found."
        )

    # Remove constant columns
    numeric_df = numeric_df.loc[
        :, numeric_df.nunique(dropna=True) > 1
    ]

    if numeric_df.empty:
        raise ValueError(
            "All numerical features contain constant values."
        )

    # Handle missing values using median
    imputer = SimpleImputer(strategy="median")

    X = imputer.fit_transform(numeric_df)

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X)

    # Predictions: 1 = Normal, -1 = Anomaly
    predictions = model.predict(X)

    # Lower decision scores indicate more unusual observations
    decision_scores = model.decision_function(X)

    anomaly_scores = -decision_scores

    # Prepare results
    results = df.astype(object).where(
        pd.notna(df), None
    ).to_dict(orient="records")

    normal_count = 0
    anomaly_count = 0

    records = []

    for index, record in enumerate(results):

        is_anomaly = predictions[index] == -1

        if is_anomaly:
            anomaly_count += 1
            status = "Anomaly"
        else:
            normal_count += 1
            status = "Normal"

        records.append({
            "row_number": index + 1,
            "status": status,
            "anomaly_score": round(
                float(anomaly_scores[index]), 6
            ),
            "original_record": record
        })

    return {
        "total_records": len(df),
        "features_used": numeric_df.columns.tolist(),
        "normal_records": normal_count,
        "anomaly_records": anomaly_count,
        "contamination": contamination,
        "records": records
    }
