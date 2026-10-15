# Diccionario de datos

## `ga4_events_flat`

Tabla de eventos a nivel evento. Su forma es deliberadamente plana para cargarla rápido en BigQuery; representa la información que en una exportación nativa de GA4 estaría dentro de `event_params`.

Campos clave:

| Campo | Tipo esperado | Descripción |
|---|---|---|
| `event_id` | STRING | Identificador único del evento. |
| `event_timestamp` | INT64 | Timestamp UTC en microsegundos. |
| `user_pseudo_id` | STRING | Identificador seudónimo del usuario. |
| `session_id` | STRING | Sesión de reproducción. |
| `incident_id` | STRING | Incidente de QoE, cuando corresponde. |
| `event_name` | STRING | Evento definido en `tracking_plan.csv`. |
| `ab_test_variant` | STRING | Variante persistente del experimento. |
| `amba_zone_id` | STRING | Nodo/zona sintética de AMBA. |
| `live_latency_ms` | INT64 | Latencia estimada de reproducción en vivo. |
| `bitrate_kbps` | INT64 | Bitrate estimado. |
| `stall_duration_ms` | INT64 | Duración del microcorte. |
| `diagnosed_cause` | STRING | Causa diagnosticada. |
| `source_type` | STRING | Siempre `synthetic`. |

## `experiment_assignments`

Una fila por usuario. Es la fuente de verdad del experimento y evita contar eventos repetidos como observaciones independientes.

## `external_amba_alerts`

Alertas externas simuladas de energía, inundación o nodos de red, utilizadas para enriquecer el diagnóstico geográfico.

## `tracking_plan`

Contrato analítico con el nombre, disparador, parámetros y objetivo de cada evento.

