# Project: ETF Crypto 401K

## Goal
The ETF Crypto 401K project aims to create a decentralized and secure solution to the current issues surrounding traditional social security systems. The goal is to empower younger generations to build custom ETFs (Exchange-Traded Funds) composed of their favorite, secure cryptocurrencies, which can serve as a more reliable alternative to social security. The project integrates blockchain technologies, decentralized finance (DeFi) tools, and innovative wallet and identity solutions to ensure transparency, security, and control over assets.

## Overview of Components

### 1. Worldcoin ID
- **Role:** Provides decentralized and privacy-preserving identity verification for users participating in the ETF platform.
- **Connection:** It is connected to **ETF Spot**, which handles the creation and management of custom crypto ETFs.
  
### 2. Optimism Wallet
- **Role:** Acts as the primary wallet for storing and managing the users' assets.
- **Connection:** Interacts with **Uniswap** for decentralized trading and liquidity management, as well as the **ETF Spot** for ETF creation.
  
### 3. Uniswap
- **Role:** Decentralized exchange (DEX) that allows for liquidity provision and token swaps necessary for ETF creation and rebalancing.
- **Connection:** Works in tandem with the **Optimism Wallet** for on-chain trading.
  
### 4. ETF Spot
- **Role:** The core platform where users create and manage their custom cryptocurrency ETFs. It connects to various data providers and pricing oracles to ensure accurate asset management.
- **Connections:**
  - Receives user identity data from **Worldcoin ID**.
  - Gets pricing information from **Redstone Prices**.
  - Leverages **DBForest Data** for additional data related to blockchain assets.
  - Interacts with **Optimism Wallet** for executing transactions.
  - Uses **ORA Wallet NLP** to facilitate natural language processing for user interaction.
  
### 5. ORA Wallet NLP
- **Role:** Facilitates interactions with the system using natural language processing. Users can communicate their preferences for ETF creation through conversational inputs.
- **Connection:** Directly linked to **Optimism Wallet** for processing commands related to assets.
  
### 6. DBForest Data
- **Role:** Provides blockchain data required for evaluating and managing the cryptocurrencies in the ETF.
- **Connection:** It feeds information into the **ETF Spot** for better decision-making and security.
  
### 7. Redstone Prices
- **Role:** Pricing oracle that ensures up-to-date and accurate crypto price feeds.
- **Connection:** Provides real-time price data to the **ETF Spot** for ETF valuation and management.

## How it Works

### 1. User Onboarding
Users authenticate themselves using **Worldcoin ID**, which ensures privacy and decentralized identity management.

### 2. Wallet Setup
Users create or connect their **Optimism Wallet** to store cryptocurrencies and interact with the ETF platform. Through **ORA Wallet NLP**, users can give commands to create and manage their ETFs using natural language.

### 3. ETF Creation
Users select their favorite and secure cryptocurrencies, which are available for trading via **Uniswap**. The **ETF Spot** platform facilitates the creation of custom ETFs by sourcing data from **Redstone Prices** for real-time asset pricing and **DBForest Data** for blockchain data.

### 4. Portfolio Management
The custom ETF is continuously managed by interacting with **Uniswap** for buying/selling assets, ensuring liquidity and optimal performance. The system uses inputs from **ORA Wallet NLP** to allow users to easily rebalance or modify their portfolios through simple language commands.

## Benefits

- **Decentralization:** Trustless system without reliance on centralized authorities.
- **Security:** The use of established blockchain and wallet protocols ensures that user funds and data are secure.
- **User-Friendly:** With **ORA Wallet NLP**, users can interact with the platform in an intuitive manner using natural language, without needing technical expertise.
- **Customizability:** Each user can create a personalized ETF that meets their preferences for risk tolerance and favorite assets.
- **Liquidity:** Integration with **Uniswap** provides access to a wide array of tokens and liquidity options.
  
## Future Scope

- Expansion of available assets through further partnerships with other decentralized exchanges and pricing oracles.
- Adding more advanced risk management and automated rebalancing features.
- Possible integration of traditional asset classes like tokenized stocks or bonds.

---

## How to Use Repo

### World ID Next.js Template

This project uses the **World ID SDK** for decentralized identity verification. Below is a guide on how to set up and run the project.

### Getting Started

First, set the correct Node.js version using `nvm` and run the development server:

```bash
nvm use 20
pnpm i && pnpm dev
