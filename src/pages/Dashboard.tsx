import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { User } from "@supabase/supabase-js";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { AlertTriangle, Activity, Shield, TrendingUp, LogOut, Users, Database } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import StatsCard from "@/components/dashboard/StatsCard";
import RecentIncidents from "@/components/dashboard/RecentIncidents";
import BotStatusCards from "@/components/dashboard/BotStatusCards";

const Dashboard = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalIncidents: 0,
    activeIncidents: 0,
    resolvedToday: 0,
    detectionRate: 0,
  });

  useEffect(() => {
    const checkAuth = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      if (!session) {
        navigate("/auth");
        return;
      }
      setUser(session.user);
      await loadStats();
      setLoading(false);
    };
    checkAuth();

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      if (!session) {
        navigate("/auth");
      } else {
        setUser(session.user);
      }
    });

    return () => subscription.unsubscribe();
  }, [navigate]);

  const loadStats = async () => {
    try {
      const { data: incidents, error } = await supabase
        .from("incidents")
        .select("*");

      if (error) throw error;

      const total = incidents?.length || 0;
      const active = incidents?.filter(i => i.status === "pending" || i.status === "reviewing").length || 0;
      const resolvedToday = incidents?.filter(i => {
        const today = new Date().toDateString();
        return i.resolved_at && new Date(i.resolved_at).toDateString() === today;
      }).length || 0;

      setStats({
        totalIncidents: total,
        activeIncidents: active,
        resolvedToday,
        detectionRate: total > 0 ? Math.round((resolvedToday / total) * 100) : 0,
      });
    } catch (error: any) {
      console.error("Error loading stats:", error);
    }
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    navigate("/auth");
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/20 to-background">
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">SafeGuard Platform</h1>
              <p className="text-sm text-muted-foreground">Cyberbullying Detection Dashboard</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" onClick={() => navigate("/incidents")}>
              <Database className="w-4 h-4 mr-2" />
              Incidents
            </Button>
            <Button variant="ghost" onClick={() => navigate("/analytics")}>
              <TrendingUp className="w-4 h-4 mr-2" />
              Analytics
            </Button>
            <Button variant="ghost" onClick={handleSignOut}>
              <LogOut className="w-4 h-4 mr-2" />
              Sign Out
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-2">Welcome back!</h2>
          <p className="text-muted-foreground">Here's what's happening with your monitoring systems</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Total Incidents"
            value={stats.totalIncidents}
            icon={AlertTriangle}
            trend="+12% from last week"
            variant="default"
          />
          <StatsCard
            title="Active Incidents"
            value={stats.activeIncidents}
            icon={Activity}
            trend="Requires attention"
            variant="warning"
          />
          <StatsCard
            title="Resolved Today"
            value={stats.resolvedToday}
            icon={Shield}
            trend="Great work!"
            variant="success"
          />
          <StatsCard
            title="Detection Rate"
            value={`${stats.detectionRate}%`}
            icon={TrendingUp}
            trend="System performance"
            variant="info"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <BotStatusCards />
        </div>

        <div className="grid grid-cols-1 gap-6">
          <RecentIncidents />
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
