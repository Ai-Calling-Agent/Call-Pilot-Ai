"use client";

import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export default function HeroSection() {

  return (
    <div className="h-screen flex flex-col justify-center items-center px-4 text-center">
      <div className="max-w-3xl">
        {/* Badge */}
        <div className="inline-block mb-6 rounded-full bg-zinc-900 text-white text-sm font-medium px-4 py-1 border border-zinc-700">
          <span className="mr-2 inline-block">🎁</span>
          Lifetime Deal
        </div>

        {/* Title */}
        <h1 className="text-5xl md:text-6xl font-bold leading-tight">
          Effortless Calling
          <br />
          with <span className="text-green-500">Live AI Conversations</span>
        </h1>

        {/* Subtitle */}
        <p className="text-zinc-300 text-lg mt-6">
          Trigger thousands of personalized calls every day, our smart agent
          talks, listens, and adapts mid-call, then hands you a crisp recap.
        </p>

        {/* CTA Button */}
        <Button
        onClick={() => toast.success("🚀 Started for free!")} // 👈 Sonner toast

          variant="default"
          size="default"
          className="mt-8 text-lg !py-6 px-6 bg-green-500 hover:bg-green-600 text-gray-50"
        >
          Start for Free
        </Button>

        {/* Subtext */}
        <p className="text-zinc-300 text-sm mt-2">
          Start dialing smarter, no staff required
        </p>
      </div>
    </div>
  );
}
