# Streaming QoE Analytics

Caso de estudio end-to-end para anticipar y diagnosticar microcortes de streaming con Machine Learning, y evaluar mediante un experimento A/B un flujo de autogestión.

> **Aviso:** proyecto independiente de portfolio, construido con datos 100% sintéticos. No representa información, resultados ni una implementación oficial de Personal Flow.

## Qué demuestra

- Diseño de tracking con eventos compatibles con un modelo GA4/Firebase.
- Generación reproducible de 4.000 usuarios y 39.199 eventos.
- Asignación A/B estable por usuario, sin contaminación entre variantes.
- Modelado y análisis en BigQuery con controles de calidad.
- Modelo preventivo para estimar el riesgo de microcorte en los próximos cinco minutos.
- Modelo diagnóstico para clasificar la causa raíz después de detectar el incidente.
- Diseño de un dashboard ejecutivo en Looker Studio.
- Prototipo web instrumentado con Firebase Analytics y Remote Config.
- Traducción de señales técnicas en KPIs de experiencia y costos operativos.

## Preguntas de negocio

1. ¿Dónde y por qué ocurren los microcortes?
2. ¿Qué porcentaje de incidentes puede resolverse sin visita técnica?
3. ¿El diagnóstico inteligente mejora la contención frente al reinicio genérico?
4. ¿Qué impacto potencial tienen las visitas evitadas y el streaming en roaming?

## Arquitectura

```mermaid
flowchart LR
    A[App web demo\nFirebase Analytics] --> B[BigQuery\nevents + assignments]
    C[Alertas AMBA\nsintéticas] --> B
    D[Remote Config\nvariantes y bitrate] --> A
    B --> E[SQL de calidad\ny métricas]
    E --> F[Looker Studio\n3 páginas]
    B --> G[ML preventivo\nriesgo a 5 minutos]
    G --> H[ML diagnóstico\nclasificación de causa raíz]
```

Para publicar el proyecto hoy, los CSV se cargan manualmente en BigQuery. La exportación nativa de Firebase puede tardar hasta 48 horas, por lo que queda documentada como evolución de la arquitectura.

## Resultados de validación del experimento sintético

| Variante | Usuarios | Activados | Contención 7 días | Visita técnica |
|---|---:|---:|---:|---:|
| Control: reinicio genérico | 2.020 | 1.646 | 63,12% | 36,88% |
| Tratamiento: diagnóstico inteligente | 1.980 | 1.634 | 67,07% | 32,93% |

- Diferencia de contención: **+3,95 puntos porcentuales**.
- IC 95% de la diferencia: **+0,69 a +7,21 pp**.
- El resultado es una simulación diseñada para practicar análisis experimental; no es evidencia de impacto real.

## Estructura

```text
data/             CSV listos para BigQuery + generador reproducible
ml/               entrenamiento, inferencia y artefactos del modelo
sql/              creación de tablas, vistas, análisis y pruebas de calidad
docs/             arquitectura, diccionario, QA y checklist de publicación
firebase-demo/    prototipo instrumentado para Analytics y Remote Config
looker/           guía exacta para construir el dashboard
LINKEDIN_POST.md  texto breve y honesto para publicar
```

## Inicio rápido

1. Crear en BigQuery el dataset `streaming_qoe_analytics` en ubicación `southamerica-east1`.
2. Cargar los cuatro CSV de `data/` usando autodetección y los nombres indicados en `docs/publish_today.md`.
3. Ejecutar los archivos de `sql/` en orden y reemplazar `YOUR_PROJECT_ID` por el ID real del proyecto.
4. Conectar Looker Studio a las vistas siguiendo `looker/dashboard_build_guide.md`.
5. Copiar `firebase-demo/firebase-config.example.js` como `firebase-config.js`, completar la configuración y servir la carpeta localmente.

## Stack

BigQuery · SQL · Looker Studio · Firebase Analytics · Remote Config · JavaScript · Python · scikit-learn · Machine Learning · experimentación A/B

## Reproducibilidad

```powershell
python data/generate_data.py
```

El generador usa una semilla fija (`20261015`) y conserva una sola variante por usuario mediante hashing estable.

## Machine Learning

El módulo `ml/` contiene dos modelos complementarios:

1. **Alerta temprana:** estima el riesgo de microcorte en los próximos cinco
   minutos a partir de las últimas señales de latencia, bitrate y Wi-Fi.
2. **Diagnóstico:** clasifica la causa raíz después de detectar el incidente.

Ambos incluyen validación cruzada, comparación con línea base, importancia de
variables, predicciones de prueba y modelos serializados.

El predictor preventivo obtuvo **86,22% de ROC-AUC**, **83,45% de PR-AUC** y
**82,63% de recall**. El clasificador diagnóstico obtuvo **77,41% de balanced
accuracy**, frente a una línea base de 25%. Los resultados corresponden a datos
sintéticos. Ver [`docs/prevention_model_card.md`](docs/prevention_model_card.md)
y [`docs/model_card.md`](docs/model_card.md).

```powershell
python ml/train_diagnosis_model.py
python ml/predict_incident.py
python ml/train_microcut_risk_model.py
python ml/predict_microcut_risk.py
```

Los datos son sintéticos y las métricas no deben interpretarse como rendimiento
en producción. El valor del proyecto está en demostrar un pipeline reproducible,
sin fuga de información y conectado con una decisión operativa concreta.

