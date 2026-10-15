# Informe de calidad de datos

Validación ejecutada sobre los archivos generados con semilla `20261015`.

| Control | Resultado |
|---|---:|
| Usuarios únicos asignados | 4.000 |
| Eventos | 39.265 |
| IDs de evento duplicados | 0 |
| Usuarios presentes en ambas variantes | 0 |
| Eventos sin usuario asignado | 0 |
| Registros sin `event_id` | 0 |
| Registros marcados como sintéticos | 39.265 |

Distribución A/B: 2.020 usuarios de control y 1.980 de tratamiento. La diferencia de contención observada en la simulación fue de +3,95 pp, con IC 95% entre +0,69 y +7,21 pp.

## Limitaciones

- Los datos no provienen de clientes reales ni reproducen tasas internas de ninguna empresa.
- La causalidad solo se ilustra dentro de la simulación; una implementación real necesitaría monitorear SRM, pérdidas de tracking, interferencias y exposición efectiva.
- Coordenadas, alertas, costos y causas son plausibles, no observados.
- Los resultados deben presentarse como demostración metodológica y no como impacto empresarial real.

