# Torrent app
This is my pet-project that allows to search for torrents using [Torrent-api-py](https://github.com/Ryuk-me/Torrent-Api-py) and then schedule download using transmisson RPC protocol.

## How to run
* Run `pip install -r requirements.txt`
* Have [Torrent-api-py](https://github.com/Ryuk-me/Torrent-Api-py) running locally or use already hosted solution
* Update `main.py` and replace configuration for transmission and `torrent-api-py` to your values
* Run `python3 main.py` to start the app
* Visit `localhost:8443` and search what you need

## Running in docker
```bash
docker build -t torrent-app ./
docker run -d -p 8443:8443 -e TR_HOST=transmisson_rpc_host \
TR_PORT=transmission_rpc_port \
TR_USER=transmission_rpc_user \
TR_PASS=transmission_rpc_pass \
TORRENT_API_URL=torrent_api_url
```

## Available paths
* `:8443/` - home page with search prompt
* `:8443/search` - page with search results
* `:8443/download` - downloads specified torrent share
* `:8443/downloads` - displays status of all active torrent downloads

## TODO
* Add more functionality
  * Add ability to specify default path for downloads
  * Add ability to specift path per download
  * Add telegram integration
    * Add subscription feature to check for any results for given query
    * Schedule downloads of subscribed queries
    * Notification about download status

* Clean code
