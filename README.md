# Spar.cli

This bot is a sequel to my previous Discord bot, [Apple.Py](https://github.com/4Kaylum/Apple.Py). It doesn't (and won't) do all the things that were incorperated into that bot, but rather works as a more admin-friendly bot than a social one.

The command prefix, by default, is set to `;`.

---

## Commands

What follows will be several tables of commands, sorted into categories. The first column is the name of the command, ie what you call in the chat to get it to work.  
The second column is the arguments is takes, if any. If none, the cell will remain blank.  
The third column is a text description of what the command does
The fourth column is the requirements that you will need to be able to run the command, ie if you have to be an admin, or have the manage messages permission, etc.  
The fifth and final column is a list of what aliases the command has.

### Admin

This section covers all of the commands that most servers' moderators will use.

Name|Argument(s)|Description|Requirements|Aliases
---|---|---|---|---
purge|\<Amount of Messages>|This will remove a set amount of messages from a channel|Manage messages|
kick|\<User Mention>|Kicks the mentioned user from the server|Kick|
ban|\<User Mention>|Bans the mentioned user from the server|Ban|

### Config

This section covers all the changes you can make to the server's config file, thus changing how the bot interacts with your server. The different ways it interacts are based on the events that happen within the server, including:

Server Event|Description|Channel Set|Text Set
---|---|---|---
Joins|When a user joins the server| :heavy_check_mark:|:heavy_check_mark:
Leaves|When a user leaves the server|:heavy_check_mark:|:heavy_check_mark:
Bans|When a user is banned|:heavy_check_mark:|:heavy_check_mark:
ChannelUpdate|When a channel is updated|:heavy_multiplication_x:|:heavy_multiplication_x:
ServerUpdate|When a server is updated|:heavy_check_mark:|:heavy_multiplication_x:
Starboard|When a star is added to a message - quotes|:heavy_check_mark:|:heavy_multiplication_x:


Name|Argument(s)|Description|Requirements|Aliases
---|---|---|---|---
set|\<Server Event> \<Channel Mention>|Sets the output text of the server event to the mentioned channel|Admin|
youare|\<Now/Not> \<Role Name/Mention>|Will set which roles the user is allowed to self-assign|Admin|
enable|\<Server Event>|Enables the server event output|Admin|
setup||Goes through all of the different events and allows you to set them graphically|Admin|
disable|\<Server Event>|Disables the server event output|Admin|
prefix|\<Content>|Sets the server's command prefix to whatever you pass as an argument|Admin|setprefix, prefixset

### Internet

This is just fun things that the internet has come up with.

Name|Argument(s)|Description|Requirements|Aliases
---|---|---|---|---
iwolfram|\<Query>|Sends a query to WolframAlpha, returns images||
cat||Gives a random picture of a cat||
pun||Gives a random pun||
wolfram|\<Query>|Sends a query to WolframAlpha, returns text||
c|\<Query>|Sends a query to Cleverbot||
trans|\<Language Shorthand> \<Content...>|Translates whatever you tell it to into a language of your choice. Language shorthand refers to things like `en` and `de`, etc||

### Misc

This is commands that I wanted in the bot, but have nowhere to categorize them into.

Name|Argument(s)|Description|Requirements|Aliases
---|---|---|---|---
git||Outputs a link to this GitHub repo||
info|\<User Mention>|Gives information about the mentioned user||
invite||This will give you a link to invite the bot to your own server||
echo|\<Content...>|Will repeat back whatever you pass as content||
clean|\<Amount> \<User Mention>|Removes the last 50 (default) messages from the mentioned user|Manage Messages|

### Random

Using anything in this category will give you a randomly generated output

Name|Argument(s)|Description|Requirements|Aliases
---|---|---|---|---
coinflip||Returns "heads" or "tails"||

### RoleManagement

The purpose of this category is to make the management of roles a lot easier, regarldess of whether you're at a PC or not

Name|Argument(s)|Description|Requirements|Aliases
---|---|---|---|---
iam|\<Role Name/Mention>|If it's been set to do so, the bot will assign whatever role the user has specified to them||
rolecolour|\<Hex Code> \<Role Name/Mention>|Changes a role's colour to whatever hex code is specified|Manage Roles|rolecolour, changecolour, changerolecolour, changerole, rolecolor, changecolor, changerolecolor

### Tags

These are essentially Simon Says commands - you can set it to say something back to you or evaluate a certain term

Name|Argument(s)|Description|Requirements|Aliases
---|---|---|---|---
tag add||Adds a server-specific tag||t add
tag del||Deletes a server-specific tag||t del
tag|\<Tag Name>|Repeats back a tag to you||t
etag add||Adds a server-specific evaluated tag||et add
etag del||Deletes a server-specific evaluated tag||et del
etag|\<Tag Name>|Repeats back an evaluated tag to you||et
