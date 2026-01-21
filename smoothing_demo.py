"""
Smoothing Demo - Standalone Example
Demonstrates how the dual smoothing approach reduces cursor jitter.
"""

import numpy as np
from collections import deque


def smooth_movement_demo():
    """
    Demonstrate the smoothing effect with sample data.
    """
    # Simulated jittery hand positions (x, y) over time
    # These represent noisy input from hand tracking
    raw_positions = [
        (500, 300), (505, 302), (498, 305), (510, 298), (502, 303),
        (508, 301), (495, 307), (512, 299), (501, 304), (509, 300)
    ]
    
    print("="*60)
    print("Cursor Smoothing Demonstration")
    print("="*60)
    print("\nRaw (Jittery) Positions vs Smoothed Positions:\n")
    
    # Smoothing parameters
    smoothing_factor = 7
    buffer_size = 5
    
    # Initialize smoothing state
    prev_x, prev_y = raw_positions[0]
    x_buffer = deque(maxlen=buffer_size)
    y_buffer = deque(maxlen=buffer_size)
    
    # Initialize buffer
    for _ in range(buffer_size):
        x_buffer.append(prev_x)
        y_buffer.append(prev_y)
    
    print(f"{'Frame':<8} {'Raw Position':<20} {'Smoothed Position':<20} {'Difference'}")
    print("-" * 60)
    
    for i, (raw_x, raw_y) in enumerate(raw_positions):
        # Apply exponential moving average (EMA)
        ema_x = prev_x + (raw_x - prev_x) / smoothing_factor
        ema_y = prev_y + (raw_y - prev_y) / smoothing_factor
        
        # Add to buffer
        x_buffer.append(ema_x)
        y_buffer.append(ema_y)
        
        # Apply moving average filter
        smoothed_x = np.mean(x_buffer)
        smoothed_y = np.mean(y_buffer)
        
        # Calculate difference
        diff = np.sqrt((smoothed_x - raw_x)**2 + (smoothed_y - raw_y)**2)
        
        print(f"{i+1:<8} ({raw_x}, {raw_y}){'':<8} ({smoothed_x:.1f}, {smoothed_y:.1f}){'':<8} {diff:.2f}px")
        
        # Update previous position
        prev_x = smoothed_x
        prev_y = smoothed_y
    
    print("\n" + "="*60)
    print("Benefits of Dual Smoothing:")
    print("="*60)
    print("1. Exponential Moving Average (EMA):")
    print("   - Reduces sudden jumps in cursor position")
    print("   - Formula: new_pos = prev_pos + (target - prev_pos) / factor")
    print(f"   - Current factor: {smoothing_factor} (higher = smoother, slower)")
    print()
    print("2. Moving Average Filter:")
    print("   - Averages last N positions for additional stability")
    print(f"   - Current buffer size: {buffer_size} positions")
    print("   - Eliminates high-frequency jitter")
    print()
    print("3. Combined Effect:")
    print("   - Much smoother cursor movement")
    print("   - Reduced sensitivity to hand tremors")
    print("   - More natural and controllable experience")
    print("="*60)


if __name__ == "__main__":
    smooth_movement_demo()
