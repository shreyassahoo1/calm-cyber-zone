import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Shield, ArrowLeft, TrendingUp, Activity, Users, AlertCircle } from "lucide-react";
import StatsCard from "@/components/dashboard/StatsCard";

const Analytics = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalIncidents: 0,
    criticalIncidents: 0,
    avgToxicity: 0,
    platformBreakdown: { discord: 0, reddit: 0 },
  });

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const { data: incidents, error } = await supabase
        .from("incidents")
        .select("*");

      if (error) throw error;

      const total = incidents?.length || 0;
      const critical = incidents?.filter(i => i.severity === "critical").length || 0;
      const avgTox = incidents?.reduce((acc, i) => acc + (i.toxicity_score || 0), 0) / total || 0;
      const discord = incidents?.filter(i => i.platform === "discord").length || 0;
      const reddit = incidents?.filter(i => i.platform === "reddit").length || 0;

      setStats({
        totalIncidents: total,
        criticalIncidents: critical,
        avgToxicity: Math.round(avgTox * 100),
        platformBreakdown: { discord, reddit },
      });
    } catch (error: any) {
      console.error("Error loading analytics:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/20 to-background">
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Button variant="ghost" onClick={() => navigate("/dashboard")}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">Analytics</h1>
                <p className="text-sm text-muted-foreground">Monitor system performance and trends</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-2">Platform Analytics</h2>
          <p className="text-muted-foreground">Comprehensive overview of detection metrics</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Total Incidents"
            value={stats.totalIncidents}
            icon={Activity}
            trend="All time"
            variant="default"
          />
          <StatsCard
            title="Critical Incidents"
            value={stats.criticalIncidents}
            icon={AlertCircle}
            trend="High priority"
            variant="danger"
          />
          <StatsCard
            title="Avg Toxicity"
            value={`${stats.avgToxicity}%`}
            icon={TrendingUp}
            trend="Detection score"
            variant="warning"
          />
          <StatsCard
            title="Discord Incidents"
            value={stats.platformBreakdown.discord}
            icon={Users}
            trend="Platform breakdown"
            variant="info"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Platform Distribution</CardTitle>
              <CardDescription>Incident breakdown by platform</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium">Discord</span>
                    <span className="text-sm text-muted-foreground">{stats.platformBreakdown.discord} incidents</span>
                  </div>
                  <div className="w-full bg-secondary rounded-full h-2">
                    <div
                      className="bg-primary h-2 rounded-full transition-all duration-500"
                      style={{
                        width: `${(stats.platformBreakdown.discord / stats.totalIncidents) * 100}%`,
                      }}
                    />
                  </div>
                </div>
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium">Reddit</span>
                    <span className="text-sm text-muted-foreground">{stats.platformBreakdown.reddit} incidents</span>
                  </div>
                  <div className="w-full bg-secondary rounded-full h-2">
                    <div
                      className="bg-accent h-2 rounded-full transition-all duration-500"
                      style={{
                        width: `${(stats.platformBreakdown.reddit / stats.totalIncidents) * 100}%`,
                      }}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>System Health</CardTitle>
              <CardDescription>Overall monitoring status</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border border-border rounded-lg">
                  <span className="text-sm font-medium">Detection System</span>
                  <span className="px-3 py-1 bg-success/20 text-success text-xs rounded-full font-medium">
                    Operational
                  </span>
                </div>
                <div className="flex items-center justify-between p-4 border border-border rounded-lg">
                  <span className="text-sm font-medium">Bot Monitoring</span>
                  <span className="px-3 py-1 bg-success/20 text-success text-xs rounded-full font-medium">
                    Active
                  </span>
                </div>
                <div className="flex items-center justify-between p-4 border border-border rounded-lg">
                  <span className="text-sm font-medium">Database Status</span>
                  <span className="px-3 py-1 bg-success/20 text-success text-xs rounded-full font-medium">
                    Healthy
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Analytics;
