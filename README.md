# nordvpn-wireguard-extractor
This python script will extract all private keys and server names from the nordvpn api and will generate wireguard config files.

## Config file
The config file is straightforward. You put in your privatekey (which you got by fillowing [this Link](https://gist.github.com/bluewalk/7b3db071c488c82c604baf76a42eaad3) ), your outputdir and check the rest (By default that should be fine).
The Limit may be insteresting, if you dont want to fetch all servers.
Then you can just run the script and all the config files are put into the corresponding folder.
