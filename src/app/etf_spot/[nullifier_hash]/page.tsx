"use client";

import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

const VerificationSuccess = () => {
    const searchParams = useSearchParams();
    const [nullifierHash, setNullifierHash] = useState<string | null>(null);

    useEffect(() => {
        const hash = searchParams.get('nullifier_hash');
        if (hash) {
            setNullifierHash(hash);
        }
    }, [searchParams]);

    if (!nullifierHash) {
        return <div>Loading...</div>;
    }

    return (
        <div className="flex flex-col items-center justify-center align-middle h-screen">
            <h1 className="text-2xl mb-5">Verification Success</h1>
            <p>Your nullifier hash is: {nullifierHash}</p>
        </div>
    );
};

export default VerificationSuccess;