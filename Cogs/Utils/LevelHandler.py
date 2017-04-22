from time import time
from random import randint
from .Configs import getMoneyJson, saveMoneyJson


class LevelHandler(object):
    '''
    A hander for every user's money on a server
    '''

    def __init__(self):
        # UserID : LevelUser keypair
        self.users = {}

    def increment(self, message):
        '''
        Used to increment a user's exp globally
        '''

        userID = message.author.id
        if userID not in self.users:
            self.users[userID] = LevelUser(userID)
        self.users[userID].increment(message.server)


class LevelUser(object):
    '''
    A handler for money on any given users server
    '''

    def __init__(self, userID):
        self.userID = userID 
        self.lastAdded = {}

    def increment(self, server):
        if server == None:
            return

        serverID = server.id
        increment = randint(0, 50)

        if self.lastAdded.get(serverID, 0) < time() + 60:
            moneyData = getMoneyJson(serverID)
            currentMoney = moneyData.get(self.userID, 0)
            currentMoney += increment
            moneyData[self.userID] = currentMoney
            saveMoneyJson(serverID, moneyData)

            moneyData = getMoneyJson('Everyone')
            currentMoney = moneyData.get(self.userID, 0)
            currentMoney += increment
            moneyData[self.userID] = currentMoney
            saveMoneyJson('Everyone', moneyData)

            self.lastAdded[serverID] = time()
