# JSON Visualizer
Json file exportation in order to visualize and manipulate its data easier.

## Dependencies
Development using the last version of python3.
 - dash (and sub-dependencies)
 - dash-cytoscape

## Install
```shell
pip install -r build/requirements.txt
```

## Usage
```shell
python src/app.py
```
Server available as development mode through `localhost:8050`.

/!\ File path must be specified within the `src/app.py` python file.

## Tests
```shell
python -m unittest
```

## Docker
```shell
docker build . -f build/dev.Dockerfile -t json_visualizer
JV="$(docker run --rm -d -v $(pwd):/app json_visualizer:latest)"
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $JV
```
