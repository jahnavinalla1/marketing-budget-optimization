view: budget_plan {
  sql_table_name: analytics.budget_plan ;;
  dimension: channel { primary_key: yes type: string sql: ${TABLE}.channel ;; }
  measure: baseline_spend { type: sum sql: ${TABLE}.baseline_spend_usd ;; value_format_name: usd }
  measure: recommended_spend { type: sum sql: ${TABLE}.recommended_spend_usd ;; value_format_name: usd }
  measure: modeled_members { type: sum sql: ${TABLE}.expected_incremental_members ;; value_format_name: decimal_1 }
  measure: change { type: number sql: ${recommended_spend} - ${baseline_spend} ;; value_format_name: usd }
}
