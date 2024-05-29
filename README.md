# Pong3D
This is Pong3D. A remake of an old project. It is a very simple 3D Pong game made in Python.

![Pong3D Screenshot](./screenshot.png)

## How to play
This game is written in Python. So you need the latest Python Interpreter installed.

### Dependencies
At the repository's directory, install all the necessary dependencies with `pip`:
```console
$ pip install -r requirements.txt
```

#### Assets
- **Soundtrack**: *Romantic* by Francisco Alvear
- **Other sounds**: from [opengameart.org](https://opengameart.org/)
- **Font**: [*Plus Jakarta*](https://fonts.google.com/specimen/Plus+Jakarta+Sans?query=plus+jakarta) (Extra Bold)

### Tutorial
After installing all the dependencies, run the only Python script at the `src` folder:
```console
$ python src/pong3d.py
```

### Controls
| **Control**                      | **Description** |
| -------------                    | --------------- |
| `ESC`                            | Exit game       |
| `W`/`S`                          | Move paddle P2  |
| `LEFT ARROW`/`RIGHT ARROW`       | Move paddle P1  |

## Old version
You can also play the old version of the game. It's source code is in the [`oldsrc` folder](./oldsrc/) inside the repository.

To play it, just install old dependencies and run the old script:
```console
$ pip install -r oldsrc/requirements.txt
$ python oldsrc/__main__.py
```

---

> By Marcio Dantas