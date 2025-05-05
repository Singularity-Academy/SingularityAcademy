#!/usr/bin/env python3
import os
import glob
from PIL import Image
import sys

def check_frames(frames_dir="frames"):
    """
    Check if frames were correctly saved and display some statistics.
    """
    if not os.path.exists(frames_dir):
        print(f"Error: Directory '{frames_dir}' does not exist")
        return False
        
    # Find all session directories
    session_dirs = glob.glob(f"{frames_dir}/session_*")
    if not session_dirs:
        print(f"No session directories found in '{frames_dir}'")
        return False
        
    # Sort by creation time (newest first)
    session_dirs.sort(key=os.path.getctime, reverse=True)
    
    # Get the latest session
    latest_session = session_dirs[0]
    print(f"Latest session: {latest_session}")
    
    # Count frames in the latest session
    frame_files = glob.glob(f"{latest_session}/frame_*.jpg")
    frame_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
    
    if not frame_files:
        print("No frames found in the latest session")
        return False
    
    print(f"Total frames: {len(frame_files)}")
    
    # Check the first, middle and last frame
    sample_frames = [frame_files[0]]
    if len(frame_files) > 1:
        sample_frames.append(frame_files[len(frame_files) // 2])
    if len(frame_files) > 2:
        sample_frames.append(frame_files[-1])
    
    print("\nSample frame details:")
    for frame_path in sample_frames:
        try:
            with Image.open(frame_path) as img:
                frame_id = os.path.basename(frame_path).split('_')[-1].split('.')[0]
                print(f"  Frame #{frame_id}: {img.format}, {img.size}, {img.mode}")
        except Exception as e:
            print(f"  Error opening {frame_path}: {e}")
    
    print("\nLatest 5 frame IDs:", end=" ")
    last_frames = frame_files[-5:] if len(frame_files) >= 5 else frame_files
    frame_ids = [os.path.basename(f).split('_')[-1].split('.')[0] for f in last_frames]
    print(", ".join(frame_ids))
    
    return True

if __name__ == "__main__":
    frames_dir = sys.argv[1] if len(sys.argv) > 1 else "frames"
    check_frames(frames_dir) 