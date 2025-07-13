import json

ARCHIVO_JSON = "gitleaks-report.json"
REPORTE_HTML = "gitleaks-report.html"

def generar_html_gitleaks(data):
    html = """
    <html>
    <head>
        <title>Reporte de Gitleaks</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }
            h1 { color: #d9534f; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 10px; border: 1px solid #ccc; text-align: left; vertical-align: top; }
            th { background-color: #eaeaea; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .ok { background-color: #dff0d8; color: #3c763d; padding: 15px; border-radius: 5px; }
            .danger { background-color: #f2dede; color: #a94442; padding: 15px; border-radius: 5px; }
            code { background-color: #eee; padding: 2px 4px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🔐 Reporte de Secretos Detectados - Gitleaks</h1>
    """

    if not data:
        html += '<div class="ok">✅ No se detectaron secretos.</div>'
    else:
        html += f'<div class="danger">⚠️ Se detectaron <strong>{len(data)}</strong> posibles secretos:</div>'
        html += """
        <table>
            <tr>
                <th>Archivo</th>
                <th>Línea</th>
                <th>Clave</th>
                <th>Match</th>
                <th>Regla</th>
                <th>Autor</th>
                <th>Commit ID</th>
                <th>Mensaje</th>
                <th>Link</th>
            </tr>
        """
        for item in data:
            archivo = item.get('File', '')
            linea = item.get('StartLine', '')
            clave = item.get('Secret', '')
            match = item.get('Match', '')
            regla = item.get('RuleID', '')
            autor = f"{item.get('Author', '')} ({item.get('Email', '')})"
            commit = item.get('Commit', '')
            mensaje = item.get('Message', '')
            link = item.get('Link', '')
            link_html = f'<a href="{link}" target="_blank">🔗 Ver Commit</a>' if link else "N/A"

            html += f"""
            <tr>
                <td>{archivo}</td>
                <td>{linea}</td>
                <td>{clave}</td>
                <td><code>{match}</code></td>
                <td>{regla}</td>
                <td>{autor}</td>
                <td>{commit}</td>
                <td>{mensaje}</td>
                <td>{link_html}</td>
            </tr>
            """

        html += "</table>"

    html += "</body></html>"
    return html

def main():
    with open(ARCHIVO_JSON, 'r') as f:
        data = json.load(f)

    html = generar_html_gitleaks(data)
    with open(REPORTE_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Reporte generado: {REPORTE_HTML}")

if __name__ == "__main__":
    main()