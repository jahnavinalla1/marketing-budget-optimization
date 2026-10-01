-- Calibration summary: hypothetical weekly experiments, not causal estimates
-- inferred from ordinary attributed performance.
SELECT channel, COUNT(*) AS calibration_points,
 MIN(spend_usd) AS min_observed_spend, MAX(spend_usd) AS max_observed_spend,
 SUM(incremental_members) AS incremental_members, SUM(spend_usd) AS spend_usd,
 SUM(spend_usd)/NULLIF(SUM(incremental_members),0) AS pooled_incremental_cac
FROM calibration GROUP BY channel;
