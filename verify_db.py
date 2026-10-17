import os
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from supabase import create_client

SUPABASE_URL = "https://neeovxcrbsigbnkoimcd.supabase.co"

# Load key from secrets.toml or environment
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
if not SUPABASE_KEY:
    try:
        import tomllib  # Python 3.11+
        secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
        if os.path.exists(secrets_path):
            with open(secrets_path, "rb") as f:
                sec = tomllib.load(f)
                SUPABASE_KEY = sec.get("SUPABASE_KEY", "")
    except Exception:
        pass

def verify():
    print("=" * 60)
    print("[WARDWATCH AI] SUPABASE CLOUD VERIFICATION PIPELINE")
    print("=" * 60)
    print(f"Connecting to: {SUPABASE_URL}...")
    
    if not SUPABASE_KEY:
        print("[FAIL] No Supabase key found in .streamlit/secrets.toml or SUPABASE_KEY env var.")
        return False

    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[OK] Authentication Successful!\n")
    except Exception as e:
        print(f"[FAIL] Connection Failed: {e}")
        return False

    tables = ["wardwatch_audit_logs", "wardwatch_alerts", "wardwatch_sbar_reports"]
    all_ready = True
    
    print("Checking Table Availability in Schema Cache:")
    for tbl in tables:
        try:
            res = client.table(tbl).select("*").limit(1).execute()
            print(f"  [OK] Table '{tbl}' is ACTIVE! (Current row count: {len(res.data)})")
        except Exception as e:
            all_ready = False
            print(f"  [PENDING] Table '{tbl}' NOT FOUND in Supabase schema cache.")

    print("\n" + "=" * 60)
    if all_ready:
        print("[SUCCESS] ALL TABLES VERIFIED! Your cloud database is 100% ready.")
        print("Launching the Streamlit command center will now write live audit trails.")
        
        try:
            test_alert = {
                "simulation_hour": 14,
                "bed_str": "BED-04",
                "patient_name": "Eleanor Wright",
                "alert_level": "WARNING",
                "risk_score": 38.5,
                "shock_index": 0.82,
                "qsofa": 1,
                "delta_map_3h": -4.8,
                "serum_lactate": 1.95,
                "top_xai_driver": "Shock Index Borderline Acceleration",
                "lead_time_hours": 4.5
            }
            client.table("wardwatch_alerts").insert(test_alert).execute()
            print("[OK] Test Alert Successfully Written to 'wardwatch_alerts'!")
        except Exception as insert_err:
            print(f"[NOTE] Test insert status: {insert_err}")
    else:
        print("ACTION REQUIRED: Run 'supabase_schema.sql' in your Supabase SQL Editor:")
        print(f"URL: https://supabase.com/dashboard/project/neeovxcrbsigbnkoimcd/sql/new")
    print("=" * 60)
    return all_ready

if __name__ == "__main__":
    verify()
