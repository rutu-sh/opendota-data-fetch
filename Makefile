setup:
	@echo installing requirements
	pip3 install -r requirements.txt

fetch-data:
	@echo "\ncreating required directories"
	mkdir -p data
	mkdir -p data/features
	mkdir -p data/heroes
	mkdir -p data/roles

	@echo "\nFetching hero stats"
	python3 fetch_hero_stats.py

	@echo "\nGenerating roles data"
	python3 generate_roles_data.py

	@echo "\nGenerating heroes csv"
	python3 generate_hero_csv.py

	@echo "\nGenerating hero-role-csv"
	python3 generate_hero_role_csv.py

	@echo "\nFinished make fetch-data"