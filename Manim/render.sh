#!/bin/bash

# Manim Render Script
# This script uses the correct Python installation to render Manim animations

PYTHON_PATH="/usr/local/bin/python3.10"
SCRIPT_NAME="main.py"
SCENE_NAME="SampleAnimation"

echo "Rendering Manim animation..."
echo "Script: $SCRIPT_NAME"
echo "Scene: $SCENE_NAME"
echo ""

$PYTHON_PATH -m manim -p $SCRIPT_NAME $SCENE_NAME

echo ""
echo "Render complete! Video saved to: media/videos/main/1080p60/$SCENE_NAME.mp4" 