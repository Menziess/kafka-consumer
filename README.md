# Kafka Consumer

## Installation

Create a virtual environment inside the repo folder:
```sh
python -m venv .venv
source .venv/bin/activate
```

Install the requirements:
```
pip install -r requirements.txt
```

Install the project in develop/editor mode:
```
pip install -e .
pip list
```

Copy and put secrets into your own `.env` file:
```
cp .env.example .env
# replace *****'s
```

## Running the code

```
consume
```
