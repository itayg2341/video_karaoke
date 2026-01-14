import json
import time
import sys
from app import main as create_karaoke_video

# Load a small test sample
with open('lyrics.json', 'r') as f:
    lyrics_data = json.load(f)

# Use only first few segments for testing
small_data = {
    "language": lyrics_data["language"],
    "duration": 10.0,  # Only 10 seconds
    "segments": lyrics_data["segments"][:3]  # Only first 3 segments
}

print("Testing with small dataset...")
start_time = time.time()

try:
    # This should be fast but let's see what happens
    print("Starting video creation...")
    # We'll simulate the main loop without actually creating video
    import numpy as np
    from PIL import Image
    
    # Simulate the main processing loop
    duration = 10.0
    fps = 24
    total_frames = int(duration * fps)
    
    print(f"Processing {total_frames} frames...")
    
    for frame_idx in range(total_frames):
        if frame_idx % 24 == 0:  # Print every second
            print(f"  Processing frame {frame_idx}/{total_frames}")
        
        # Simulate the expensive nested loop
        current_time = frame_idx / fps
        words_to_show = []
        
        for segment in small_data["segments"]:
            segment_start = segment['start']
            segment_end = segment['end']
            
            if segment_start <= current_time < segment_end:
                for word_data in segment.get('words', []):
                    word_text = word_data['word']
                    word_start = word_data['start']
                    word_end = word_data['end']
                    is_highlight = word_start <= current_time < word_end
                    words_to_show.append((word_text, is_highlight))
    
    end_time = time.time()
    print(f"✓ Processing completed in {end_time - start_time:.2f} seconds")
    
    # Now let's test with the full dataset to see the performance issue
    print("\nTesting with full dataset...")
    start_time = time.time()
    
    full_duration = lyrics_data["duration"]
    full_fps = 24
    full_total_frames = int(full_duration * full_fps)
    
    print(f"Processing {full_total_frames} frames...")
    
    # Process just first 100 frames to demonstrate the issue
    for frame_idx in range(min(100, full_total_frames)):
        if frame_idx % 24 == 0:
            print(f"  Processing frame {frame_idx}/{full_total_frames}")
        
        current_time = frame_idx / full_fps
        words_to_show = []
        
        for segment in lyrics_data["segments"]:
            segment_start = segment['start']
            segment_end = segment['end']
            
            if segment_start <= current_time < segment_end:
                for word_data in segment.get('words', []):
                    word_text = word_data['word']
                    word_start = word_data['start']
                    word_end = word_data['end']
                    is_highlight = word_start <= current_time < word_end
                    words_to_show.append((word_text, is_highlight))
    
    end_time = time.time()
    print(f"✓ First 100 frames processed in {end_time - start_time:.2f} seconds")
    
    # Estimate full processing time
    estimated_full_time = (end_time - start_time) * (full_total_frames / 100)
    print(f"⚠️  Estimated full processing time: {estimated_full_time:.2f} seconds ({estimated_full_time/60:.1f} minutes)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
