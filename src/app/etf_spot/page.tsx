"use client";

import React, { useState } from 'react';

interface CoinWeight {
  coin: string;
  weight: number;
}

const VerificationSuccess: React.FC = () => {
  const [coin, setCoin] = useState('');
  const [coinWeights, setCoinWeights] = useState<CoinWeight[]>([]);
  const [isUniform, setIsUniform] = useState(true);

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

  return (
    <div className="flex flex-col items-center justify-center align-middle h-screen bg-gradient-to-r from-green-400 via-blue-500 to-purple-600">
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
      <table className="table-auto bg-white rounded-lg shadow-lg">
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
    </div>
  );
};

export default VerificationSuccess;