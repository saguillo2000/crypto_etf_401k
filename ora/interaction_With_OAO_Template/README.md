https://docs.ora.io/doc/oao-onchain-ai-oracle/develop-guide/tutorials/interaction-with-oao-tutorial

source .env

forge script script/Prompt.s.sol --rpc-url $RPC_URL --broadcast --verify --etherscan-api-key $ETHERSCAN_KEY --legacy --gas-price 500000000
