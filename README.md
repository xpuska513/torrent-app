# Torrent app
This is my pet-project that allows to search for torrents using [Torrent-api-py](https://github.com/Ryuk-me/Torrent-Api-py) and then schedule download using transmisson RPC protocol.

## How to run
* Run `pip install -r requirements.txt`
* Have [Torrent-api-py](https://github.com/Ryuk-me/Torrent-Api-py) running locally or use already hosted solution
* Update `main.py` and replace configuration for transmission and `torrent-api-py` to your values
* Run `python3 main.py` to start the app
* Visit `localhost:8443` and search what you need

## Available paths
* `:8443/` - home page with search prompt
* `:8443/search` - page with search results
* `:8443/download` - downloads specified torrent share
* `:8443/downloads` - displays status of all active torrent downloads