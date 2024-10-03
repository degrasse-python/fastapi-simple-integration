# Distributed ML API w/ FastAPI & Celery
Working example for serving a distributed ML prediction API using Python's FastAPI and Celery. 


## Usage

1. Follow the instructions below to prep your environment for the API.

**Install ENVs:**
Add this to your ~/.profile (zprofile on MacOS)
On MacOS you should be able to add the exports to your zshrc and open a new terminal for things to work.
* MODEL_PATH: Path to pickled machine learning model
* BROKER_URI: Message broker to be used by Celery e.g. RabbitMQ
* BACKEND_URI: Celery backend e.g. Redis

```bash
export PATH=$PATH:/usr/local/sbin
export BROKER_URI='rabbitmq.host:1989'
export BACKEND_URI=host_address
export PATH='/home/g5thcinematic/.local/bin:$PATH'
export MODEL_PATH='path/to/model'
```

then init the profile to add the current terminal

`source ~/.profile`

**Install requirements:**
```bash
sudo apt update && sudo apt upgrade -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install uvicorn
sudo apt install python3-pip

pip3 install poetry
```

```bash
apt list | grep python3.12
sudo apt install python3.12
sudo apt install python3.12-venv
python3.12 --version

sudo apt install pipx
pipx ensurepath --force
pipx install poetry
python3.12 -m venv fastapi
source fastapi/bin/activate
```


2.  Clone this repo using 
`git clone https://github.com/degrasse-python/fastapi-simple-integration.git`


3. Build All Python Dependencies
``` bash
cd fastapi-simple-integration
poetry install
```

**Start Services-local:Ubuntu**
```bash
# start the API for handling requests
uvicorn main:app --reload
# start the celery workers
celery -A celery_task_app:worker worker -l info
```

**Start Services-local:MacOS**
```bash
# start the API for handling requests
uvicorn main:app --reload
# start the celery workers
celery -A celery_task_app:worker worker -l info

```

**Set environment variables:**
On MacOS you should be able to add the exports to your zshrc and open a new terminal for things to work.
* MODEL_PATH: Path to pickled machine learning model
* BROKER_URI: Message broker to be used by Celery e.g. RabbitMQ
* BACKEND_URI: Celery backend e.g. Redis
