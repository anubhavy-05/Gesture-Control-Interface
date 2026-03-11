"""
Test script to verify hand tracking is working correctly.
"""
import sys
import os

# Add parent directories to path
script_dir = os.path.dirname(os.path.abspath(__file__))
virtual_world_dir = os.path.dirname(script_dir)
parent_dir = os.path.dirname(virtual_world_dir)
sys.path.insert(0, parent_dir)

print("="*60)
print("Hand Tracking Test")
print("="*60)
print(f"\n1. Script directory: {script_dir}")
print(f"2. VIRTUAL-WORLD directory: {virtual_world_dir}")
print(f"3. Parent (Gesture-Control-Interface): {parent_dir}")
print(f"4. hand_tracker.py exists: {os.path.exists(os.path.join(parent_dir, 'hand_tracker.py'))}")

print("\n5. Attempting to import HandDetector...")
try:
    from hand_tracker import HandDetector
    print("   ✓ HandDetector imported successfully!")
    
    print("\n6. Creating HandDetector instance...")
    detector = HandDetector(max_hands=1)
    print("   ✓ HandDetector created successfully!")
    
    print("\n7. Testing detector attributes...")
    print(f"   - Max hands: {detector.max_hands}")
    print(f"   - INDEX_TIP id: {detector.INDEX_TIP}")
    print(f"   - THUMB_TIP id: {detector.THUMB_TIP}")
    
    print("\n" + "="*60)
    print(" SUCCESS! Hand tracking is working correctly!")
    print("="*60)
    
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "="*60)
    print("✗ FAILED! Hand tracking is NOT working")
    print("="*60)
