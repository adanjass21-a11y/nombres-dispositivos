# Consulta de IP (Python + Flask)

Aplicación web sencilla para consultar:
- IP introducida y tipo IPv4/IPv6
- DNS inverso (si existe)
- Metadatos públicos aproximados de IP pública: ubicación, ISP, organización y ASN

## Ejecutar localmente

1. Instala Python 3.11 o 3.12.
2. En esta carpeta, ejecuta:

   ```bash
   python -m venv .venv
   ```

3. Activa el entorno:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

4. Instala dependencias y arranca:

   ```bash
   pip install -r requirements.txt
   python app.py
   ```

5. Abre `http://127.0.0.1:5000`.

## Publicación

Netlify sirve el frontend y sus funciones de servidor documentadas se escriben en JavaScript/TypeScript o Go; este proyecto Flask necesita un servicio que ejecute Python (por ejemplo, Render o Railway). Sube esta carpeta a un repositorio Git y crea allí un servicio web Python. Comando de inicio: `gunicorn app:app`.

## Limitaciones importantes

- Una IP privada como `192.168.x.x`, `10.x.x.x` o `172.16.x.x` solo tiene sentido dentro de la red correspondiente.
- El DNS inverso, si existe, no garantiza que sea el nombre real de Windows.
- La IP por sí sola no revela el nombre real del dispositivo, el usuario, el número de serie ni todos sus datos. Para eso se requiere un agente instalado con autorización o una herramienta de inventario de la red.
- La ubicación por IP es aproximada y puede señalar la sede del proveedor, VPN o salida de red.
- La aplicación no escanea puertos ni intenta entrar a los dispositivos.
