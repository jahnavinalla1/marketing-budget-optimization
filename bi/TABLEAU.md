# Tableau dashboard build guide

Status: CSV exports and exact build specifications supplied; no Tableau workbook has been created or published. Build these in Tableau Desktop/Public after regenerating data. Every workbook title must include “Synthetic portfolio study.”

## 03 — Allocation

Connect separately to `outputs/allocation.csv`, `outputs/model_validation.csv`, and `outputs/sensitivity.csv`. Use side-by-side bars for baseline and recommended spend by channel, a change-in-spend table, holdout MAE bars, and scenario gains. Avoid physical joins across these different grains. Show the $40k total, $4k floor, $16k cap and $1k step. Title all gains “modeled.” Reconcile spend total and scenario percentages to the exports.

## Validation before publishing

Check each dashboard's full-data totals, one filtered slice, zero-denominator behavior, field types, tooltips, and synthetic-data disclosure. Export a screenshot, retain the `.twb`/`.twbx`, and add a real Tableau Public URL only after publishing. Never place real customer IDs in a public workbook.
