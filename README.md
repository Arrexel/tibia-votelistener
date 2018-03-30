<p align="center">
  <img width="600" height="194" src="https://otservers.org/img/votelistener.png">
</p>

# How it works
tibia-votelistener is a standalone program that runs on the same machine as your Tibia server. It listens for vote notifications from [otservers.org](https://otservers.org), and then rewards the player who voted.

# Download
- Windows: unreleased
- Linux: unreleased
- Cross-platform (Python): [src/VoteListener.py](https://github.com/Arrexel/tibia-votelistener/blob/master/src/VoteListener.py)

# Installation
Installation is very easy. Simply run the executable file (or if using the Python script, run it with `python VoteListener.py`) and a `VoteListener.ini` file will be generated in the same folder.

## Configuring VoteListener.ini

Set the language of the vote listener. `en` for English and `pr` for Portuguese.
```
[LANGUAGE]
lang = en
```
This is the IP and Port the vote listener will use. Normally you will want to enter your public IP address (not localhost or 127.0.0.1). The key can be obtained from your [otservers.org](https://otservers.org) control panel.
```
[VOTE LISTENER]
ip = 192.168.204.161
port = 7272
key = YOUR_KEY_HERE
```

Enter your Tibia server database connection information. A table named `player_votes` will be created automatically and used to store votes. If you are not running multiple servers on the same machine, leave the `table_prefix` blank.
```
[TIBIA DATABASE]
username = root
password = toor
database = tibia
ip = 127.0.0.1
port = 3306
table_prefix =
```


## Adding the Lua script
Open `data/talkactions/talkactions.xml` and add the following line.
```
<talkaction words="!vote" script="votelistener.lua" />
```

Create the file `data/talkactions/scripts/votelistener.lua` and add the following code to it. This script allows users to check for queued vote rewards using the `!vote` command, and also handles which rewards the player will receive. If the player does not have any vote rewards queued, they will be given a link to vote for the server.

```
function giveReward(player)
    -- Enter code here for rewards
    -- Refer to the Github readme for examples
    -- https://github.com/Arrexel/tibia-votelistener
end

function onSay(player, words, param)
	local resultId = db.storeQuery("SELECT `votes` FROM `player_votes` WHERE `name` = " .. db.escapeString(player:getName()))
	if resultId == false then
		return false
	end

	local votes = result.getNumber(resultId, "votes")
	result.free(resultId)

	if votes == 0 then
        player:sendTextMessage(MESSAGE_EVENT_ADVANCE, "You do not have any pending vote rewards.")
        player:sendTextMessage(MESSAGE_EVENT_ADVANCE, "To vote, go to https://otservers.org/en/vote/YOUR_SERVER_ID_HERE")
		return false
	end
    
    db.query("UPDATE `player_votes` SET `votes` = 0 WHERE `name` = " .. db.escapeString(player:getName()))
    
    for vote=0,votes,1
    do
        giveReward(player)
        print("> " .. player:getName() .. " voted!")
        for _, targetPlayer in ipairs(Game.getPlayers()) do
            targetPlayer:sendPrivateMessage(MESSAGE_EVENT_ADVANCE, player:getName() .. " received rewards for voting!")
            targetPlayer:sendPrivateMessage(MESSAGE_EVENT_ADVANCE, "Say !vote for awesome rewards.")
        end
    end

	return false
end
```

## Customizing vote rewards
Customizing vote rewards is very easy. Simply add the rewards to the `giveReward()` function. 

### Example (give items)
Gives the player 10x earth. Refer to `data/items/items.xml` for a list of all item IDs.
```
function giveReward(player)
    player:addItem(101, 10)
end
```
