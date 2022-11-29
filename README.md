# PyScrapAttr

PyScrapAttr is a lightweight python CLI and it's purpose is to scrap recursively a website and extract stats about class and id attributes.

# Installation

See further for Docker usage.
## Compile the library
In order to compile the C++ library, make sure you have installed g++ compiler in your system and is accessible from your PATH.

Run the following command (in the root folder) to compile and create a shared library.
1. Compilation 
```bash
g++ -c -fPIC add.cpp -o add.o
```
2. Create a shared library
```bash
g++ -shared -Wl,-soname,libadd.so -o libadd.so  add.o
```

## Run the RabbitMQ container
Before running the script, you must setup and run the RabbitMQ container.

Execute the following steps :
- Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/)
- Run `docker compose up -d --build` at the root of the folder. This will automatically pull and run the RabbitMQ instance.

## Configure the virtual environment
### Create a new environment virtualenv

Create a virutal environment using [virtualenv](https://docs.python.org/fr/3/library/venv.html).

```bash
python3 -m venv venv
```

### Entering the environment

```bash
source venv/bin/activate
```

## Installation of package listed in requirement.txt

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip3 install -r requirements.txt
```

## How to use the program
You can find help by typing `python main.py --help`.
```
> python main.py --help
usage: PyScrapAttr [-h] [--url URL] [--depth DEPTH]
PyScrapAttr is a lightweight python CLI and it's purpose is to scrap recursively a website and extract stats about class and id
attributes.

options:
  -h, --help     show this help message and exit
  --url URL      Url of website to scrape.
  --depth DEPTH  Depth of recursivity to stop at.
```

- Example : `python main.py --url https://www.github.com --depth 3`

## Installation and usage via Docker
At the root folder build the docker image :
```
docker build -t pyscrapweb .
```

You can the run the project directly from the container :

```bash
docker run --net=host --rm -v ${PWD}:/app pyscrapweb \
    --url ${HOSTNAME} \
    --depth ${DEPTH}
```
