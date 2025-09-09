import BenefitSection from "@/components/BenefitSection";
import FeaturesSection from "@/components/FeatureSection";
import HeroSection from "@/components/HeroSection";


export default function Home() {
  return (
    <div className="bg-black text-white">
      {/* HERO SECTION */}
      <HeroSection/>

      {/* BENEFIT SECTION */}
      <BenefitSection/>

      {/* FEATURES SECTION */}
      <FeaturesSection />
    </div>
  );
}
