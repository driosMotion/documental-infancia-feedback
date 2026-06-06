# 🎬 Documental Infancia — Galería de Feedback

Galería web para revisar y aprobar imágenes del documental animado **Infancia**.

## Cómo funciona

### 1. Iniciar el servidor local (en la Mac)

```bash
cd ~/Documents/HermesProjects/documental-infancia-feedback
python3 feedback_server.py
```

Esto levanta el servidor en **http://192.168.1.35:8765**

### 2. Abrir desde el celular

En la misma WiFi, abrí **http://192.168.1.35:8765** desde el navegador.

### 3. Dar feedback

Por cada imagen:
- **✅ Aprobar** — la imagen está bien
- **✏️ Cambios** — pedir modificaciones (se habilita un textarea)
- **❌ Rechazar** — no sirve, hay que regenerarla

Al terminar, tocá **📤 Enviar Feedback**. El feedback se guarda en la Mac y el asistente lo recibe.

### 4. Sin WiFi

Si no estás en la misma WiFi, la página funciona igual pero el feedback se guarda localmente en el celular. Copiá el resumen y pegalo en Telegram.

## Estructura

```
documental-infancia-feedback/
├── index.html            # Galería web
├── images.json           # Manifiesto de imágenes (yo lo actualizo)
├── feedback_server.py    # Servidor local (feedback + imágenes)
├── feedback_data.json    # Feedback recibido (se genera solo)
└── README.md
```

## GitHub Pages

La versión estática también está disponible en:
**https://driosmotion.github.io/documental-infancia-feedback/**

(El feedback local no funciona desde GitHub Pages — usá el servidor local para feedback completo)
