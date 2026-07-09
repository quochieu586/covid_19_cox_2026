import pandas as pd
import numpy as np
from lifelines import CoxTimeVaryingFitter

def compute_survival_probabilities(
        model, subject_df: pd.DataFrame
    ) -> pd.DataFrame:
    """
    Compute survival probabilities over time for a single subject.
    Return a dataframe with columns: "time", "survival_probability".
    """
    baseline_cumulative_hazard = model.baseline_cumulative_hazard_

    ## if the end date of the subject is not in the baseline cumulative hazard, we need to append it to the baseline cumulative hazard with the same value as the nearest existing date.
    subject_end_date = subject_df["stop"].max()
    if subject_end_date not in baseline_cumulative_hazard.index:
        # Find the nearest date in the baseline cumulative hazard
        nearest_date = baseline_cumulative_hazard.index[baseline_cumulative_hazard.index <= subject_end_date].max()
        if pd.isna(nearest_date):
            nearest_date = baseline_cumulative_hazard.index.min()
        # Append the new date with the same hazard value
        baseline_cumulative_hazard.loc[subject_end_date] = baseline_cumulative_hazard.loc[nearest_date]

    columns = model.params_.index.values
    beta = model.params_.values

    times = baseline_cumulative_hazard.index.values
    H0 = baseline_cumulative_hazard.values.flatten()

    delta_H0 = np.diff(np.insert(H0, 0, 0))

    H_i = 0
    results = []

    for t_k, dH0_k in zip(times, delta_H0):
        # find covariate value at time t_k
        row = subject_df[(subject_df["start"] <= t_k) & (subject_df["stop"] >= t_k)]

        if row.empty:
            break

        risk = np.exp(row[columns].values @ beta)[0]

        H_i += risk * dH0_k

        results.append((t_k, np.exp(-H_i)))

    return pd.DataFrame(results, columns=["time", "survival_probability"])


def C_index_calculation(model: CoxTimeVaryingFitter, base_df: pd.DataFrame) -> float:
    """
    Compute C-index of model which is then used for tuning.
    
    Args:
        model (CoxTimeVaryingFitter): Model which is already fitting.
        base_df (pd.Dataframe): Dataframe used for fitting model.
        
    Returns:
        float: C-index of model.
    """
    # print("Step 3: Evaluate the model using C-index...")

    risk_set_df = base_df.groupby(['iso_code']).agg(
        last_date = ('stop', 'max'),
        status = ('status', 'max'),
        tgroup = ('tgroup', 'max')
    ).reset_index().sort_values(by=['last_date'])

    risk_set = risk_set_df[risk_set_df['status'] == 1].values.tolist()

    # Step 2: Precompute model parameters and country data
    beta = model.params_.values  # Convert to numpy array
    selected_col = model.params_.index.values

    country_data = base_df.groupby(['iso_code', 'tgroup'])[selected_col].first().to_dict(orient='index')
    
    pi_comp = 0
    pi_conc = 0

    # Step 3: Loop over the pairs in risk set
    for idx, country_i in enumerate(risk_set):
        country_i_key = (country_i[0], country_i[3])
        country_i_data = list(country_data[country_i_key].values())
        country_i_hr = np.exp(np.matmul(beta.T, country_i_data))

        for country_j in risk_set[idx + 1:]:
            country_j_key = (country_j[0], country_i[3])
            country_j_data = list(country_data[country_j_key].values())
            # print(country_j_data)
            country_j_hr = np.exp(np.matmul(beta.T, country_j_data))

            # Case tied --> half risk score
            if country_i_hr == country_j_hr:
                pi_conc += 0.5
            # Case concordant
            elif country_i_hr > country_j_hr:
                pi_conc += 1.0

            pi_comp += 1.0

    return pi_conc / pi_comp if pi_comp > 0 else np.nan
