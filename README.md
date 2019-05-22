Event Chain: An Event System Built on Forge

Quick Setup
---
1. Go to your python environment

2. `pip install forge-event-chain`


Run
---

Before running event_chain, make sure your local forge is running properly.

1. Add event_chain config in your forge config.
    ```toml
    [app]
    name = "Event-Chain"
    version = "0.1.0"
    path = "~/.forge/event_chain"
    host="127.0.0.1" # Your local IP address for wallet to connect
    port=5000
    did_address='http://localhost:4000' # The DID service event_chain will call from

    ```

2. restart forge to activate the updated config.

3. simulate original data to start with:

   `FORGE_CONFIG=/home/User/forge_release.toml python3.7 event_chain.simulation.simulate`

2. start event_chain application:

   `FORGE_CONFIG=/home/User/forge_release.toml python3.7 event_chain.runner normal`
