# PyGame ping-pong 
Implementation of classic ping-pong game using PyGame.
![screenshot of the game](/screenshots/demonstration.png "demo")
## Rquierements
To this game via source code basic requirement would be to have a 
Python interpreter on your local machine and meet a short list of packages required:
- PyGame - obviously to run the game;
- Pillow - to read byte string and convert it to Surface object.   

Both can be installed with `requirements.txt` via python package manager `pip`.
A more detailed description of package installation process is explained in 
the [Dependencies installation](#Dependencies-installation) section.  
**The game is well tested with Python 3.11 and Pygame 2.4.8**, so it's recommended
to use this versions of packages and Python itself.

## How to run game
There is two ways of running the game:
- Use a script;
- Use an executable.

To run it as a script, all the requirements should be met and current working 
directory should be `ping-pong`, then the run will succeed
and game will launch. Here is an example of running the game as a script:
```shell
$ (venv) python main.py
``` 
A more simple approach is to use executable file that bundled with all 
packages and tools required to run the game. There is no need to trouble your
self with package management, just run executable file as usual and enjoy the game
of ping pong.

## Dependencies installation
Installing dependencies with package manager `pip` is done easily with `requirements.txt`.
To use it as intended create `venv` and run command below:
```shell
$ (venv) pip install -r requirements.txt
````  
When packages are installed command prompt will be returned to you, and you'll
be able to run script with your local Python interpreter. Here is a table
of all packages necessary:

| Package | Version |
|:-------:|:-------:|
| pygame  |  2.4.0  |
| Pillow  |  9.5.0  |

## Build executable from source code
If you're done playing this simple version of ping-pong and want to add some 
features, change sprites or add some more content, there is a way to re-build 
executable file to distribute your version of game. One way is to use 
`Pyinstaller` as a tool to convert your modified code to and executable.
There is a `main.spec` file at `ping-pong` directory for such a case, 
you can use it, here is an example how:
```shell
$ (venv) pyinstaller main.spec
```
As a result, `Pyinstaller` will produce an executable named `ping-pong` at
`dist` folder. Game uses images at `img` folder, so if you change images,
you should re-produce byte-strings with `img_to_str` function implemented at
`encode_imgs.py` and use it in `main.py` script.
