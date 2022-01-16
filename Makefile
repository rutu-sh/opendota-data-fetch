SOURCE_DIR=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VERSION=v2

N_PLAYERS=5
HERO_JSON_PATH=${SOURCE_DIR}/data/heroes/hero_data.json
PLAYER_JSON_PATH=${SOURCE_DIR}/data/players/player_data.json 
PLAYER_HERO_JSON_PATH=${SOURCE_DIR}/data/player_hero/player_hero_data.json
HERO_METADATA_JSON_PATH=${SOURCE_DIR}/data/heroes/hero_metadata.json
HERO_ROLE_JSON_PATH=${SOURCE_DIR}/data/heroes/hero_role_data.json


setup:
	@echo ${SOURCE_DIR}
	@echo installing requirements
	pip3 install -r ${SOURCE_DIR}/requirements.txt

create-dirs:
	@echo "\ncreating required directories"
	mkdir -p ${SOURCE_DIR}/data
	mkdir -p ${SOURCE_DIR}/data/heroes
	mkdir -p ${SOURCE_DIR}/data/players
	mkdir -p ${SOURCE_DIR}/data/player_hero
	@echo "\nCreated required directories"

fetch-hero-data:
	@echo "\nFetching hero stats"
	python3 ${SOURCE_DIR}/${VERSION}/feature-fetch/fetch_hero_features.py  --output-path ${HERO_JSON_PATH}
	@echo "\nFetched hero stats"

fetch-player-data:
	@echo "\nFetch players data"
	python3 ${SOURCE_DIR}/${VERSION}/feature-fetch/fetch_player_features.py  --output-path ${PLAYER_JSON_PATH} --n-players ${N_PLAYERS}
	@echo "\nFetched players data"

fetch-player-hero-data:
	@echo "\nFetching player-hero data"
	python3 ${SOURCE_DIR}/${VERSION}/feature-fetch/fetch_player_hero_features.py  --heroes-json-path ${HERO_JSON_PATH} --players-json-path ${PLAYER_JSON_PATH} --output-path ${PLAYER_HERO_JSON_PATH} --n-players 10
	@echo "\nFetched player-hero data"

fetch-hero-metadata:
	@echo "\nFetching hero metadata"
	python3 ${SOURCE_DIR}/${VERSION}/feature-fetch/fetch_hero_metadata.py --output-path ${HERO_METADATA_JSON_PATH}
	@echo "\nFetched hero metadata"

fetch-hero-role-data:
	@echo "\nFetching hero-role-data"
	python3 ${SOURCE_DIR}/${VERSION}/feature-fetch/fetch_hero_role_labels.py --heroes-json-path ${HERO_METADATA_JSON_PATH} --output-path ${HERO_ROLE_JSON_PATH}
	@echo "\nFetched hero-role-data"

fetch-all-data:

	@echo "\nFetching all data"

	$(MAKE) create-dirs
	$(MAKE) fetch-hero-data
	$(MAKE) fetch-hero-metadata
	$(MAKE) fetch-player-data
	${MAKE} fetch-hero-role-data

	@echo "\nFinished fetching all data"
