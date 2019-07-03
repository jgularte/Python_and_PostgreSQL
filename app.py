from flask import Flask, render_template, session, redirect, request, url_for, g
from utility import oauth
from classes.screen_name import UserScreenName
from classes.database import Database
import requests

# Initialize the database and set up the consumer object.
Database.initialize(user='postgres', password='francis24$', database='learning', host='localhost')

app = Flask(__name__)
app.secret_key = '1234'


# g is a global variable available throughout the entire request
@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = UserScreenName.load_db_screen_name(session['screen_name'])


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():

    # check if user is logged in
    if 'screen_name' in session:
        return redirect(url_for('profile'))

    # get request token; store it in the session
    request_token = oauth.get_request_token()
    session['request_token'] = request_token

    # redirect the user to twitter so the confirm authorization
    return redirect(oauth.get_oauth_verifier_url(request_token))


@app.route('/logout/twitter')
def twitter_logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/auth/twitter')
def twitter_auth():

    # get oauth verifier
    oauth_verifier = request.args.get('oauth_verifier')

    # get access token
    access_token = oauth.get_access_token(session['request_token'], oauth_verifier)

    # see if screen_name is in database
    user = UserScreenName.load_db_screen_name(access_token['screen_name'])
    if not user:

        # if not, create user and save it to database
        user = UserScreenName(access_token['screen_name'],
                              access_token['oauth_token'],
                              access_token['oauth_token_secret'])
        user.save_to_db()

    # add screen_name to session
    session['screen_name'] = user.screen_name
    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)


@app.route('/search')
def search():
    query = request.args.get('q')
    response = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={0}'.format(query))
    tweets = [{'tweet': i['text'], 'label': 'neutral'} for i in response['statuses']]

    for i in tweets:

        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': i['tweet']})
        json_response = r.json()
        label = json_response['label']
        i['label'] = label

    return render_template('search.html', content=tweets)


app.run(port=4995, debug=True)
