# opendota-data-fetch
repo for fetching and processing data from opendota 

# Usage
## Install packages and create required dirs
```
make setup
```

## Create required dirs
```
make create-dirs
```

## Fetch all data
```
make fetch-all-data
```

## Generate all features
```
make generate-all-features
```

## Fetch hero data
```
make fetch-hero-data
```

## Fetch player data
```
make fetch-player-data
```

## Fetch player-hero data
```
make fetch-player-hero-data
```

## Fetch hero-metadata
```
make fetch-hero-metadata
```

## Fetch hero-role-data
```
make fetch-hero-role-data
```

## Generate role features
```
make generate-role-features
```

## Generate hero features
```
make generate-hero-features
```

## Generate player features
```
make generate-player-features
```

## Generate hero-role edge features
```
make generate-hero-role-edge-features
```

## Generate player-hero edge features
```
make generate-player-hero-edge-features
```


# Embedding Generation Checklist

- [x] Fetch pro-players data
- [x] Fetch hero data
- [x] Fetch role data
- [ ] Fetch player-hero relations
- [x] Fetch hero-role relations
- [x] Embedding generation POC
- [ ] Verify embeddings
- [ ] Experiment with different PCA
- [ ] Experiment with different metapaths
- [ ] Normalize all features (StandardScaler)
- [ ] Isolate and visualize embeddings for each type of node (player,hero,role)
- [ ] Generate embeddings with Teams and Leagues as nodes in the Graph
- [ ] Compare embeddings in presence/absence of nodes/node_features


# Research Paper Checklist

- [ ] Kal dekhenge
- [ ] Make repo public


# Ideas

- [ ] Can be used to compare playing-style of Teams ? 
- [ ] Try out with heterogeneous versions of GraphSAGE, GAT etc ? 
