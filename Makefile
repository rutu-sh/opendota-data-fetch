SOURCE_DIR=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VERSION=v2

test:
	echo 
setup:
	@echo ${SOURCE_DIR}
	@echo installing requirements
	pip3 install -r ${SOURCE_DIR}/requirements.txt

create-dirs:
	@echo "\ncreating required directories"
	mkdir -p ${SOURCE_DIR}/data
	mkdir -p ${SOURCE_DIR}/data/heroes
	mkdir -p ${SOURCE_DIR}/data/players
	@echo "\nCreated required directories"

fetch-hero-data:
	@echo "\nFetching hero stats"
	python3 ${SOURCE_DIR}/${VERSION}/feature-fetch/fetch_hero_features.py  --output-path ${SOURCE_DIR}/data/heroes/hero_data.json
	@echo "\nFetched hero stats"

fetch-player-data:
	@echo "\nFetch players data"
	python3 ${SOURCE_DIR}/${VERSION}/feature-fetch/fetch_player_features.py  --output-path ${SOURCE_DIR}/data/players/player_data.json --n-players 5
	@echo "\nFetched players data"

fetch-all-data:

	@echo "\nFetching all data"

	$(MAKE) create-dirs
	$(MAKE) fetch-hero-data
	$(MAKE) fetch-player-data

	@echo "\nFinished fetching all data"
