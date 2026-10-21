"""Bootstrap helpers for clustered and skewed economic data (ECON 5200 Lab 7).

The cluster argument is a parameter, not an afterthought: pass the clusters to
cluster_bootstrap_mean and the interval respects the dependence inside each
cluster; bootstrap_mean treats every row as an independent draw.
"""
import numpy as np


def percentile_ci(draws, level=0.95):
    """Percentile interval from an array of bootstrap replicates."""
    alpha = (1.0 - level) / 2.0
    lo, hi = np.percentile(draws, [100 * alpha, 100 * (1 - alpha)])
    return float(lo), float(hi)


def bootstrap_mean(x, B=2000, seed=42):
    """Ordinary i.i.d. bootstrap of the mean. Valid only for independent draws."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x)
    return np.array([rng.choice(x, size=len(x), replace=True).mean()
                     for _ in range(B)])


def cluster_bootstrap_mean(groups, B=2000, seed=42):
    """Cluster bootstrap of the mean: resample whole clusters, then pool.

    `groups` holds one array per cluster. With few clusters the interval is much
    wider than the i.i.d. one; that width is the honest cost of the design.
    For regression with few clusters, prefer the wild cluster bootstrap
    (Cameron, Gelbach & Miller 2008).
    """
    rng = np.random.default_rng(seed)
    groups = [np.asarray(g) for g in groups]
    k = len(groups)
    if k < 2:
        raise ValueError("need at least 2 clusters")
    out = np.empty(B)
    for b in range(B):
        picked = rng.integers(0, k, size=k)
        out[b] = np.concatenate([groups[i] for i in picked]).mean()
    return out
