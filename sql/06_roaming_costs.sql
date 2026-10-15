CREATE OR REPLACE VIEW `YOUR_PROJECT_ID.streaming_qoe_analytics.v_roaming_costs` AS
SELECT
  event_date,
  roaming_country_iso,
  remote_config_bitrate_cap_kbps,
  COUNT(*) AS alerts,
  COUNT(DISTINCT user_pseudo_id) AS users,
  SUM(roaming_mb_consumed) AS roaming_mb,
  SUM(roaming_cost_usd) AS roaming_cost_usd,
  AVG(bitrate_kbps) AS avg_bitrate_kbps
FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.v_events_clean`
WHERE event_name = 'roaming_stream_alert'
GROUP BY ALL;

