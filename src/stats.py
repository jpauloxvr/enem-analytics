import pandas as pd

from .config import AREAS


def present(data, area):
    return data[data[f"TP_PRESENCA_{area}"] == 1]


def mean_table(data, group_column):
    columns = {}
    for area in AREAS:
        columns[area] = present(data, area).groupby(group_column)[f"NU_NOTA_{area}"].mean()
    with_status = data[data["TP_STATUS_REDACAO"].notna()]
    columns["ESSAY_WITH_ZEROS"] = with_status.groupby(group_column)["NU_NOTA_REDACAO"].mean()
    valid = data[data["TP_STATUS_REDACAO"] == 1]
    columns["ESSAY_VALID_ONLY"] = valid.groupby(group_column)["NU_NOTA_REDACAO"].mean()
    columns["n_LC"] = present(data, "LC").groupby(group_column).size()
    columns["n_CN"] = present(data, "CN").groupby(group_column).size()
    return pd.DataFrame(columns)


def absence_rates(data, group_column):
    rates = {}
    for area in ["LC", "CN"]:
        rates[f"absent_{area}_%"] = data.groupby(group_column)[
            f"TP_PRESENCA_{area}_ORIG"
        ].apply(lambda s: (s == 0).mean() * 100)
    return pd.DataFrame(rates)


def public_private_pivot(data, group_column, area):
    scores = present(data, area)
    column = f"NU_NOTA_{area}"
    means = scores.pivot_table(
        index=group_column, columns="NETWORK", values=column, aggfunc="mean"
    )
    counts = scores.pivot_table(
        index=group_column, columns="NETWORK", values=column, aggfunc="count"
    )
    return pd.DataFrame({
        "public": means["Public"],
        "private": means["Private"],
        "gap": means["Private"] - means["Public"],
        "n_public": counts["Public"],
        "n_private": counts["Private"],
    })


def filter_min_private(pivot, minimum=1000):
    return pivot[pivot["n_private"] >= minimum]


def national_mean_std(df):
    result = {}
    for area in AREAS:
        scores = present(df, area)[f"NU_NOTA_{area}"]
        result[area] = (scores.mean(), scores.std())
    return result


def state_zscores(state_means, national):
    z = pd.DataFrame(index=state_means.index)
    for area in AREAS:
        mean, std = national[area]
        z[area] = (state_means[area] - mean) / std
    z["range"] = z[AREAS].max(axis=1) - z[AREAS].min(axis=1)
    return z


def gap_in_std(network_means, school_subset):
    result = {}
    for area in AREAS:
        gap = network_means.loc["Private", area] - network_means.loc["Public", area]
        std = present(school_subset, area)[f"NU_NOTA_{area}"].std()
        result[area] = gap / std
    return pd.Series(result)
