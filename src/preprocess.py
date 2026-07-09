import pandas as pd
from pandas import DataFrame
from typing import Tuple, List
from lifelines.utils import to_long_format, add_covariate_to_timeline
from typing import Tuple, List
from sklearn.preprocessing import StandardScaler

def _format_cp(
    df: DataFrame,
    agg_funcs: dict,
    cutting_points: list,
    strata_columns: list = []
) -> DataFrame:
    """
    Format data in counting process format.

    Args
    ----
    df : pd.DataFrame
        Input long format dataframe with columns: iso_code, days, status, and other covariates.
    agg_funcs : dict
        List of condition when grouping element
    cutting_points : list[int]
        List of cutting points
    strata_columns : list
        List of columns to strata. Default is [].
        
    Returns
    -------
        cp_df : pd.DataFrame
            Counting process dataframe after grouping
    """

    def getTGroup(x):
        for idx, mock in enumerate(cutting_points):
            if x < mock:
                return idx+1
        return len(cutting_points) + 1
    
    df["tgroup"] = df["days"].apply(getTGroup)

    # return df
    df = df.groupby(["iso_code", "tgroup"]).agg(agg_funcs).reset_index()

    for col in strata_columns:
        for idx in range(len(cutting_points) + 1):
            df[f"{col}::strata_{idx+1}"] = df[col].where(df['tgroup'] == idx+1, 0)

    return df.drop(columns=strata_columns, axis=0)


def format_data(
        timedp_df: DataFrame,
        timeidp_df: DataFrame,
        agg_functions: dict,
        cutting_points: List,
        tdp_effect: bool = False,
        normalized: bool = True,
        scaler: StandardScaler = None
    ) -> Tuple[DataFrame, StandardScaler]:
    """
    Format data in Couting Process.

    Args
    ----
    timedp_df : Dataframe
        Time dependent data.

    timeidp_df : Dataframe
        Time independent data.

    agg_functions : dict
        Dictionary of aggregate functions.

    cutting_points : list
        List of cutting points.

    tdp_effect : bool
        Whether using strata or not.

    Returns
    -------
    CP_df : pd.DataFrame
        Data in counting process.
    """
    base_df = timeidp_df.set_index(keys="iso_code")
    base_df = to_long_format(base_df, duration_col="duration").reset_index()

    if not tdp_effect:
        tdp_new_df = _format_cp(timedp_df.copy(), agg_functions, cutting_points)
    else:
        strata_cols = [col for col in timedp_df.columns if col not in ["iso_code", "days", "status"]]
        tdp_new_df = _format_cp(timedp_df.copy(), agg_functions, cutting_points, strata_cols)
    
    df = add_covariate_to_timeline(base_df, tdp_new_df, event_col="status", duration_col="days", id_col="iso_code")

    if normalized:
        feature_cols = [col for col in df.columns if col not in ['start', 'tgroup', 'stop', 'iso_code', 'status']]
        scaled_df, scaler = normalize_features(df, feature_cols, scaler)
        return scaled_df, scaler
    else:
        return df, None
    
def normalize_features(
        orgin_df: pd.DataFrame, 
        feature_cols: list,
        scaler: StandardScaler = None) -> Tuple[DataFrame, StandardScaler]:
    """
    Normalizes the selected features in the input dataframes.

    Args
    ----
    orgin_df : pd.DataFrame
        The original dataframe containing the features to be normalized.
    
    feature_cols : list
        List of feature column names to be normalized.
    
    scaler : StandardScaler, optional
        An instance of StandardScaler to be used for normalization. If None, a new StandardScaler
        will be created and fitted to the data.

    Returns
    -------
    indp_train_scaled : pd.DataFrame
        The resulted normalized dataframe.
    
    scaler : StandardScaler
        The fitted StandardScaler instance.
    """
    if scaler is None:
        scaler = StandardScaler()
        scaler.fit(orgin_df[feature_cols])

    indp_train_scaled = orgin_df.copy()

    indp_train_scaled[feature_cols] = scaler.transform(orgin_df[feature_cols])

    return indp_train_scaled, scaler