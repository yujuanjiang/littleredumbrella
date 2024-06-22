from flask import Flask, request, url_for, redirect, render_template, jsonify, make_response, current_app
import json
import os

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config.from_prefixed_env()
config_path = app.root_path + "/config.json"

def get_site_config():
    site_config = {}
    in_file = open(config_path, mode='r', encoding='utf-8')
    site_config = json.loads( in_file.read() )
    in_file.close()
    return site_config

@app.route("/index")
def home():
    site_config = get_site_config()
    return render_template('index.html', status=site_config.get("STATUS"), announcement=site_config.get("ANNOUNCEMENT"))

@app.route("/manage", methods = ['GET', 'POST'])
def manage():
    site_config = get_site_config()

    if request.method == 'GET':
        in_file = open(config_path, mode='r', encoding='utf-8')
        site_config = json.loads( in_file.read() )
        in_file.close()

        auth = request.authorization
        if auth and auth.username == site_config.get("SITE_USER") and auth.password == site_config.get("SITE_PWD"):	
            return render_template('manage.html', status=site_config.get("STATUS"), announcement=site_config.get("ANNOUNCEMENT"))	
        return make_response("<h1>Access denied!</h1>", 401, {'www-Authenticate':'Basic realm="Login required!"'})
    else:
        site_config["STATUS"]=request.form.get("status")
        site_config["ANNOUNCEMENT"]=request.form.get("announcement")
 
        out_file = open(config_path, "w")
        out_file.write(json.dumps(site_config))
        out_file.close()
        return redirect('/manage')
	

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8000, debug=True)

    except Exception as e:
        print("App startup failed!\n")
        print(exception(e))


