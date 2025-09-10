"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Phone, Languages, BarChart2, TrendingUp } from "lucide-react";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselPrevious,
  CarouselNext,
  CarouselDots,
} from "./ui/carousel";

const FeaturesSection = () => {
  return (
    <section className="py-20 px-4 bg-black text-white relative">
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="inline-block mb-4 rounded-full bg-zinc-900 text-green-500 text-sm font-semibold px-4 py-1 border border-zinc-800">
          Features
        </div>
        <h2 className="text-2xl md:text-4xl font-bold mb-4">
          What CallPilot AI Offers?
        </h2>
        <p className="text-zinc-300 text-lg">
          CallPilot AI delivers end-to-end automation for outbound calling—
          combining human-like AI conversations with real-time call insights.
        </p>
      </div>

      <div className="relative max-w-5xl mx-auto">
        <Carousel className="w-full" opts={{ align: "start", loop: true }}>
          <CarouselContent className="mb-8">
            <CarouselItem className="md:basis-1/2 lg:basis-1/3 ">
              <Card className="bg-gray-base border-zinc-800 text-white h-full rounded-md flex flex-col gap-0">
                <CardHeader className="pb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-md bg-green-light flex items-center justify-center">
                      <Phone className="text-green-500 w-5 h-5" />
                    </div>
                    <CardTitle className="text-white text-xl font-semibold">
                      24/7 Calling Capability
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-zinc-300 leading-relaxed">
                    Our AI agent runs non-stop, making thousands of calls daily
                    to ensure no lead is left behind.
                  </p>
                </CardContent>
              </Card>
            </CarouselItem>

            <CarouselItem className="md:basis-1/2 lg:basis-1/3">
              <Card className="bg-gray-base border-zinc-800 text-white h-full rounded-md flex flex-col gap-0">
                <CardHeader className="pb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-md bg-green-light flex items-center justify-center">
                      <Languages className="text-green-500 w-5 h-5" />
                    </div>
                    <CardTitle className="text-white text-xl font-semibold">
                      Language Flexibility
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-zinc-300 leading-relaxed">
                    Communicate naturally in Hindi and English. Our AI adapts
                    for better customer connection.
                  </p>
                </CardContent>
              </Card>
            </CarouselItem>

            <CarouselItem className="md:basis-1/2 lg:basis-1/3">
              <Card className="bg-gray-base border-zinc-800 text-white h-full rounded-md flex flex-col gap-0">
                <CardHeader className="pb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-md bg-green-light flex items-center justify-center">
                      <BarChart2 className="text-green-500 w-5 h-5" />
                    </div>
                    <CardTitle className="text-white text-xl font-semibold">
                      Cost Efficiency
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-zinc-300 leading-relaxed">
                    Save up to 70% in operational costs by replacing manual
                    dialing teams with smart AI agents that scale.
                  </p>
                </CardContent>
              </Card>
            </CarouselItem>

            <CarouselItem className="md:basis-1/2 lg:basis-1/3">
              <Card className="bg-gray-base border-zinc-800 text-white h-full rounded-md flex flex-col gap-0">
                <CardHeader className="pb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-md bg-green-light flex items-center justify-center">
                      <TrendingUp className="text-green-500 w-5 h-5" />
                    </div>
                    <CardTitle className="text-white text-xl font-semibold">
                      Boosted Conversions
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-zinc-300 leading-relaxed">
                    Personalized, dynamic AI conversations improve response
                    rates and close more leads fast.
                  </p>
                </CardContent>
              </Card>
            </CarouselItem>
          </CarouselContent>

          {/* Arrows positioned below the carousel */}
          <div className="flex justify-center items-center gap-4">
            <CarouselPrevious className="bg-zinc-900 border-zinc-700 hover:bg-zinc-800 text-white" />
            <CarouselDots />
            <CarouselNext className="bg-zinc-900 border-zinc-700 hover:bg-zinc-800 text-white" />
          </div>
        </Carousel>
      </div>
    </section>
  );
}

export default FeaturesSection;