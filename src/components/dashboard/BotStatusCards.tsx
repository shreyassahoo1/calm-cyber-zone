import { useEffect, useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Bot, Activity } from "lucide-react";
import { formatDistanceToNow } from "date-fns";

interface BotStatus {
  platform: string;
  status: string;
  last_ping: string;
  message_count: number;
  incidents_detected: number;
}

const BotStatusCards = () => {
  const [botStatuses, setBotStatuses] = useState<BotStatus[]>([]);

  useEffect(() => {
    loadBotStatus();

    const channel = supabase
      .channel("bot-status-changes")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "bot_status" },
        () => {
          loadBotStatus();
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  const loadBotStatus = async () => {
    try {
      const { data, error } = await supabase
        .from("bot_status")
        .select("*");

      if (error) throw error;
      setBotStatuses(data || []);
    } catch (error: any) {
      console.error("Error loading bot status:", error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "online": return "success";
      case "offline": return "destructive";
      case "error": return "warning";
      default: return "default";
    }
  };

  const getStatusVariant = (status: string): "default" | "destructive" | "outline" | "secondary" => {
    switch (status) {
      case "online": return "default";
      case "offline": return "destructive";
      case "error": return "secondary";
      default: return "outline";
    }
  };

  return (
    <>
      {botStatuses.length === 0 ? (
        <Card className="col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="w-5 h-5" />
              Bot Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground text-center py-4">No bots configured yet</p>
          </CardContent>
        </Card>
      ) : (
        botStatuses.map((bot) => (
          <Card key={bot.platform} className="border-2 hover:shadow-lg transition-all duration-300">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2 capitalize">
                  <Bot className="w-5 h-5" />
                  {bot.platform} Bot
                </CardTitle>
                <Badge variant={getStatusVariant(bot.status)} className="capitalize">
                  {bot.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Messages Processed</span>
                  <span className="font-semibold">{bot.message_count.toLocaleString()}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Incidents Detected</span>
                  <span className="font-semibold text-warning">{bot.incidents_detected}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Last Active</span>
                  <span className="font-semibold">
                    {formatDistanceToNow(new Date(bot.last_ping), { addSuffix: true })}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))
      )}
    </>
  );
};

export default BotStatusCards;
