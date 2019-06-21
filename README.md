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

### 2. Config env file

Create a `.env` file at `forge_symposia/` folder, and set your own config.
The `forge_symposia/env_sample` file is a sample.

### 3. Simulate data

#### 3.1 Generate wallet by SK

``` node.js
node forge_symposia/tools/declare.js
```

#### 3.2 Create the protocol on the chain

This step need moderator sk in the chain

``` shell
forge protocol:deploy protocols/event_chain/event_chain/event_chain.itx.json
```

#### 3.3 Generate mock data

``` bash
export PYTHONPATH=. && python forge_symposia/server/simulation/simulate.py
```

### 4. Start server on port 5000 with debug mode

```bash
export PYTHONPATH=. && python forge_symposia/server/app.py
```

### 5. Start client on port 3000

```bash
yarn start:client
```
