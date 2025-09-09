import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Phone, Languages, BarChart2, TrendingUp } from "lucide-react";

export default function BenefitSection() {
  return (
    <div className="py-16 px-4">
      <div className="text-center max-w-4xl mx-auto mb-12">
        <h2 className="text-4xl md:text-5xl font-bold text-white">
          Simple <span className="text-green-500">Monitoring</span> Tool
        </h2>
        <p className="text-zinc-300 text-lg mt-2">
          Everything You Need, All Together
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-10 max-w-6xl mx-auto">
        {/* Feature 1 */}
        <Card className="bg-gray-base border-zinc-800 text-white">
          <CardHeader className="pb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-md bg-zinc-800 flex items-center justify-center">
                <Phone className="text-green-500 w-5 h-5" />
              </div>
              <CardTitle className="text-white text-xl font-semibold">
                24/7 Calling Capability
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <p className="text-zinc-300 leading-relaxed">
              Never miss a lead, our AI agent makes calls around the clock,
              automatically reaching prospects across time zones and ensuring
              your outreach never sleeps.
            </p>
          </CardContent>
        </Card>

        {/* Feature 2 */}
        <Card className="bg-gray-base border-zinc-800 text-white">
          <CardHeader className="pb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-md bg-zinc-800 flex items-center justify-center">
                <Languages className="text-green-500 w-5 h-5" />
              </div>
              <CardTitle className="text-white text-xl font-semibold">
                Multilingual Support
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <p className="text-zinc-300 leading-relaxed">
              Speak your customers' language with seamless bilingual
              conversations in Hindi and English, expanding your reach across
              diverse markets and demographics.
            </p>
          </CardContent>
        </Card>

        {/* Feature 3 */}
        <Card className="bg-gray-base border-zinc-800 text-white">
          <CardHeader className="pb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-md bg-zinc-800 flex items-center justify-center">
                <BarChart2 className="text-green-500 w-5 h-5" />
              </div>
              <CardTitle className="text-white text-xl font-semibold">
                Cost Reduction Statistics
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <p className="text-zinc-300 leading-relaxed">
              Dramatically slash your outreach budget with automated calling
              that reduces operational costs by up to 70% compared to
              traditional manual dialing teams.
            </p>
          </CardContent>
        </Card>

        {/* Feature 4 */}
        <Card className="bg-gray-base border-zinc-800 text-white">
          <CardHeader className="pb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-md bg-zinc-800 flex items-center justify-center">
                <TrendingUp className="text-green-500 w-5 h-5" />
              </div>
              <CardTitle className="text-white text-xl font-semibold">
                Conversion Rate Improvements
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <p className="text-zinc-300 leading-relaxed">
              Transform prospects into customers with intelligent,
              personalized AI conversations that adapt in real-time and boost
              conversion rates by 40% or more.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
