"use client";

import { VerificationLevel, IDKitWidget, useIDKit } from "@worldcoin/idkit";
import type { ISuccessResult } from "@worldcoin/idkit";
import { verify } from "./actions/verify";
import { useRouter } from "next/navigation"; 

export default function Home() {
  const app_id = process.env.NEXT_PUBLIC_WLD_APP_ID as `app_${string}`;
  const action = process.env.NEXT_PUBLIC_WLD_ACTION;

  if (!app_id) {
    throw new Error("app_id is not set in environment variables!");
  }
  if (!action) {
    throw new Error("action is not set in environment variables!");
  }

  const { setOpen } = useIDKit();

  const router = useRouter(); // Use useRouter from Next.js

  const onSuccess = (result: ISuccessResult) => {
    // Navigate to the new route based on nullifier_hash
    router.push(`/etf_spot`);
  };

  const handleProof = async (result: ISuccessResult) => {
    console.log(
      "Proof received from IDKit, sending to backend:\n",
      JSON.stringify(result)
    ); // Log the proof from IDKit to the console for visibility
    const data = await verify(result);
    if (data.success) {
      console.log("Successful response from backend:\n", JSON.stringify(data)); // Log the response from our backend for visibility
    } else {
      throw new Error(`Verification failed: ${data.detail}`);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center align-middle h-screen bg-gradient-to-r from-green-400 via-blue-500 to-purple-600">
      <p className="text-2xl mb-5 text-white">ETF journey starts! Crypto401K</p>
      <IDKitWidget
        action={action}
        app_id={app_id}
        onSuccess={onSuccess}
        handleVerify={handleProof}
        verification_level={VerificationLevel.Device} // Change this to VerificationLevel.Device to accept Orb- and Device-verified users
      />
      <button
        className="border border-black rounded-md bg-white text-black mt-5"
        onClick={() => setOpen(true)}
      >
        <div className="mx-3 my-1">Verify with World ID</div>
      </button>
    </div>
  );
}