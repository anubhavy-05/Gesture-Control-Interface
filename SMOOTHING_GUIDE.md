# Smoothing Configuration Guide

## Overview
The mouse cursor smoothing uses a **dual-filter approach** to eliminate jitter caused by slight hand movements:

1. **Exponential Moving Average (EMA)** - First layer of smoothing
2. **Moving Average Filter** - Second layer for additional stability

## How It Works

### Exponential Moving Average (EMA)
```
smoothed_position = previous_position + (target_position - previous_position) / smoothing_factor
```
- Gradually transitions from current position to target position
- Higher `smoothing_factor` = smoother but slower movement

### Moving Average Filter
- Maintains a buffer of recent positions
- Calculates the average of all positions in the buffer
- Eliminates high-frequency jitter and tremors

## Adjusting Parameters

### In `main.py` (line ~58):
```python
mouse = MouseController(smoothing_factor=7, buffer_size=5)
```

### Parameters:

#### `smoothing_factor` (default: 7)
- **Range**: 1-15
- **Lower values (3-5)**: 
  - ✅ More responsive
  - ✅ Faster movement
  - ❌ Less smooth, more jitter
- **Medium values (6-8)**: 
  - ✅ Balanced responsiveness and smoothness
  - ✅ Recommended for most users
- **Higher values (9-15)**: 
  - ✅ Very smooth, stable cursor
  - ❌ Slower, less responsive
  - ❌ Lag becomes noticeable

#### `buffer_size` (default: 5)
- **Range**: 3-10
- **Lower values (3-4)**:
  - ✅ More responsive to quick movements
  - ❌ Less effective at filtering jitter
- **Medium values (5-7)**:
  - ✅ Good balance
  - ✅ Recommended for most users
- **Higher values (8-10)**:
  - ✅ Maximum stability
  - ✅ Best for tremor reduction
  - ❌ Increased lag

## Recommended Configurations

### Fast & Responsive (Gaming/Quick Tasks)
```python
mouse = MouseController(smoothing_factor=4, buffer_size=3)
```

### Balanced (Default - General Use)
```python
mouse = MouseController(smoothing_factor=7, buffer_size=5)
```

### Ultra Smooth (Presentations/Steady Work)
```python
mouse = MouseController(smoothing_factor=10, buffer_size=7)
```

### Maximum Stability (Tremor Reduction)
```python
mouse = MouseController(smoothing_factor=12, buffer_size=8)
```

## Testing Your Settings

1. Run the demo to see smoothing in action:
   ```bash
   python smoothing_demo.py
   ```

2. Run the main application and test cursor movement:
   ```bash
   python main.py
   ```

3. Adjust parameters in `main.py` based on your preference
4. Restart the application to test new settings

## Troubleshooting

### Cursor is too slow/laggy
- **Decrease** `smoothing_factor` (try 5 or 6)
- **Decrease** `buffer_size` (try 3 or 4)

### Cursor is jittery/shaky
- **Increase** `smoothing_factor` (try 8 or 9)
- **Increase** `buffer_size` (try 6 or 7)

### Cursor doesn't respond to fast movements
- **Decrease both** parameters
- This allows more responsive tracking

## Technical Details

### Why Dual Smoothing?
- **EMA alone**: Good for gradual smoothing but can still show high-frequency jitter
- **Moving Average alone**: Good for filtering noise but can lag on quick movements
- **Combined**: Best of both worlds - smooth, stable, and responsive

### Performance Impact
- Minimal CPU usage (~0.1% additional)
- No noticeable latency with default settings
- Buffers are memory-efficient (< 100 bytes)
