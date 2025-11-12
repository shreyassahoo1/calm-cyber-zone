import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Shield, Bot, TrendingUp, AlertTriangle, ArrowRight } from "lucide-react";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/20 to-background">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary to-accent rounded-2xl mb-6 shadow-lg">
            <Shield className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent">
            SafeGuard Platform
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
            Advanced cyberbullying detection and monitoring system powered by AI.
            Protect your community with real-time incident detection across Discord and Reddit.
          </p>
          <div className="flex items-center justify-center gap-4">
            <Button
              size="lg"
              onClick={() => navigate("/auth")}
              className="bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-opacity"
            >
              Get Started
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => navigate("/dashboard")}
            >
              View Dashboard
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div className="bg-card border border-border rounded-xl p-8 hover:shadow-lg transition-all duration-300">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
              <Bot className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-xl font-bold mb-3">AI-Powered Detection</h3>
            <p className="text-muted-foreground">
              Advanced machine learning models analyze content in real-time to detect toxic behavior and cyberbullying patterns.
            </p>
          </div>

          <div className="bg-card border border-border rounded-xl p-8 hover:shadow-lg transition-all duration-300">
            <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4">
              <TrendingUp className="w-6 h-6 text-accent" />
            </div>
            <h3 className="text-xl font-bold mb-3">Real-Time Analytics</h3>
            <p className="text-muted-foreground">
              Monitor incidents, track trends, and gain insights with comprehensive analytics dashboards and reporting tools.
            </p>
          </div>

          <div className="bg-card border border-border rounded-xl p-8 hover:shadow-lg transition-all duration-300">
            <div className="w-12 h-12 bg-warning/10 rounded-lg flex items-center justify-center mb-4">
              <AlertTriangle className="w-6 h-6 text-warning" />
            </div>
            <h3 className="text-xl font-bold mb-3">Instant Alerts</h3>
            <p className="text-muted-foreground">
              Get notified immediately when critical incidents are detected, allowing for rapid response and intervention.
            </p>
          </div>
        </div>

        <div className="mt-16 text-center">
          <h2 className="text-3xl font-bold mb-6">Multi-Platform Support</h2>
          <div className="flex items-center justify-center gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-2">
                <Bot className="w-8 h-8 text-primary" />
              </div>
              <p className="font-semibold">Discord</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-2">
                <Bot className="w-8 h-8 text-accent" />
              </div>
              <p className="font-semibold">Reddit</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
