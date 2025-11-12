export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "13.0.5"
  }
  public: {
    Tables: {
      analytics: {
        Row: {
          created_at: string
          data: Json
          event_type: string
          id: string
          platform: Database["public"]["Enums"]["bot_platform"] | null
        }
        Insert: {
          created_at?: string
          data: Json
          event_type: string
          id?: string
          platform?: Database["public"]["Enums"]["bot_platform"] | null
        }
        Update: {
          created_at?: string
          data?: Json
          event_type?: string
          id?: string
          platform?: Database["public"]["Enums"]["bot_platform"] | null
        }
        Relationships: []
      }
      bot_status: {
        Row: {
          created_at: string
          error_message: string | null
          id: string
          incidents_detected: number
          last_ping: string
          message_count: number
          metadata: Json | null
          platform: Database["public"]["Enums"]["bot_platform"]
          status: Database["public"]["Enums"]["bot_status_type"]
          updated_at: string
          uptime_seconds: number
        }
        Insert: {
          created_at?: string
          error_message?: string | null
          id?: string
          incidents_detected?: number
          last_ping?: string
          message_count?: number
          metadata?: Json | null
          platform: Database["public"]["Enums"]["bot_platform"]
          status?: Database["public"]["Enums"]["bot_status_type"]
          updated_at?: string
          uptime_seconds?: number
        }
        Update: {
          created_at?: string
          error_message?: string | null
          id?: string
          incidents_detected?: number
          last_ping?: string
          message_count?: number
          metadata?: Json | null
          platform?: Database["public"]["Enums"]["bot_platform"]
          status?: Database["public"]["Enums"]["bot_status_type"]
          updated_at?: string
          uptime_seconds?: number
        }
        Relationships: []
      }
      incidents: {
        Row: {
          author_id: string
          author_name: string | null
          channel_id: string | null
          channel_name: string | null
          content: string
          context: Json | null
          created_at: string
          detected_at: string
          id: string
          message_url: string | null
          notes: string | null
          platform: Database["public"]["Enums"]["bot_platform"]
          resolved_at: string | null
          resolved_by: string | null
          sentiment_score: number | null
          severity: Database["public"]["Enums"]["incident_severity"]
          status: Database["public"]["Enums"]["incident_status"]
          toxicity_score: number | null
          updated_at: string
        }
        Insert: {
          author_id: string
          author_name?: string | null
          channel_id?: string | null
          channel_name?: string | null
          content: string
          context?: Json | null
          created_at?: string
          detected_at?: string
          id?: string
          message_url?: string | null
          notes?: string | null
          platform: Database["public"]["Enums"]["bot_platform"]
          resolved_at?: string | null
          resolved_by?: string | null
          sentiment_score?: number | null
          severity?: Database["public"]["Enums"]["incident_severity"]
          status?: Database["public"]["Enums"]["incident_status"]
          toxicity_score?: number | null
          updated_at?: string
        }
        Update: {
          author_id?: string
          author_name?: string | null
          channel_id?: string | null
          channel_name?: string | null
          content?: string
          context?: Json | null
          created_at?: string
          detected_at?: string
          id?: string
          message_url?: string | null
          notes?: string | null
          platform?: Database["public"]["Enums"]["bot_platform"]
          resolved_at?: string | null
          resolved_by?: string | null
          sentiment_score?: number | null
          severity?: Database["public"]["Enums"]["incident_severity"]
          status?: Database["public"]["Enums"]["incident_status"]
          toxicity_score?: number | null
          updated_at?: string
        }
        Relationships: []
      }
      profiles: {
        Row: {
          avatar_url: string | null
          created_at: string
          email: string | null
          full_name: string | null
          id: string
          updated_at: string
        }
        Insert: {
          avatar_url?: string | null
          created_at?: string
          email?: string | null
          full_name?: string | null
          id: string
          updated_at?: string
        }
        Update: {
          avatar_url?: string | null
          created_at?: string
          email?: string | null
          full_name?: string | null
          id?: string
          updated_at?: string
        }
        Relationships: []
      }
      user_roles: {
        Row: {
          created_at: string
          id: string
          role: Database["public"]["Enums"]["app_role"]
          user_id: string
        }
        Insert: {
          created_at?: string
          id?: string
          role: Database["public"]["Enums"]["app_role"]
          user_id: string
        }
        Update: {
          created_at?: string
          id?: string
          role?: Database["public"]["Enums"]["app_role"]
          user_id?: string
        }
        Relationships: []
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      has_role: {
        Args: {
          _role: Database["public"]["Enums"]["app_role"]
          _user_id: string
        }
        Returns: boolean
      }
    }
    Enums: {
      app_role: "admin" | "moderator" | "user"
      bot_platform: "discord" | "reddit"
      bot_status_type: "online" | "offline" | "error"
      incident_severity: "low" | "medium" | "high" | "critical"
      incident_status: "pending" | "reviewing" | "resolved" | "dismissed"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {
      app_role: ["admin", "moderator", "user"],
      bot_platform: ["discord", "reddit"],
      bot_status_type: ["online", "offline", "error"],
      incident_severity: ["low", "medium", "high", "critical"],
      incident_status: ["pending", "reviewing", "resolved", "dismissed"],
    },
  },
} as const
