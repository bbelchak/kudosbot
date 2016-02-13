import os
import re
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config.from_envvar('SLACK_SLASH_TOKEN')


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
    if token != app.config.SLACK_SLASH_TOKEN:
        return render_template('404.html'), 400
    kudos_user = re.search('(?@\w+) ')
    if not kudos_user:
        return "I'm sorry, I didn't hear a name in there. Try again?"
    response = 'Thanks, I\'ve given kudos to %s' % kudos_user
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
