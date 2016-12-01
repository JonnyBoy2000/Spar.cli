from json import loads, dumps
from os.path import realpath, dirname
workingDirectory = dirname(realpath(__file__))


def getServerJson(serverID):
    '''Returns the JSON config for a server'''

    try:
        with open(workingDirectory + '\\..\\ServerConfigs\\{}.json'.format(serverID)) as a:
            jsonData = loads(a.read())
    except FileNotFoundError:
        with open(workingDirectory + '\\..\\\\ServerConfigs\\Default.json') as a:
            jsonData = loads(a.read())
    return jsonData


def saveServerJson(serverID, jsonData):
    '''Writes a JSON file into savedata'''

    with open(workingDirectory + '\\..\\ServerConfigs\\{}.json'.format(serverID), 'w') as a:
        a.write(dumps(jsonData, indent=4))


def fixJson(inputDictionary, referenceDictionary=getServerJson('Default')):
    '''Fixes an input dictionary with a reference'''

    # Go through the reference dictionary
    for i in referenceDictionary:

        # Sees if the different objects exist in the reference
        if type(referenceDictionary[i]) == dict:
            if i not in inputDictionary:
                inputDictionary[i] = referenceDictionary[i]
            else:

                # If it's a JSON, it'll have to reccur through the function
                inputDictionary[i] = fixJson(
                    inputDictionary[i], referenceDictionary[i])
        else:
            if i in inputDictionary:
                pass
            else:
                inputDictionary[i] = referenceDictionary[i]
    return inputDictionary