
import pandas as pd
import numpy as np


def calculate_quality(df: pd.DataFrame):

    total_rows, total_columns = df.shape
    total_cells = total_rows * total_columns

    if total_cells == 0:
        raise ValueError("Dataset must contain at least one cell.")

    # 1. COMPLETENESS
    missing_count = int(df.isna().sum().sum())

    completeness = (
        (total_cells - missing_count) / total_cells
    ) * 100

    # 2. UNIQUENESS
    duplicate_count = int(df.duplicated().sum())

    uniqueness = (
        (total_rows - duplicate_count) / total_rows
    ) * 100

    # 3. VALIDITY
    # Detect infinite numerical values.
    invalid_count = 0

    for column in df.columns:

        series = df[column]

        if pd.api.types.is_numeric_dtype(series):

            values = pd.to_numeric(
                series, errors="coerce"
            )

            invalid_count += int(
                np.isinf(values.fillna(0)).sum()
            )

    valid_cells = total_cells - missing_count

    validity = (
        ((valid_cells - invalid_count) / valid_cells) * 100
        if valid_cells > 0 else 100.0
    )

    # 4. CONSISTENCY
    # Detect leading/trailing whitespace in text values.
    inconsistent_count = 0

    for column in df.select_dtypes(
        include=["object", "string"]
    ).columns:

        series = df[column].dropna().astype(str)

        inconsistent_count += int(
            series.ne(series.str.strip()).sum()
        )

    consistency = (
        ((valid_cells - inconsistent_count) / valid_cells) * 100
        if valid_cells > 0 else 100.0
    )

    # Keep scores within 0 to 100.
    validity = max(0.0, validity)
    consistency = max(0.0, consistency)

    # 5. OVERALL QUALITY SCORE
    overall_score = (
        0.40 * completeness
        + 0.25 * uniqueness
        + 0.20 * validity
        + 0.15 * consistency
    )

    # QUALITY CATEGORY
    if overall_score >= 90:
        category = "Excellent"
    elif overall_score >= 75:
        category = "Good"
    elif overall_score >= 50:
        category = "Fair"
    else:
        category = "Poor"

    # ISSUE REPORT
    issues = []

    if missing_count > 0:
        issues.append({
            "issue": "Missing Values",
            "count": missing_count,
            "severity": "High"
        })

    if duplicate_count > 0:
        issues.append({
            "issue": "Duplicate Records",
            "count": duplicate_count,
            "severity": "Medium"
        })

    if invalid_count > 0:
        issues.append({
            "issue": "Infinite Numerical Values",
            "count": invalid_count,
            "severity": "High"
        })

    if inconsistent_count > 0:
        issues.append({
            "issue": "Whitespace Inconsistency",
            "count": inconsistent_count,
            "severity": "Low"
        })

    return {
        "total_rows": int(total_rows),
        "total_columns": int(total_columns),

        "quality_scores": {
            "completeness": round(completeness, 2),
            "uniqueness": round(uniqueness, 2),
            "validity": round(validity, 2),
            "consistency": round(consistency, 2),
            "overall_score": round(overall_score, 2),
            "category": category
        },

        "issues": issues
    }
