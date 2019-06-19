# Forge Python Starter

## Requirements

- Node.js >= v10.x
- Python 3.x
- A running Blockchain node # by forge-cli

## Setup

### 1. Install dependencies

``` bash
pip install -r requirements.txt
cd forge_symposia && yarn install
```

### 2. Simulate data

#### 2.1 Generate wallet by SK

``` node.js
node forge_symposia/tools/declare.js
```

#### 2.2 Create the protocol on the chain

This step need moderator sk in the chain

``` shell
forge protocol:deploy protocols/event_chain/event_chain/event_chain.itx.json
```

#### 2.3 Generate mock data

``` bash
export PYTHONPATH=. && python forge_symposia/server/simulation/simulate.py
```

### 3. Start server on port 5000 with debug mode

```bash
export PYTHONPATH=. && python forge_symposia/server/app.py
```

### 4. Start client on port 3000

```bash
yarn start:client
```

## Sample .env file

``` python
REACT_APP_MONGO_URI="mongodb://127.0.0.1:27017/forge-python-starter"
REACT_APP_COOKIE_SECRET="0x6721a1883a8a9c08ea431a6528faf4c1a220194e8a3c0bed6159fd9737b4b7DB"
REACT_APP_CHAIN_ID="forge"

REACT_APP_CHAIN_HOST="http://10.1.10.176:8211/api"
REACT_APP_APP_TOKEN_SECRET="443aa6b102ab5af098da42dd3d6136d86da749804c2dee506f"
REACT_APP_APP_NAME="Forge Symposia"
REACT_APP_APP_PORT="3030"

APP_SK="50E5B2470DEACAE7FACF9C7191EF06F9B993C72827519BDB3D32A3C34D7D982CDED338C010AB9504FB0A22C85A2013010E94917C1110F47EC733B47530F94279"
APP_PK="DED338C010AB9504FB0A22C85A2013010E94917C1110F47EC733B47530F94279"
REACT_APP_APP_ID="z1gK9jeNy4wjNNAAN1A2anXmUDjJaJCvgGu"

REACT_APP_BASE_URL="http://10.1.10.176:3030"
SERVER_HOST="http://10.1.10.176:5000"
FORGE_SOCK_GRPC='127.0.0.1:27210'
```
