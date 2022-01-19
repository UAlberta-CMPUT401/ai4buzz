# ai4buzz
- https://cmput401.ca/projects/a3bc8e93-1275-434e-9e88-f4af38bb276c
- https://ualberta-cmput401.github.io/ai4buzz/

# REST-API

- Base url: http://[2605:fd00:4:1001:f816:3eff:fe26:70dd]
- Docs: http://[2605:fd00:4:1001:f816:3eff:fe26:70dd]/docs

# Web client

- Url: http://[2605:fd00:4:1001:f816:3eff:fe67:1ff9]

# Local Setup

## Prerequisites

- Python 3.9
- Yarn and Nodejs

## API

1. clone the repo
2. `cd` into the `api` directory
3. generate virtual environment with `python3 -m venv env`
4. activate virtual env with `source env/bin/activate`
5. install requirements with `pip install -r requirements.txt`
6. run app with `uvicorn api.main:app --reload`

## Web Client

1. clone the repo if you haven't already
2. `cd` into `frontend` directory
3. use `yarn start` to start app locally

# Testing

## Backend

- Endpoint test API: `pytest api/tests/test_endpoints.py`
- Unit test models: `python -m unittest discover -p "*__test.py"`

## Frontend

- snap shot test: `yarn test`

## Screencast
https://drive.google.com/file/d/1Gijqd3WXwUsRNdpM-ITVAIPL44Fg5tlj/view?usp=sharing
