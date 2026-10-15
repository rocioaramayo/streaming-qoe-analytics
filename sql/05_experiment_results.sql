CREATE OR REPLACE VIEW `YOUR_PROJECT_ID.streaming_qoe_analytics.v_experiment_results` AS
WITH by_variant AS (
  SELECT
    variant,
    COUNT(*) AS assigned_users,
    COUNTIF(CAST(activated AS INT64) = 1) AS activated_users,
    COUNTIF(CAST(activated AS INT64) = 1 AND CAST(contained_7d AS INT64) = 1) AS contained_users,
    COUNTIF(CAST(activated AS INT64) = 1 AND CAST(technical_visit_requested AS INT64) = 1) AS visit_users,
    SUM(CAST(avoided_visit_cost_usd AS FLOAT64)) AS avoided_visit_cost_usd
  FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.experiment_assignments`
  GROUP BY variant
), rates AS (
  SELECT
    *,
    SAFE_DIVIDE(contained_users, activated_users) AS containment_rate,
    SAFE_DIVIDE(visit_users, activated_users) AS visit_rate
  FROM by_variant
)
SELECT
  *,
  SQRT(SAFE_DIVIDE(containment_rate * (1 - containment_rate), activated_users)) AS containment_se,
  containment_rate - 1.96 * SQRT(SAFE_DIVIDE(containment_rate * (1 - containment_rate), activated_users)) AS ci95_low,
  containment_rate + 1.96 * SQRT(SAFE_DIVIDE(containment_rate * (1 - containment_rate), activated_users)) AS ci95_high
FROM rates;

CREATE OR REPLACE VIEW `YOUR_PROJECT_ID.streaming_qoe_analytics.v_experiment_lift` AS
WITH r AS (
  SELECT * FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.v_experiment_results`
), p AS (
  SELECT
    MAX(IF(STARTS_WITH(variant, 'A_'), containment_rate, NULL)) AS p_control,
    MAX(IF(STARTS_WITH(variant, 'B_'), containment_rate, NULL)) AS p_treatment,
    MAX(IF(STARTS_WITH(variant, 'A_'), activated_users, NULL)) AS n_control,
    MAX(IF(STARTS_WITH(variant, 'B_'), activated_users, NULL)) AS n_treatment
  FROM r
)
SELECT
  p_treatment - p_control AS absolute_lift,
  SAFE_DIVIDE(p_treatment - p_control, p_control) AS relative_lift,
  (p_treatment - p_control) - 1.96 * SQRT(
    SAFE_DIVIDE(p_control * (1 - p_control), n_control) +
    SAFE_DIVIDE(p_treatment * (1 - p_treatment), n_treatment)
  ) AS diff_ci95_low,
  (p_treatment - p_control) + 1.96 * SQRT(
    SAFE_DIVIDE(p_control * (1 - p_control), n_control) +
    SAFE_DIVIDE(p_treatment * (1 - p_treatment), n_treatment)
  ) AS diff_ci95_high
FROM p;

