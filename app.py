from flask import Flask, render_template, request
import ipaddress
import socket
import urllib.request
import json

app = Flask(__name__)

def public_ip_details(ip_text):
    """Return public-IP metadata only; does not scan devices or access private networks."""
    ip_obj = ipaddress.ip_address(ip_text)
    result = {
        "ip": str(ip_obj),
        "tipo": "IPv4" if ip_obj.version == 4 else "IPv6",
        "alcance": "Pública" if ip_obj.is_global else "Privada/reservada",
        "nombre_dns": "No disponible",
        "ubicacion": "No disponible",
        "proveedor": "No disponible",
        "organizacion": "No disponible",
        "asn": "No disponible",
    }

    try:
        hostname, aliases, _ = socket.gethostbyaddr(str(ip_obj))
        result["nombre_dns"] = hostname
        if aliases:
            result["alias_dns"] = ", ".join(aliases)
    except (socket.herror, socket.gaierror, OSError):
        pass

    # Geolocation providers generally return no useful location for private IPs.
    if ip_obj.is_global:
        url = f"https://ipwho.is/{ip_obj}"
        req = urllib.request.Request(url, headers={"User-Agent": "ConsultaIP/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
            if data.get("success"):
                city = data.get("city")
                region = data.get("region")
                country = data.get("country")
                result["ubicacion"] = ", ".join(x for x in [city, region, country] if x) or "No disponible"
                result["proveedor"] = data.get("connection", {}).get("isp") or "No disponible"
                result["organizacion"] = data.get("connection", {}).get("org") or "No disponible"
                result["asn"] = data.get("connection", {}).get("asn") or "No disponible"
        except Exception:
            result["nota"] = "No se pudo consultar el proveedor de datos públicos en este momento."

    if not ip_obj.is_global:
        result["nota"] = (
            "Las IP privadas (por ejemplo, 192.168.x.x o 10.x.x.x) solo se pueden "
            "identificar dentro de la red correspondiente. La IP por sí sola no revela "
            "el nombre real de Windows ni los datos completos del equipo."
        )
    else:
        result["nota"] = (
            "Los datos de ubicación son aproximados. Una IP pública no permite conocer "
            "por sí sola el nombre real del equipo, usuario, número de serie ni archivos."
        )
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    details = None
    error = None
    ip_value = ""
    if request.method == "POST":
        ip_value = request.form.get("ip", "").strip()
        try:
            if not ip_value:
                raise ValueError("Escribe una dirección IP.")
            details = public_ip_details(ip_value)
        except ValueError as exc:
            error = str(exc) if str(exc) else "La dirección IP no es válida."
    return render_template("index.html", details=details, error=error, ip_value=ip_value)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
