import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { AlertTriangle, ExternalLink } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { format } from "date-fns";

interface Incident {
  id: string;
  platform: string;
  severity: string;
  status: string;
  content: string;
  author_name: string;
  detected_at: string;
  toxicity_score: number;
}

const RecentIncidents = () => {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadIncidents();

    const channel = supabase
      .channel("incidents-changes")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "incidents" },
        () => {
          loadIncidents();
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  const loadIncidents = async () => {
    try {
      const { data, error } = await supabase
        .from("incidents")
        .select("*")
        .order("detected_at", { ascending: false })
        .limit(5);

      if (error) throw error;
      setIncidents(data || []);
    } catch (error: any) {
      console.error("Error loading incidents:", error);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string): "default" | "destructive" | "outline" | "secondary" => {
    switch (severity) {
      case "critical": return "destructive";
      case "high": return "destructive";
      case "medium": return "secondary";
      case "low": return "outline";
      default: return "default";
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Recent Incidents</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">Loading incidents...</div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-warning" />
              Recent Incidents
            </CardTitle>
            <CardDescription>Latest detected cyberbullying incidents</CardDescription>
          </div>
          <Button variant="outline" onClick={() => navigate("/incidents")}>
            View All
            <ExternalLink className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {incidents.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            No incidents detected yet
          </div>
        ) : (
          <div className="space-y-4">
            {incidents.map((incident) => (
              <div
                key={incident.id}
                className="p-4 border border-border rounded-lg hover:bg-secondary/50 transition-colors cursor-pointer"
                onClick={() => navigate(`/incidents/${incident.id}`)}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <Badge variant={getSeverityColor(incident.severity)}>
                      {incident.severity}
                    </Badge>
                    <Badge variant="outline">{incident.platform}</Badge>
                    <Badge variant="outline">
                      Toxicity: {Math.round((incident.toxicity_score || 0) * 100)}%
                    </Badge>
                  </div>
                  <span className="text-xs text-muted-foreground">
                    {format(new Date(incident.detected_at), "MMM dd, HH:mm")}
                  </span>
                </div>
                <p className="text-sm text-foreground mb-2 line-clamp-2">{incident.content}</p>
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <span>Author: {incident.author_name || "Unknown"}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default RecentIncidents;
