from disco.bot import Bot, Plugin


class MiscCommands(Plugin):

    @Plugin.command('echo', '<content:str...>')
    def on_echo_command(self, event, content):
        '''echo <Content>
        Repeats back what the user passes as an argument.'''
        event.msg.reply(content)

    @Plugin.command('invite')
    def on_invite_command(self, event):
        '''invite
        Gives an invite link to add the bot to a server'''
        event.msg.reply('https://discordapp.com/oauth2/authorize?client_id=252880131540910080&scope=bot&permissions=0')

    @Plugin.command('git')
    def on_git_command(self, event):
        '''git
        Gives a link to the bot's git repo'''
        event.msg.reply('https://github.com/4Kaylum/Spar.cli/')

    @Plugin.command('ev', '<content:str...>')
    def on_ev_command(self, event, content):
        '''ev <Content>
        Python evaluates the content of the message passed as parameters'''
        event.msg.reply('```\n{}```'.format(eval(content)))
