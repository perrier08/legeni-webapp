import os
from string import Template

from flask import Flask, jsonify

app = Flask(__name__)

PAGE = Template("""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Legeni WebApp</title>
  <style>
    body { font-family: sans-serif; margin: 0; }
    .banner { background: $color; color: white; padding: 2rem; }
  </style>
</head>
<body>
  <div class="banner">
    <h1>Legeni WebApp</h1>
    <p>Version $version</p>
  </div>
</body>
</html>
""")


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/")
def index():
    version = os.environ.get("APP_VERSION", "dev")
    color = os.environ.get("APP_COLOR", "#8250df")
    return PAGE.substitute(version=version, color=color)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
