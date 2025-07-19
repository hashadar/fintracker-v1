"""Asset classification functions for categorizing financial assets."""

from ..config import ASSET_TO_ASSET_TYPE, ASSET_TYPES, PLATFORM_TO_ASSET_TYPE


def classify_asset_types(df):
    """
    Classify assets into Cash, Investments, Pensions, etc., based on predefined mappings.
    Classification is performed by first checking the 'Platform' and then the 'Asset' columns.

    Args:
        df (pd.DataFrame): DataFrame with 'Asset' and 'Platform' columns.

    Returns:
        pd.DataFrame: DataFrame with an added 'Asset_Type' column.
    """
    if df is None or df.empty:
        return df

    df = df.copy()

    # Initialize Asset_Type with a default value
    df["Asset_Type"] = ASSET_TYPES["OTHER"]

    # Classify based on the 'Platform' column first
    if "Platform" in df.columns:
        df["Asset_Type"] = (
            df["Platform"].map(PLATFORM_TO_ASSET_TYPE).fillna(df["Asset_Type"])
        )

    # For assets still unclassified, use the 'Asset' column
    unclassified_mask = df["Asset_Type"] == ASSET_TYPES["OTHER"]
    if "Asset" in df.columns and unclassified_mask.any():
        df.loc[unclassified_mask, "Asset_Type"] = (
            df.loc[unclassified_mask, "Asset"]
            .map(ASSET_TO_ASSET_TYPE)
            .fillna(df.loc[unclassified_mask, "Asset_Type"])
        )

    return df


def get_asset_type_summary(df):
    """
    Get a summary of asset type classifications.

    Args:
        df (pd.DataFrame): DataFrame with 'Asset_Type' column

    Returns:
        dict: Summary statistics for each asset type
    """
    if df is None or df.empty or "Asset_Type" not in df.columns:
        return {}

    summary = {}

    # Count assets by type
    asset_type_counts = df["Asset_Type"].value_counts()

    # Value by asset type
    asset_type_values = df.groupby("Asset_Type")["Value"].sum()

    # Platform distribution by asset type
    platform_distribution = (
        df.groupby(["Asset_Type", "Platform"])["Value"].sum().unstack(fill_value=0)
    )

    # Asset distribution by asset type
    asset_distribution = (
        df.groupby(["Asset_Type", "Asset"])["Value"].sum().unstack(fill_value=0)
    )

    summary = {
        "counts": asset_type_counts.to_dict(),
        "values": asset_type_values.to_dict(),
        "platform_distribution": platform_distribution.to_dict(),
        "asset_distribution": asset_distribution.to_dict(),
        "total_assets": len(df),
        "total_value": df["Value"].sum(),
        "unique_platforms": df["Platform"].nunique(),
        "unique_assets": df["Asset"].nunique(),
    }

    return summary


def validate_asset_classification(df):
    """
    Validate the asset classification and provide insights.

    Args:
        df (pd.DataFrame): DataFrame with 'Asset_Type' column

    Returns:
        dict: Validation results and recommendations
    """
    if df is None or df.empty:
        return {"error": "No data provided"}

    validation_results = {
        "total_assets": len(df),
        "classified_assets": len(df[df["Asset_Type"] != ASSET_TYPES["OTHER"]]),
        "unclassified_assets": len(df[df["Asset_Type"] == ASSET_TYPES["OTHER"]]),
        "classification_rate": len(df[df["Asset_Type"] != ASSET_TYPES["OTHER"]])
        / len(df)
        * 100,
        "asset_type_distribution": df["Asset_Type"].value_counts().to_dict(),
        "unclassified_assets_list": df[df["Asset_Type"] == ASSET_TYPES["OTHER"]][
            ["Asset", "Platform"]
        ].to_dict("records"),
        "recommendations": [],
    }

    # Generate recommendations
    if validation_results["unclassified_assets"] > 0:
        validation_results["recommendations"].append(
            f"Review {validation_results['unclassified_assets']} unclassified assets. "
            f"Consider updating PLATFORM_TO_ASSET_TYPE or ASSET_TO_ASSET_TYPE mappings in config.py."
        )

    if validation_results["classification_rate"] < 90:
        validation_results["recommendations"].append(
            "Consider adding more classification rules to improve coverage"
        )

    # Check for unusual classifications
    for asset_type in [
        ASSET_TYPES["CASH"],
        ASSET_TYPES["INVESTMENTS"],
        ASSET_TYPES["PENSIONS"],
    ]:
        if asset_type not in validation_results["asset_type_distribution"]:
            validation_results["recommendations"].append(
                f"No assets classified as {asset_type} - verify classification rules"
            )

    return validation_results
