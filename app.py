import os
import re
import sys
import logging
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config['SLACK_SLASH_TOKEN'] = os.environ.get('SLACK_SLASH_TOKEN')
app.config['SLACK_KUDOS_CHANNEL'] = os.environ.get('SLACK_KUDOS_CHANNEL', '#general')
app.config['SLACK_WEBHOOK_URL'] = os.environ.get('SLACK_WEBHOOK_URL')

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/give-kudos', methods=['POST'])
def give_kudos():
    token = request.form['token']
    if token != app.config['SLACK_SLASH_TOKEN']:
        return render_template('404.html'), 400
    parsed = re.search(r'(@\w+)\s+(\w.*$)', request.form['text'])
    kudos_user, message = parsed.group(1, 2)
    if not kudos_user:
        return "I'm sorry, I didn't hear a name in there. Try again?"
    post_json = {
        "channel": app.config['SLACK_KUDOS_CHANNEL'],
        "attachments": [{
            "fallback": "@%s has given %s kudos! \"%s\"" % (request.form['user_name'], kudos_user, message),
            "pretext": "@%s has given %s kudos!" % (request.form['user_name'], kudos_user),
            "color": "good",
            "fields": [
                {
                    "title": "Kudos!",
                    "value": message,
                    "short": False
                }
            ]
        }],
        "link_names": 1
    }
    resp = requests.post(app.config['SLACK_WEBHOOK_URL'], json=post_json)
    response = "Thanks, I've given kudos to %s for %s." % (kudos_user, message)
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
