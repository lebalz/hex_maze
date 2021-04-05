# hex_maze

Create random hexagonal mazes and export them to svg.

![example](examples/maze_10x10.svg)

It's possible to add margin to the tiles:

![tile marign](examples/maze_15x10.svg)

You can omit tiles from beeing part of the labyrinth too:

![omit tiles](examples/maze_6x8.svg)

![omit hex](examples/hexa.svg)

## Package and upload to pip

@see [this tutorial](https://packaging.python.org/tutorials/packaging-projects/)

```sh
rm -rf build/ dist/ hex_maze.egg-info/ && \
python3 setup.py sdist bdist_wheel && \
python3 -m twine upload dist/*
```
