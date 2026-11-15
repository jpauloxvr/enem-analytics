import matplotlib.pyplot as plt
import seaborn as sns

from .config import AREAS, IMAGES_DIR


def save_figure(fig, filename, dpi=150):
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMAGES_DIR / filename, dpi=dpi, bbox_inches="tight")


def state_dot_plot(state_means, area="LC", national_mean=None):
    order = state_means[area].sort_values()
    fig, ax = plt.subplots(figsize=(8, 9))
    ax.scatter(order.values, order.index)
    if national_mean is not None:
        ax.axvline(national_mean, linestyle="--", color="gray")
    ax.set_title(f"Mean {area} score by state of exam (participants present)")
    ax.set_xlabel("Score")
    fig.tight_layout()
    return fig


def zscore_heatmap(z):
    order = z[AREAS].mean(axis=1).sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(7, 10))
    sns.heatmap(
        z.loc[order, AREAS], annot=True, fmt=".2f", cmap="RdBu_r", center=0,
        cbar_kws={"label": "Std. deviations from national mean"}, ax=ax,
    )
    ax.set_title("State mean score by area, relative to the national mean")
    ax.set_xlabel("Area")
    ax.set_ylabel("")
    fig.tight_layout()
    return fig


def gap_dumbbell(pivot):
    pivot = pivot.sort_values("gap")
    fig, ax = plt.subplots(figsize=(8, 9))
    ax.hlines(y=pivot.index, xmin=pivot["public"], xmax=pivot["private"], color="gray")
    ax.scatter(pivot["public"], pivot.index, label="Public", zorder=3)
    ax.scatter(pivot["private"], pivot.index, label="Private", zorder=3)
    ax.set_xlabel("Mean score")
    ax.legend()
    fig.tight_layout()
    return fig


def gap_map(shapes, pivot, title):
    merged = shapes.merge(pivot[["gap"]], left_on="SIGLA_UF", right_index=True, how="left")
    fig, ax = plt.subplots(figsize=(8, 8))
    merged.plot(
        column="gap", cmap="YlOrRd", legend=True, edgecolor="white", linewidth=0.5,
        ax=ax, legend_kwds={"label": "Private minus public mean (points)"},
        missing_kwds={"color": "lightgray"},
    )
    ax.set_title(title)
    ax.set_axis_off()
    return fig
