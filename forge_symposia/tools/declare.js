/* eslint-disable no-console */
const path = require('path');
require('dotenv').config({path: path.resolve(path.join('forge_symposia', '.env'))});

// eslint-disable-next-line import/no-extraneous-dependencies
const GraphqlClient = require('@arcblock/graphql-client');
const { fromSecretKey } = require('@arcblock/forge-wallet');

const client = new GraphqlClient('http://localhost:8210/api');
const appWallet = fromSecretKey(`0x${process.env.REACT_APP_APP_SK}`);

(async () => {
  try {
    const res = await client.sendDeclareTx({
      tx: {
        itx: {
          moniker: process.env.MOCK_MONIKER,
        },
      },
      wallet: appWallet,
    });

    console.log('Application wallet declared', appWallet);
    console.log('Application wallet declared', res);
    process.exit(0);
  } catch (err) {
    console.error(err);
    console.error(err.errors);
    process.exit(1);
  }
})();
