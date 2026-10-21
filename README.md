# Diagnosing Broken Confidence Intervals

**ECON 5200 · Causal Machine Learning & Applied Analytics · Lab 07**

## Objective

I diagnosed three bootstrap confidence intervals that looked fine or failed quietly, worked out why each one was wrong, and measured how often a nominal 95% interval actually covers the truth.

## Methodology

- Bootstrapped the median age of 32,561 respondents in the UCI Adult census data, where ages are recorded as whole numbers, and compared the percentile interval with scipy's BCa interval.
- Ran 400 simulated experiments with samples of 50 from a right-skewed lognormal distribution, and counted how often parametric and bootstrap 95% intervals contained the true mean and the true median, with a Monte Carlo standard error for each share.
- Built a simulated wage panel of 1,000 workers across 25 firms, where firms differ much more than the workers inside them, and compared a bootstrap that resamples workers with a cluster bootstrap that resamples whole firms.
- Measured the coverage of both intervals over 200 fresh panels.
- Used a `bootstrap_utils.py` module with percentile, i.i.d. and cluster bootstrap functions.
- Had an AI write a general coverage function, revised my prompt once to fix how it seeded each repetition, and checked its output against my own coverage numbers.

## Key Findings

**A bootstrap SE of zero did not mean the median was known exactly.** Every one of 2,000 resamples gave a median of 37, so the bootstrap SE was 0.000000 and the percentile interval was [37.0, 37.0]. The ages are discrete, with a large block of people at exactly 37, so the resampled median could not move. BCa returned nan with a warning instead of an interval, which was the honest answer.

**On skewed data with n = 50, no interval reached 95%.** For the mean, the parametric interval covered 92.5% and the bootstrap 92.0%, which is within noise of each other. For the median, the parametric interval covered only 66.8%, because it is centered on the sample mean, which sits above the median on right-skewed data. The bootstrap interval for the median covered 92.8%.

**Treating clustered workers as independent made the interval far too narrow.** Resampling workers gave an interval 5.7x too narrow, and it covered the true mean in only 19.5% of panels. Resampling whole firms brought coverage to 91.0%.

**The AI's first coverage function was a valid simulation but did not reproduce my numbers.** It drew its own random seeds for each repetition. After I revised the prompt so that repetition i used seed + i, its coverage matched mine exactly: 19.5% for the naive interval and 91.0% for the clustered one.

## Repository Contents

| File | Description |
|---|---|
| `lab-ch07-diagnostic.ipynb` | Full lab notebook with rendered output |
| `src/bootstrap_utils.py` | Percentile, i.i.d. and cluster bootstrap functions |

## Data

The census data is the UCI Adult Census Income dataset (32,561 respondents). The skewed samples and the clustered wage panel are simulated with fixed seeds.
