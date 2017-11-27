import os
import json
import random
import shlex
from flask import Flask, Blueprint, Response, request

_blueprint = Blueprint("Quotes", __name__)
_path = "./quotes/"

def _get_var(name, default=None):
    try:
        return os.environ[name]
    except:
        return default


def _parse(string):
    return list(shlex.shlex(string))

def _response(status, body):
    return Response(response=json.dumps(body), mimetype="application/json", status=status)


def _reply_slack(text, attachment=None, private=False):
    response = {
        "response_type": "in_channel" if private else "ephemeral",
        "text": text,
    }
    if attachment is not None:
        response["attachments"] = [{
            "text": attachment
        }]
    return _response(200, response)


def _send_quote(name, text):
    return _reply_slack(name, text, True)


def _get_form():
    return request.form
    

def _get_folder():
    try:
        return request.args.get("folder")
    except:
        return None


def _get_action():
    form = _get_form()
    if "text" in form.keys() and len(form["text"]):
        args = _parse(form["text"])
        if args[0] in ["list", "show", "help"]:
            return (args[0], None if len(args) is 1 else args[1])
        else:
            return ("error", args[0])
    return (None, None)


def _get_help():
    return """Valid commands:
    <nothing> : Send a random quote
    list : List available quotes
    show <name> : Show specified quote
    help : Show this message"""



def _get_quote_list(folder):
    path = _path + folder
    return [f.replace(".quote", "") for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def _get_quote(folder, name=None):
    quote_list = _get_quote_list(folder)
    quote_name = random.choice(quote_list) if name is None else name
    if quote_name not in quote_list:
        return _reply_slack("Quote " + quote_name + " not found")
    quote_path = _path + folder + "/" + quote_name + ".quote"
    quote = ""
    with open(quote_path, "r") as quote_file:
        quote = quote_file.read()
    quote_title = "Quote : " + quote_name
    return _reply_slack(quote_title, quote, True)


@_blueprint.route("/", methods=["GET", "POST"])
def get_quote():
    folder = _get_folder()
    if folder is None:
        return _response(404, {"error": "No folder"})
    action = _get_action()
    print(action[0])
    if action[0] == "error":
        return _reply_slack(action[1] + " is not a valid command", _get_help())
    elif action[0] == "help":
        return _reply_slack("Need help ?", _get_help())
    elif action[0] == "list":
        return _reply_slack("Available quotes", ", ".join(_get_quote_list(folder)))
    else:
        return _get_quote(folder, None if action[0] != "show" else action[1])


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(_blueprint)
    app.run(port=int(_get_var("QUOTER_PORT", 80)), host="0.0.0.0")

