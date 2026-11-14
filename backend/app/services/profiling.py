
import pandas as pd


def generate_profile(df: pd.DataFrame):
    """
    Generate an automated profile of an uploaded dataset.
    """

    total_rows, total_columns = df.shape

    # Missing value analysis
    missing_values = df.isnull().sum()

    missing_percentage = (
        df.isnull().mean() * 100
    )

    # Duplicate record analysis
    duplicate_count = int(df.duplicated().sum())

    # Column-wise analysis
    column_profiles = []

    for column in df.columns:

        series = df[column]

        profile = {
            "column_name": str(column),
            "data_type": str(series.dtype),
            "total_values": int(series.count()),
            "missing_values": int(series.isnull().sum()),
            "missing_percentage": round(
                float(missing_percentage[column]), 2
            ),
            "unique_values": int(series.nunique()),
        }

        # Numerical column statistics
        if pd.api.types.is_numeric_dtype(series):

            profile["statistics"] = {
                "mean": (
                    float(series.mean())
                    if series.notna().any() else None
                ),
                "median": (
                    float(series.median())
                    if series.notna().any() else None
                ),
                "minimum": (
                    float(series.min())
                    if series.notna().any() else None
                ),
                "maximum": (
                    float(series.max())
                    if series.notna().any() else None
                ),
                "standard_deviation": (
                    float(series.std())
                    if series.notna().any() else None
                )
            }

        column_profiles.append(profile)

    # Overall dataset summary
    return {
        "total_rows": int(total_rows),
        "total_columns": int(total_columns),
        "total_missing_values": int(missing_values.sum()),
        "duplicate_records": duplicate_count,
        "columns": column_profiles
    }
