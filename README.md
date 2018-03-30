# How it works
tibia-votelistener is a standalone program that runs on the same machine as your Tibia server. It listens for vote notifications from [otservers.org](https://otservers.org), and then rewards the player who voted.

# Download
- Windows: unreleased
- Linux: unreleased
- Cross-platform (Python): [src/VoteListener.py](https://github.com/Arrexel/tibia-votelistener/blob/master/src/VoteListener.py)

# Installation
Installation is very easy. Simply run the executable file (or if using the Python script, run it with `python VoteListener.py`) and a `VoteListener.ini` file will be generated in the same folder.

## Configuring VoteListener.ini

```
[LANGUAGE]
lang = en
```
Set the language of the vote listener. `en` for English and `pr` for Portuguese.

```
[VOTE LISTENER]
ip = 192.168.204.161
port = 7272
key = YOUR_KEY_HERE
```
This is the IP and Port the vote listener will use. Normally you will want to enter your public IP address (not localhost or 127.0.0.1). The key can be obtained from your [otservers.org](https://otservers.org) control panel.

```
[TIBIA DATABASE]
username = root
password = toor
database = tibia
ip = 127.0.0.1
port = 3306
table_prefix =
```

Enter your Tibia server database connection information. A table named `player_votes` will be created automatically and used to store votes. If you are not running multiple servers on the same machine, leave the `table_prefix` blank.
