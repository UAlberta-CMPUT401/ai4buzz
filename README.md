# ai4buzz

https://ualberta-cmput401.github.io/ai4buzz/

# REST-API

- Base url: http://[2605:fd00:4:1001:f816:3eff:fe26:70dd]
- Docs: http://[2605:fd00:4:1001:f816:3eff:fe26:70dd]/docs

# Local Setup

## Prerequisites

- Python 3.9
- Yarn and Nodejs

## API

1. clone the repo
2. `cd` into the `backend` directory
3. generate virtual environment with `python3 -m venv env`
4. activate virtual env with `source env/bin/activate`
5. install requirements with `pip install -r requirements.txt`
6. run app with `uvicorn api.main:app --reload`

## Web Client

1. clone the repo if you haven't already
2. `cd` into `frontend` directory
3. use `yarn start` to start app locally
