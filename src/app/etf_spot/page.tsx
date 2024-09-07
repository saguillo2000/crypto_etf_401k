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

  const handleAddCoinWeight = () => {
    if (coin.trim() && !coinWeights.some(item => item.coin === coin)) {
      setCoinWeights([...coinWeights, { coin, weight: 0 }]);
      setCoin('');
    }
  };

  const calculateWeights = () => {
    const totalCoins = coinWeights.length;
    const updatedCoinWeights = coinWeights.map(item => ({
      ...item,
      weight: isUniform ? 1 / totalCoins : Math.random() // Replace Math.random() with actual marketcap logic
    }));
    setCoinWeights(updatedCoinWeights);
  };

  const handleChatSubmit = async () => {
    if (chatInput.trim()) {
      const question = chatInput;
      setChatInput('');
      // Simulate an API call to get the answer from an LLM
      const answer = await getAnswerFromLLM(question);
      setChatHistory([...chatHistory, { question, answer }]);
    }
  };

  const getAnswerFromLLM = async (question: string): Promise<string> => {
    // Simulate an API call to an LLM
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(`This is a simulated answer to the question: "${question}"`);
      }, 1000);
    });
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
        <button onClick={calculateWeights} className="bg-green-500 text-white p-2 mb-5">
          Calculate Weights
        </button>
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
                <td className="border px-4 py-2">{item.weight.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="flex space-x-4">
          <button className="bg-green-500 text-white p-2 flex items-center">
            <FaRocket className="mr-2" /> Buy
          </button>
          <button className="bg-red-500 text-white p-2 flex items-center">
            <FaMoneyBillWave className="mr-2" /> Sell
          </button>
        </div>
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