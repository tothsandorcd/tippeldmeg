from flask import Flask, request, render_template_string, Response
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os
import subprocess


# Load environment variables
load_dotenv(".env")

USERNAME = os.getenv("USERNAME")
PASSWORD_HASH = os.getenv("PASSWORD_HASH")

if not USERNAME or not PASSWORD_HASH:
    raise SystemExit("Missing USERNAME or PASSWORD_HASH in .env")

app = Flask(__name__)

def getStartPage():
   HTML = """
   <!doctype html>
   <html>
     <body>
      <h1>Run or Schedule Script</h1>
      <form action="/run" method="post">
        <label>Execution:</label><br>
        <input type="radio" name="day_option" value="now" checked> Now (immediate)<br>
        <input type="radio" name="day_option" value="Today"> Today<br>
        <input type="radio" name="day_option" value="Mon"> Monday<br>
        <input type="radio" name="day_option" value="Tue"> Tuesday<br>
        <input type="radio" name="day_option" value="Wed"> Wednesday<br>
        <input type="radio" name="day_option" value="Thu"> Thursday<br>
        <input type="radio" name="day_option" value="Fri"> Friday<br>
        <input type="radio" name="day_option" value="Sat"> Saturday<br>
        <input type="radio" name="day_option" value="Sun"> Sunday<br><br>
     
        <label>Hour (0-23):</label>
        <select name="hour">
   """

   for h in range(24):
     HTML += f'            <option value="{h:02d}:02">{h:02d}:02</option>\n'

   HTML += """
        </select><br><br>
        <button type="submit">Schedule/Run Script</button>
      </form>
      <br><br>"""

   result = subprocess.run(["atq"], capture_output=True, text=True)

   outputlines = ""
   
   for line in result.stdout.splitlines():
       parts = line.split()
       if len(parts) >= 6:
           outputlines = outputlines + " ".join(parts[1:5]) + "<br>"
       else:
           outputlines = outputlines + line
           


   HTML += f"schedules: <br>{outputlines} {result.stderr}"

   HTML += """
      <br>
     </body>
   </html>
   """
   
   return HTML

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
    return render_template_string(getStartPage())

@app.route("/run", methods=["POST"])
def run_script():

    day_option = request.form.get("day_option")
    hour = request.form.get("hour")
    
    if day_option == "now":
            result = subprocess.run(["./myscript.sh"], capture_output=True, text=True)
#            result = subprocess.run(["date >> myscript.log"], shell=True, capture_output=True, text=True)
            return f"<h2>Executed immediately:</h2><pre>{result.stdout or '(no output)'}\n{result.stderr}</pre>"
    else:
                  if day_option == "Today":
                        result = subprocess.run([f'echo "cd /home/sasa/Documents/repo/tippeldmeg/webapp && ./myscript.sh >> myscript.log 2>&1" | at {hour}'], shell=True, capture_output=True, text=True)
#                        result = subprocess.run([f'echo "cd /home/sasa/Documents/repo/tippeldmeg/webapp && date >> myscript.log" | at {hour}'], shell=True, capture_output=True, text=True)
                        return f"<h2>Scheduled today:</h2><pre>{hour}. Result {result}\n</pre>"
                  else:
                        result = subprocess.run([f'echo "cd /home/sasa/Documents/repo/tippeldmeg/webapp && ./myscript.sh >> myscript.log 2>&1" | at {hour} {day_option}'], shell=True, capture_output=True, text=True)
#                        result = subprocess.run([f'echo "cd /home/sasa/Documents/repo/tippeldmeg/webapp && date >> myscript.log" | at {hour} {day_option}'], shell=True, capture_output=True, text=True)
                        return f"<h2>Scheduled:</h2><pre>{hour} {day_option}. Result {result}\n</pre>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=21407, ssl_context=('/home/sasa/certs/cert.pem','/home/sasa/certs/key.pem'))

