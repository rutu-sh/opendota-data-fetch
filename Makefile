SOURCE_DIR=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VERSION=v2

N_PLAYERS=10

FEATURE_FETCH=${SOURCE_DIR}/${VERSION}/feature-fetch
FEATURE_GEN=${SOURCE_DIR}/${VERSION}/feature-gen

DATA_PATH=${SOURCE_DIR}/data
FEATURE_PATH=${SOURCE_DIR}/feature

HERO_JSON_PATH=${DATA_PATH}/heroes/hero_data.json
PLAYER_JSON_PATH=${DATA_PATH}/players/player_data.json 
PLAYER_HERO_JSON_PATH=${DATA_PATH}/player_hero/player_hero_data.json
HERO_METADATA_JSON_PATH=${DATA_PATH}/heroes/hero_metadata.json
HERO_ROLE_JSON_PATH=${DATA_PATH}/heroes/hero_role_data.json

HERO_FEATURE_PATH=${FEATURE_PATH}/heroes/hero_features.csv
PLAYER_FEATURE_PATH=${FEATURE_PATH}/players/player_features.csv
ROLE_FEATURE_PATH=${FEATURE_PATH}/roles/role_features.csv
PLAYER_HERO_EDGE_PATH=${FEATURE_PATH}/player_hero/player_hero_edge.csv
HERO_ROLE_EDGE_PATH=${FEATURE_PATH}/hero_role/hero_role_edge.csv


create-dirs:
	@echo "\ncreating required directories"
	mkdir -p ${DATA_PATH}
	mkdir -p ${DATA_PATH}/heroes
	mkdir -p ${DATA_PATH}/players
	mkdir -p ${DATA_PATH}/player_hero
	mkdir -p ${FEATURE_PATH}/heroes
	mkdir -p ${FEATURE_PATH}/players
	mkdir -p ${FEATURE_PATH}/roles
	mkdir -p ${FEATURE_PATH}/player_hero
	mkdir -p ${FEATURE_PATH}/hero_role
	@echo "\nCreated required directories"

setup:
	@echo ${SOURCE_DIR}
	@echo installing requirements
	pip3 install -r ${SOURCE_DIR}/requirements.txt
	$(MAKE) create-dirs

fetch-hero-data:
	@echo "\nFetching hero stats"
	python3 ${FEATURE_FETCH}/fetch_hero_features.py  --output-path ${HERO_JSON_PATH}
	@echo "\nFetched hero stats"

fetch-player-data:
	@echo "\nFetch players data"
	python3 ${FEATURE_FETCH}/fetch_player_features.py  --output-path ${PLAYER_JSON_PATH} --n-players ${N_PLAYERS}
	@echo "\nFetched players data"

fetch-player-hero-data:
	@echo "\nFetching player-hero data"
	python3 ${FEATURE_FETCH}/fetch_player_hero_features.py  --heroes-json-path ${HERO_JSON_PATH} --players-json-path ${PLAYER_JSON_PATH} --output-path ${PLAYER_HERO_JSON_PATH} --n-players ${N_PLAYERS}
	@echo "\nFetched player-hero data"

fetch-hero-metadata:
	@echo "\nFetching hero metadata"
	python3 ${FEATURE_FETCH}/fetch_hero_metadata.py --output-path ${HERO_METADATA_JSON_PATH}
	@echo "\nFetched hero metadata"

fetch-hero-role-data:
	@echo "\nFetching hero-role-data"
	python3 ${FEATURE_FETCH}/fetch_hero_role_labels.py --heroes-json-path ${HERO_METADATA_JSON_PATH} --output-path ${HERO_ROLE_JSON_PATH}
	@echo "\nFetched hero-role-data"

fetch-all-data:

	@echo "\nFetching all data"

	$(MAKE) create-dirs
	$(MAKE) fetch-hero-data
	$(MAKE) fetch-hero-metadata
	$(MAKE) fetch-player-data
	$(MAKE) fetch-hero-role-data
	$(MAKE) fetch-player-hero-data

	@echo "\nFinished fetching all data"

generate-hero-features:
	@echo "\nGenerating Hero Features"
	python3 ${FEATURE_GEN}/generate_hero_features.py --heroes-data-json ${HERO_JSON_PATH} --output-path ${HERO_FEATURE_PATH}
	@echo "\nGenerated hero features"


generate-player-features:
	@echo "\nGenerating Player Features"
	python3 ${FEATURE_GEN}/generate_players_features.py --players-data-json ${PLAYER_JSON_PATH} --output-path ${PLAYER_FEATURE_PATH}
	@echo "\nGenerated player features"

generate-role-features:
	@echo "\nGenerating role Features"
	python3 ${FEATURE_GEN}/generate_role_features.py --output-path ${ROLE_FEATURE_PATH}
	@echo "\nGenerated role features"

generate-hero-role-edge-features:
	@echo "\nGenerating hero-role edge features"
	python3 ${FEATURE_GEN}/generate_hero_role_features.py --heroes-data-json ${HERO_JSON_PATH} --output-path ${HERO_ROLE_EDGE_PATH}
	@echo "\nGenerated hero-role edge features"

generate-player-hero-edge-features:
	@echo "\nGenerating player-hero edge features"
	python3 ${FEATURE_GEN}/generate_player_hero_features.py --heroes-data-json ${HERO_JSON_PATH} --player-hero-data-json ${PLAYER_HERO_JSON_PATH} --output-path ${PLAYER_HERO_EDGE_PATH}
	@echo "\nGenerated hero-role edge features"

