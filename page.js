"use client";

import { useEffect, useState } from "react";
import sdk, { type FrameContext } from "@farcaster/frame-sdk";

export default function Home() {
  const [isSDKLoaded, setIsSDKLoaded] = useState(false);
  const [context, setContext] = useState<FrameContext>();

  useEffect(() => {
    const load = async () => {
      // گرفتن context از Farcaster
      setContext(await sdk.context);

      // اعلام به Farcaster که فریم آماده‌ی نمایش هست
      sdk.actions.ready();
    };

    if (!isSDKLoaded) {
      setIsSDKLoaded(true);
      load();
    }
  }, [isSDKLoaded]);

  if (!isSDKLoaded) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-black text-white">
      <h1 className="text-3xl font-bold mb-4">🚀 Flwy Frame</h1>
      <p className="mb-6">Welcome to your Farcaster mini-app!</p>

      {context && (
        <div className="bg-gray-800 p-4 rounded text-sm max-w-xs text-left">
          <h2 className="font-semibold mb-2">Frame Context</h2>
          <pre className="whitespace-pre-wrap break-words">
            {JSON.stringify(context, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}