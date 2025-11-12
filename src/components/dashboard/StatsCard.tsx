import { Card, CardContent } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: string;
  variant?: "default" | "success" | "warning" | "danger" | "info";
}

const StatsCard = ({ title, value, icon: Icon, trend, variant = "default" }: StatsCardProps) => {
  const variantStyles = {
    default: "from-card to-card/80",
    success: "from-success/10 to-success/5 border-success/20",
    warning: "from-warning/10 to-warning/5 border-warning/20",
    danger: "from-destructive/10 to-destructive/5 border-destructive/20",
    info: "from-info/10 to-info/5 border-info/20",
  };

  const iconStyles = {
    default: "bg-primary text-primary-foreground",
    success: "bg-success text-success-foreground",
    warning: "bg-warning text-warning-foreground",
    danger: "bg-destructive text-destructive-foreground",
    info: "bg-info text-info-foreground",
  };

  return (
    <Card className={cn("bg-gradient-to-br border shadow-md hover:shadow-lg transition-all duration-300", variantStyles[variant])}>
      <CardContent className="p-6">
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <div className={cn("w-10 h-10 rounded-lg flex items-center justify-center", iconStyles[variant])}>
            <Icon className="w-5 h-5" />
          </div>
        </div>
        <div className="space-y-1">
          <p className="text-3xl font-bold text-foreground">{value}</p>
          {trend && (
            <p className="text-xs text-muted-foreground">{trend}</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default StatsCard;
