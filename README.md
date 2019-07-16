# Forge Python Starter

## Requirements

- Node.js >= v10.x
- Python 3.x or have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html#install-macos-silent) installed
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

#### 3.2 Create the protocol on the chain

This step needs `MODERATOR_SK` and `MODERATOR_PK` stored in your environment

```make deploy-protocols```

#### 3.3 Generate mock data

```make simulate```

### 4. Start server on port 5000 with debug mode

```bash
make start-server
```

### 5. Start client on port 3000

```bash
make start-client
```
