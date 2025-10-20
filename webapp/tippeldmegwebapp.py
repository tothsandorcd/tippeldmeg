from flask import Flask, request, render_template_string, Response
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(".env")

USERNAME = os.getenv("USERNAME")
PASSWORD_HASH = os.getenv("PASSWORD_HASH")

if not USERNAME or not PASSWORD_HASH:
    raise SystemExit("Missing USERNAME or PASSWORD_HASH in .env")

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
  <body>
    <h1>Run Script</h1>
    <form action="/run" method="post">
      <button type="submit">Execute Script</button>
    </form>
  </body>
</html>
"""

def authenticate():
    return Response("Authentication required", 401,
                    {"WWW-Authenticate": 'Basic realm="Login Required"'})

@app.before_request
def require_auth():
    auth = request.authorization
    if not auth or auth.username != USERNAME or not check_password_hash(PASSWORD_HASH, auth.password):
        return authenticate()

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/run", methods=["POST"])
def run_script():
    import subprocess
    result = subprocess.run(["./myscript.sh"], capture_output=True, text=True)
    return f"<pre>{result.stdout or '(no output)'}{result.stderr}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=21407, ssl_context=('/home/sasa/certs/cert.pem','/home/sasa/certs/key.pem'))
