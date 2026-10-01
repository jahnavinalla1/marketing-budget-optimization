# Data contracts and metric definitions

All records are synthetic. Seeds 41, 52, 63, and 74 regenerate the four respective datasets. No personal data, proprietary company data, scraped ad accounts, or API credentials are used.

## Project 03 — budget allocation

`calibration.csv`: 16 synthetic weekly spend/response observations per channel, 64 rows. `incremental_members` is a noisy continuous estimate from a hypothetical experiment, so fractional values are intentional. Weeks 1–12 train; 13–16 are held out. Spend ranges $4,000–$18,000. Fit m(s)=a×(1−exp(−s/b)); solve a analytically for each candidate b, then minimize training squared error. Holdout MAE is measured in members. Parameters are fitted independently by channel.

Optimize a $40,000 weekly budget with $4,000 floors, $16,000 caps and $1,000 increments. The equal-allocation baseline is feasible. Objective: sum of modeled incremental members. No extrapolation above the calibration maximum. Response-shock scenarios retain the proposed allocation to test robustness. Neither point predictions nor stress tests are statistical confidence intervals.
