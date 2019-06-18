# Forge Python Starter

## Usage
Install requirements
```bash
pip install -r requirements.txt
```
Start client on port 3000

```bash
yarn start:client
```

Simulate Data
```bash
python forge_symposia/server/simulation/simulate.py
```

Start python server on 5000 with debug mode

```bash
python forge_symposia/server/app.py

```

Sample .env file
```python
REACT_APP_MONGO_URI="mongodb://127.0.0.1:27017/forge-python-starter"
REACT_APP_COOKIE_SECRET="0x6721a1883a8a9c08ea431a6528faf4c1a220194e8a3c0bed6159fd9737b4b7DB"
REACT_APP_CHAIN_ID="forge"

REACT_APP_CHAIN_HOST="http://10.1.10.176:8211/api"
REACT_APP_APP_TOKEN_SECRET="443aa6b102ab5af098da42dd3d6136d86da749804c2dee506f"
REACT_APP_APP_NAME="Forge Symposia"
REACT_APP_APP_PORT="3030"

REACT_APP_APP_SK="50E5B2470DEACAE7FACF9C7191EF06F9B993C72827519BDB3D32A3C34D7D982CDED338C010AB9504FB0A22C85A2013010E94917C1110F47EC733B47530F94279"
REACT_APP_APP_PK="DED338C010AB9504FB0A22C85A2013010E94917C1110F47EC733B47530F94279"
REACT_APP_APP_ID="z1gK9jeNy4wjNNAAN1A2anXmUDjJaJCvgGu"

REACT_APP_BASE_URL="http://10.1.10.176:3030"
SERVER_HOST="http://10.1.10.176:5000"
FORGE_SOCK_GRPC='127.0.0.1:27210'
```

