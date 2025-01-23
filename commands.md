# Telegram File Bot Commands

## General Commands

*   `/start`: Starts the bot.
*   `/getid`: Gets your chat ID.
*   `/help`: Shows help message.

## Channel Commands

*   `/setlogchannel`: Sets the log channel.
*   `/setfailchannel`: Sets the fail channel.
*   `/viewchannels`: Views configured channels.

## File Commands

*   `/thumbnailchange`: Changes file thumbnail.
*   `/filenamechange`: Starts the file renaming process.
*   `/rename_process <filename> <metadata>`: Renames the file using the selected format.
* `/setsource`: Sets the source directory for files.
* `/settarget`: Sets the target directory for files.
* `/work <start-end(optional)>`: Starts file processing (with optional range). Example: `/work 10-20` or `/work` for all.
* `/end`: Ends file processing.
* `/processstatus`: Shows file processing status.

## User Management

*   `/adduser <user_id>`: Adds a user.
*   `/userlist`: Lists all users.
*   `/removeuser <user_id>`: Removes a user.
*   `/setlimit <user_id> <limit>`: Sets user limit.

## API Management

*   `/addapi <api_key>`: Adds an API key.
*   `/apilist`: Lists all API keys.
*   `/removeapi <api_key>`: Removes an API key.
