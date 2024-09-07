import React from 'react';
import { useParams } from 'react-router-dom';

const VerificationSuccess: React.FC = () => {
  // Get the nullifier_hash from the URL
  const { nullifierHash } = useParams();

  return (
    <div className="flex flex-col items-center justify-center align-middle h-screen">
      <h1 className="text-2xl mb-5">Verification Success</h1>
      <p>Your nullifier hash is: {nullifierHash}</p>
    </div>
  );
};

export default VerificationSuccess;