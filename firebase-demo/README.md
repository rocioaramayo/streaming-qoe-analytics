# Demo Firebase

1. Registrar una app web en Firebase con Analytics habilitado.
2. Copiar `firebase-config.example.js` como `firebase-config.js`.
3. Completar las credenciales públicas de configuración de la app.
4. En Remote Config crear:
   - `smart_diagnosis_enabled` (boolean)
   - `roaming_bitrate_cap_kbps` (number)
   - `router_photo_flow_enabled` (boolean)
5. Servir la carpeta, no abrir el HTML como archivo:

```powershell
python -m http.server 8080
```

Luego abrir `http://localhost:8080`. Los botones registran eventos tanto en Firebase Analytics como en la consola visible para facilitar una captura de portfolio.

