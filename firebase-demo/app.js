import { initializeApp } from "https://www.gstatic.com/firebasejs/12.15.0/firebase-app.js";
import { getAnalytics, logEvent, setUserProperties } from "https://www.gstatic.com/firebasejs/12.15.0/firebase-analytics.js";
import { getRemoteConfig, fetchAndActivate, getBoolean, getNumber } from "https://www.gstatic.com/firebasejs/12.15.0/firebase-remote-config.js";

let analytics = null;
let variant = "LOCAL_DEMO";
const eventLog = document.querySelector("#eventLog");

function localLog(name, params) {
  const item = document.createElement("li");
  item.textContent = `${new Date().toLocaleTimeString()} · ${name} · ${JSON.stringify(params)}`;
  if (eventLog.children[0]?.textContent.startsWith("Esperando")) eventLog.innerHTML = "";
  eventLog.prepend(item);
}

try {
  const { firebaseConfig } = await import("./firebase-config.js");
  const app = initializeApp(firebaseConfig);
  analytics = getAnalytics(app);
  const remoteConfig = getRemoteConfig(app);
  remoteConfig.settings.minimumFetchIntervalMillis = 0;
  remoteConfig.defaultConfig = {
    smart_diagnosis_enabled: false,
    roaming_bitrate_cap_kbps: 0,
    router_photo_flow_enabled: false
  };
  await fetchAndActivate(remoteConfig);
  const smart = getBoolean(remoteConfig, "smart_diagnosis_enabled");
  const cap = getNumber(remoteConfig, "roaming_bitrate_cap_kbps");
  variant = smart ? "B_TREATMENT_SMART_DIAGNOSIS" : "A_CONTROL_GENERIC_REBOOT";
  document.querySelector("#smartStatus").textContent = smart ? "activo" : "inactivo";
  document.querySelector("#bitrateStatus").textContent = cap ? `${cap} kbps` : "sin límite";
  document.querySelector("#variantStatus").textContent = variant;
  setUserProperties(analytics, { experiment_variant: variant, source_type: "synthetic_demo" });
} catch (error) {
  document.querySelector("#smartStatus").textContent = "modo local";
  document.querySelector("#bitrateStatus").textContent = "modo local";
  localLog("firebase_not_configured", { message: "Copiar firebase-config.example.js como firebase-config.js" });
}

document.querySelectorAll("button[data-event]").forEach((button) => {
  button.addEventListener("click", () => {
    const name = button.dataset.event;
    const params = {
      experiment_id: "qoe_smart_diagnosis_v1",
      experiment_variant: variant,
      platform: "WEB_DEMO",
      source_type: "synthetic_demo"
    };
    if (analytics) logEvent(analytics, name, params);
    localLog(name, params);
  });
});

