import traceback
from utils.database import init_supabase

try:
    print("Testing...")
    s = init_supabase()
    print(f"Result: {s}")
    print(f"Type: {type(s)}")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
