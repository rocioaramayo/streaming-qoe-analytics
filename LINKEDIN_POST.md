Construí un caso de estudio end-to-end para analizar y diagnosticar la calidad de experiencia en una plataforma de streaming.

Trabajé con datos sintéticos y armé un flujo con Python, Firebase, BigQuery y Looker Studio para:

• monitorear latencia y microcortes
• anticipar el riesgo de microcorte en los próximos 5 minutos
• clasificar automáticamente su causa raíz
• evaluar un diagnóstico inteligente mediante A/B testing
• estimar visitas técnicas evitadas y costos de roaming

El predictor preventivo alcanzó 86,22% de ROC-AUC y 82,63% de recall. El modelo diagnóstico obtuvo 77,41% de balanced accuracy frente a una línea base de 25%.

Para evitar resultados artificiales incorporé señales solapadas, validación cruzada y una separación por usuario sin fuga de información. El desafío fue conectar las predicciones con una decisión concreta: cuándo intervenir, qué flujo mostrar y cómo medir su impacto.

Repositorio y dashboard: [agregar enlaces]

#MachineLearning #DataAnalytics #BigQuery #LookerStudio #Firebase #SQL #ABTesting

_Proyecto independiente de portfolio con datos 100% sintéticos. No afiliado a Personal Flow._

