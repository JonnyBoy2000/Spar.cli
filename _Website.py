from json import loads, dumps
from flask import Flask, request
from praw import Reddit
from Cogs.Utils.Configs import getTokens
app = Flask(__name__)


# Used to validate refresh tokens
tokens = getTokens()['Reddit']
redditFull = Reddit(
    client_id=tokens['ID'],
    client_secret=tokens['Secret'],
    user_agent=tokens['User Agent'],
    redirect_uri=tokens['Redirect URI']
)


@app.route('/')
def indexPage():
    return 'Yup, it works.'


# Used as part of the webserver of the bot
@app.route('/SparCli/reddit/callback', methods=['GET'])
def result():

    # Get the passed arguments
    state = request.args.get('state')
    jState = loads(state)
    userID= jState['DiscordID']
    UUID = jState['UUID']
    userAuth = request.args.get('code')

    # Set the default output
    z = {'Success':True, 'Discord ID':userID, 'Reddit Auth':userAuth, 'Error': None, 'User': None}

    # Look at the stored UUIDs
    with open('redditInstances.json') as a:
        q = loads(a.read())

    # Compare the given UUID with the stored one
    try:
        if q['UUIDs'][userID] == UUID:
            del q['UUIDs'][userID]
        else:
            raise KeyError
    except KeyError:
        z['Success'] = False 
        z['Error'] = 'Invalid UUID auth.'
        return dumps(z)

    # Get the refresh token
    redditUser = redditFull
    refreshCode = redditUser.auth.authorize(userAuth)
    userPerson = redditUser.user.me().name

    # Save the refresh token
    q['Tokens'][userID] = refreshCode
    with open('redditInstances.json', 'w') as a:
        a.write(dumps(q, indent=4))

    # Return all to the user
    z['User'] = userPerson
    return dumps(z)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # app.run()

