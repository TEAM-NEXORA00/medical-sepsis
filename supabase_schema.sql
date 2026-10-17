-- ==============================================================================
-- WARDWATCH AI: SUPABASE CLOUD DATABASE SCHEMA
-- Paste this script into your Supabase SQL Editor (https://supabase.com/dashboard)
-- Project: https://neeovxcrbsigbnkoimcd.supabase.co
-- ==============================================================================

-- 1. EHR Nurse Intervention Audit Trail Table
CREATE TABLE IF NOT EXISTS wardwatch_audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    simulation_hour INT NOT NULL,
    bed_id INT NOT NULL,
    bed_str TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    risk_score NUMERIC(5, 2) NOT NULL,
    risk_tier TEXT NOT NULL,
    completed_interventions INT NOT NULL,
    stat_lactate BOOLEAN DEFAULT FALSE,
    blood_cultures BOOLEAN DEFAULT FALSE,
    antibiotics BOOLEAN DEFAULT FALSE,
    crystalloid_bolus BOOLEAN DEFAULT FALSE,
    rapid_response BOOLEAN DEFAULT FALSE,
    telemetry_escalate BOOLEAN DEFAULT FALSE,
    nurse_notes TEXT
);

-- 2. Real-Time Telemetry Early Warning Alerts Table
CREATE TABLE IF NOT EXISTS wardwatch_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    simulation_hour INT NOT NULL,
    bed_str TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    alert_level TEXT NOT NULL, -- 'CRITICAL', 'WARNING', 'INFO'
    risk_score NUMERIC(5, 2) NOT NULL,
    shock_index NUMERIC(4, 2),
    qsofa INT,
    delta_map_3h NUMERIC(5, 2),
    serum_lactate NUMERIC(4, 2),
    top_xai_driver TEXT,
    lead_time_hours NUMERIC(3, 1)
);

-- 3. SBAR Shift Handover Reports Table
CREATE TABLE IF NOT EXISTS wardwatch_sbar_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    simulation_hour INT NOT NULL,
    bed_str TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    situation TEXT NOT NULL,
    background TEXT NOT NULL,
    assessment TEXT NOT NULL,
    recommendation TEXT NOT NULL
);

-- Enable Row Level Security (RLS) and public read/insert policies for demo
ALTER TABLE wardwatch_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE wardwatch_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE wardwatch_sbar_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public insert on wardwatch_audit_logs" 
ON wardwatch_audit_logs FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public select on wardwatch_audit_logs" 
ON wardwatch_audit_logs FOR SELECT USING (true);

CREATE POLICY "Allow public insert on wardwatch_alerts" 
ON wardwatch_alerts FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public select on wardwatch_alerts" 
ON wardwatch_alerts FOR SELECT USING (true);

CREATE POLICY "Allow public insert on wardwatch_sbar_reports" 
ON wardwatch_sbar_reports FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public select on wardwatch_sbar_reports" 
ON wardwatch_sbar_reports FOR SELECT USING (true);
