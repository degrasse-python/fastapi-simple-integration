# Distributed ML API w/ FastAPI & Celery
Working example for serving a distributed ML prediction API using Python's FastAPI and Celery. 


## Usage

**Install requirements:**
```bash
pip3 install -r poetry
poetry install
```

**Install requirements:**
Add this to your ~/.bash_profile (zprofile on MacOS)
`PATH=$PATH:/usr/local/sbin`

**Start Services-local:Ubuntu**
```bash
# start the celery workers
celery -A celery_task_app:worker worker -l info

```

**Start Services-local:MacOS**
```bash
# start the celery workers
celery -A celery_task_app:worker worker -l info

```


**Set environment variables:**
On MacOS you should be able to add the exports to your zshrc and open a new terminal for things to work.
* MODEL_PATH: Path to pickled machine learning model
* BROKER_URI: Message broker to be used by Celery e.g. RabbitMQ
* BACKEND_URI: Celery backend e.g. Redis

`nano ~/.zshrc`

```bash
export MODEL_PATH='path/to/model'
export BROKER_URI='localhost.rabbitmq:1989'
export BACKEND_URI='host:6379'
```

**Start API:**
```bash
uvicorn app:app
```

**Start worker node:**
```bash
celery -A celery_task_app:worker worker -l info
```



**Stopping the services**
```bash
# stops the locally running RabbitMQ node
brew services stop rabbitmq
```