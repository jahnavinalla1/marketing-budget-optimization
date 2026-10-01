- dashboard: budget_plan_portfolio
  title: "Marketing Investment & Budget Allocation — Synthetic Data"
  layout: newspaper
  preferred_viewer: dashboards-next
  elements:
  - name: primary_view
    title: "Marketing Investment & Budget Allocation"
    model: marketing
    explore: budget_plan
    type: looker_column
    fields: [budget_plan.channel, budget_plan.recommended_spend]
    row: 0
    col: 0
    width: 24
    height: 10
