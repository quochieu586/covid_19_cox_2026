from pandas import DataFrame
from typing import Tuple, List
from lifelines import CoxTimeVaryingFitter
from typing import Tuple, List
from sklearn.preprocessing import StandardScaler

from .preprocess import format_data

def _get_time_varying_fitter(df: DataFrame, columns: list, l2_pen: float, l1_pen: float):
    df = df[columns]
    covid_tdp = CoxTimeVaryingFitter(penalizer=l2_pen, l1_ratio=l1_pen)
    covid_tdp.fit(df, id_col='iso_code', event_col='status', start_col='start', stop_col='stop', fit_options={'step_size': 0.5})
    return covid_tdp

def fitting_model(
        timedp_df: DataFrame,
        timeidp_df: DataFrame,
        agg_functions: dict,
        cutting_points: list,
        l2_pen: float = 0,
        l1_pen: float = 0,
        tdp_effect: bool = False,
        normalized: bool = True,
        unselected_col: List[str] = [],
    ) -> Tuple[CoxTimeVaryingFitter, StandardScaler]:
    """
    Fit the piece-wise time-varying Cox model.

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

    l2_pen : float
        L2 penalizer for elastic net cox.

    l1_pen : float
        L1 penalizer for elastic net cox.

    unselected_col : list[str]
        List of skipped columns.

    Returns
    -------
    model : CoxTimeVaryingFitter
        Model after fitting.

    CP_df : pd.DataFrame
        Dataset in counting process format.
    """
    # print("Step 1: Create counting process data...")
    CP_df, scaler = format_data(timedp_df, timeidp_df, agg_functions, cutting_points, 
                                    tdp_effect=tdp_effect, normalized=normalized)

    # print("Step 2: Fit the model...")
    columns = [col for col in CP_df.columns if col != "tgroup" and col not in unselected_col]

    return _get_time_varying_fitter(CP_df, columns, l2_pen, l1_pen), scaler
