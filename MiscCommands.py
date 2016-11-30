from disco.bot import Bot, Plugin

class MiscCommands(Plugin):


    @Plugin.command('echo', '<content:str...>')
    def on_echo_command(self, event, content):
        event.msg.reply(content)

    @Plugin.command('invite')
    def on_invite_command(self, event):
        event.msg.reply('https://discordapp.com/oauth2/authorize?client_id=252880131540910080&scope=bot&permissions=0')

