import BenefitSection from "@/components/BenefitSection";
import DemoSection from "@/components/DemoSection";
import FeaturesSection from "@/components/FeatureSection";
import HeroSection from "@/components/HeroSection";


export default function Home() {
  return (
    <div className="bg-black text-white">
      <HeroSection/>

      <BenefitSection/>

      <FeaturesSection />

      <DemoSection/>


    </div>
  );
}
