"use client";

import { Button } from "@/components/ui/button";
import Link from "next/link";

const DemoSection = () => {
  return (
    <section className="flex flex-col justify-center items-center py-20 px-4 text-center bg-black">
      <div className="max-w-3xl">
        <div className="inline-block mb-6 rounded-full bg-green-600/10 text-green-400 text-sm font-medium px-4 py-1 border border-green-700/50">
          Live Demo
        </div>

        <h2 className="text-4xl md:text-5xl font-bold leading-tight text-white">
          See It in Action
        </h2>

        <p className="text-zinc-300 text-lg mt-6 mb-6">
          Explore a fully interactive demo page and experience how{" "}
          real-time monitoring
          and AI-powered insights
          keep your system transparent and reliable.
        </p>

        <Link href="/demo">
          <Button variant="default" size="lg">
            Open Demo →
          </Button>
        </Link>
      </div>
    </section>
  );
};

export default DemoSection;
