"""Run one example early-warning prediction."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "ml" / "artifacts" / "microcut_risk" / "microcut_risk_model.joblib"


def main() -> None:
    model = joblib.load(MODEL_PATH)
    window = pd.DataFrame(
        [
            {
                "heartbeat_count": 3,
                "latency_last": 19000,
                "latency_mean": 15000,
                "latency_slope": 3600,
                "bitrate_last": 1800,
                "bitrate_mean": 2900,
                "bitrate_slope": -950,
                "wifi_last": -76,
                "wifi_mean": -69,
                "wifi_slope": -6,
                "platform": "ANDROID_TV",
                "subscription_tier": "FLOW_FULL",
                "connection_type": "HOME_WIFI",
                "amba_zone_id": "AMBA_SUR_NODO_08",
            }
        ]
    )
    risk = model.predict_proba(window)[0, 1]
    print(f"Microcut risk in the next 5 minutes: {risk:.2%}")


if __name__ == "__main__":
    main()
