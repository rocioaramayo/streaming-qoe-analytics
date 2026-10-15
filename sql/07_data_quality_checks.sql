-- Todos los controles críticos deben devolver 0.
SELECT 'duplicate_event_id' AS test, COUNT(*) AS failures
FROM (
  SELECT event_id FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.v_events_clean`
  GROUP BY event_id HAVING COUNT(*) > 1
)
UNION ALL
SELECT 'users_in_multiple_variants', COUNT(*)
FROM (
  SELECT user_pseudo_id
  FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.experiment_assignments`
  GROUP BY user_pseudo_id
  HAVING COUNT(DISTINCT variant) > 1
)
UNION ALL
SELECT 'events_without_assignment', COUNT(*)
FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.v_events_clean` e
LEFT JOIN `YOUR_PROJECT_ID.streaming_qoe_analytics.experiment_assignments` a USING (user_pseudo_id)
WHERE a.user_pseudo_id IS NULL
UNION ALL
SELECT 'non_synthetic_rows', COUNT(*)
FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.v_events_clean`
WHERE source_type != 'synthetic';

