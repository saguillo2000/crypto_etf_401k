"use client";

import React, { useState } from 'react';
import { FaRocket, FaMoneyBillWave } from 'react-icons/fa'; // Import the rocket and money icons from react-icons

interface CoinWeight {
  coin: string;
  weight: number;
}

const VerificationSuccess: React.FC = () => {
  const [coin, setCoin] = useState('');
  const [coinWeights, setCoinWeights] = useState<CoinWeight[]>([]);
  const [isUniform, setIsUniform] = useState(true);
  const [chatInput, setChatInput] = useState('');
  const [chatHistory, setChatHistory] = useState<{ question: string, answer: string }[]>([]);
  const [showPopup, setShowPopup] = useState(false);
  const [showPending, setShowPending] = useState(false);
  const [popupMessage, setPopupMessage] = useState('');
  const [walletSummary, setWalletSummary] = useState('');

  const handleAddCoinWeight = () => {
    if (coin.trim() && !coinWeights.some(item => item.coin === coin)) {
      setCoinWeights([...coinWeights, { coin, weight: 0 }]);
      setCoin('');
    }
  };

  const calculateWeights = async () => {
    if (isUniform) {
      const totalCoins = coinWeights.length;
      const updatedCoinWeights = coinWeights.map(item => ({
        ...item,
        weight: parseFloat((1 / totalCoins).toFixed(3)), // Ensure weight has 3 decimals
      }));
      setCoinWeights(updatedCoinWeights);
    } else {
      const symbols = coinWeights.map(item => item.coin);
      console.log('Symbols for POST request:', { symbols }); // Log the symbols array

      try {
        const response = await fetch('http://127.0.0.1:8003/compute_market_caps_weights/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ symbols }),
        });

        if (!response.ok) {
          throw new Error('Failed to fetch market cap weights');
        }

        const data = await response.json();
        console.log('API response:', data); // Log the API response

        const updatedCoinWeights = coinWeights.map(item => ({
          ...item,
          weight: parseFloat((data[item.coin] || 0).toFixed(3)), // Ensure weight has 3 decimals
        }));
        setCoinWeights(updatedCoinWeights);
      } catch (error) {
        console.error('Error calculating weights:', error);
      }
    }
  };

  const handleChatSubmit = async () => {
    if (chatInput.trim()) {
      const question = chatInput;
      setChatInput('');
      try {
        const response = await fetch('http://127.0.0.1:8003/gen_prompt/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ prompt: question }),
        });

        if (!response.ok) {
          throw new Error('Failed to fetch answer');
        }

        const data = await response.json();
        const answer = data.answer; // Accessing the 'answer' field directly
        console.log('API response answer:', answer); // Log the answer to the console
        setChatHistory([...chatHistory, { question, answer }]);
      } catch (error) {
        console.error('Error fetching answer:', error);
      }
    }
  };

  const handleBuy = () => {
    setShowPending(true);
    setTimeout(() => {
      setShowPending(false);
      setPopupMessage('ETF fulfilled');
      setShowPopup(true);
      setTimeout(() => {
        setShowPopup(false);
      }, 3000); // Hide the popup after 3 seconds
    }, 6000); // Wait for 6 seconds before showing the popup
  };

  const handleSell = () => {
    setShowPending(true);
    setTimeout(() => {
      setShowPending(false);
      setPopupMessage('All your assets have been converted to USDT');
      setShowPopup(true);
      setTimeout(() => {
        setShowPopup(false);
      }, 3000); // Hide the popup after 3 seconds
    }, 6000); // Wait for 6 seconds before showing the popup
  };

  const walletStatus = async () => {
    const hardcodedSummary = `**Asset Description**

The user's crypto wallet portfolio consists of 8 assets, including 2 stablecoins (USDT and USDC), 2 wrapped tokens (WBTC and WETH), and 4 other tokens (ETH, OP, WLD, and KWENTA). The portfolio includes a mix of native tokens, stablecoins, and wrapped tokens.

* **ETH**: The native currency of the Ethereum network, with a balance of 0.0018.
* **WBTC**: An ERC-20 token backed 1:1 with Bitcoin, with a balance of N/A (not available).
* **WETH**: An ERC-20 version of Ether, allowing for easier integration with smart contracts and DeFi protocols, with a balance of 0.0001.
* **OP**: The native token of the Optimism network, used for governance and gas fee payments, with a balance of N/A (not available).
* **WLD**: A cryptocurrency aiming to create a global identity and financial network, with a balance of N/A (not available).
* **KWENTA**: The governance token for Kwenta, a decentralized derivatives trading platform, with a balance of N/A (not available).
* **USDT**: A stablecoin pegged to the US dollar, with a balance of N/A (not available).
* **USDC**: A stablecoin pegged to the US dollar, with a balance of N/A (not available).`;

    setWalletSummary(hardcodedSummary);
    setPopupMessage('Wallet Summary');
    setShowPopup(true);
  };

  return (
    <div className="flex h-screen bg-gradient-to-r from-green-400 via-blue-500 to-purple-600">
      <div className="flex-1 flex flex-col items-center justify-center align-middle p-5">
        <h1 className="text-2xl mb-5 text-white">ETF creation for future Pension!</h1>
        <div className="mb-5">
          <select
            value={coin}
            onChange={(e) => setCoin(e.target.value)}
            className="border p-2 mr-2"
          >
            <option value="" disabled>Select coin</option>
            <option value="BTC">BTC</option>
            <option value="ETH">ETH</option>
            <option value="UNI">UNI</option>
            <option value="SOL">SOL</option>
            <option value="USDT">USDT</option>
            <option value="USDC">USDC</option>
          </select>
          <button onClick={handleAddCoinWeight} className="bg-blue-500 text-white p-2">
            Add Coin
          </button>
        </div>
        <div className="mb-5">
          <label className="mr-2 text-white">
            <input
              type="radio"
              name="weightType"
              checked={isUniform}
              onChange={() => setIsUniform(true)}
            />
            Uniform Weight
          </label>
          <label className="text-white">
            <input
              type="radio"
              name="weightType"
              checked={!isUniform}
              onChange={() => setIsUniform(false)}
            />
            Marketcap Based
          </label>
        </div>
        <div className="flex space-x-4 mb-5">
          <button onClick={calculateWeights} className="bg-green-500 text-white p-2">
            Calculate Weights
          </button>
          <button onClick={walletStatus} className="bg-blue-500 text-white p-2">
            Wallet Status
          </button>
        </div>
        <table className="table-auto bg-white rounded-lg shadow-lg mb-5">
          <thead>
            <tr>
              <th className="px-4 py-2 bg-blue-500 text-white">Coin</th>
              <th className="px-4 py-2 bg-blue-500 text-white">Weight</th>
            </tr>
          </thead>
          <tbody>
            {coinWeights.map((item, index) => (
              <tr key={index} className={index % 2 === 0 ? 'bg-blue-100' : 'bg-blue-200'}>
                <td className="border px-4 py-2">{item.coin}</td>
                <td className="border px-4 py-2">{item.weight.toFixed(3)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="flex space-x-4">
          <button onClick={handleBuy} className="bg-green-500 text-white p-2 flex items-center">
            <FaRocket className="mr-2" /> Buy
          </button>
          <button onClick={handleSell} className="bg-red-500 text-white p-2 flex items-center">
            <FaMoneyBillWave className="mr-2" /> Sell
          </button>
        </div>
        {showPending && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-5 rounded-lg shadow-lg">
              <h2 className="text-2xl mb-4">Transaction pending...</h2>
            </div>
          </div>
        )}
        {showPopup && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-5 rounded-lg shadow-lg">
              <h2 className="text-2xl mb-4">{popupMessage}</h2>
              {popupMessage === 'Wallet Summary' && (
                <div className="whitespace-pre-wrap">{walletSummary}</div>
              )}
              <button onClick={() => setShowPopup(false)} className="bg-blue-500 text-white p-2">
                Close
              </button>
            </div>
          </div>
        )}
      </div>
      <div className="flex-1 flex flex-col items-center justify-center align-middle p-5">
        <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-5 flex flex-col h-full">
          <div className="overflow-y-auto flex-grow mb-3 w-full">
            {chatHistory.map((chat, index) => (
              <div key={index} className="mb-3">
                <p className="font-bold">Q: {chat.question}</p>
                <p className="text-gray-700">A: {chat.answer}</p>
              </div>
            ))}
          </div>
          <div className="w-full">
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Ask a question..."
              className="border p-2 w-full"
            />
            <button onClick={handleChatSubmit} className="bg-blue-500 text-white p-2 mt-2 w-full">
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerificationSuccess;