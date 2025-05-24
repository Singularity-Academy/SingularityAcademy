# Manim Sample Video Project

This project demonstrates how to create mathematical animations using [Manim Community Edition](https://docs.manim.community/en/stable/).

## What's Generated

The sample animation includes:
- 📝 **Title Animation**: "Manim Sample Video" appears at the top
- 🧮 **Mathematical Formulas**: 
  - Euler's identity: `e^(iπ) + 1 = 0`
  - Gaussian integral: `∫_{-∞}^{∞} e^(-x²) dx = √π`
- 🔷 **Geometric Shapes**: Circle, square, and triangle with color transformations
- 🎨 **Animations**: Writing, rotating, color changes, and movements
- ✨ **Final Message**: "Created with Manim!"

## Files Structure

```
.
├── main.py              # Main Manim animation script
├── render.sh            # Helper script for easy rendering
├── README.md            # This documentation
└── media/
    └── videos/
        └── main/
            └── 1080p60/
                └── SampleAnimation.mp4  # Generated video output
```

## How to Run

### Option 1: Using the helper script (Recommended)
```bash
./render.sh
```

### Option 2: Direct command
```bash
python3 -m manim -p main.py SampleAnimation
```

## Prerequisites

- **Manim Community Edition**: Already installed via pip
- **Python 3.10**: Located at `python3`
- **LaTeX**: Required for mathematical formula rendering (automatically handled)

## Output

The rendered video will be saved as:
`media/videos/main/1080p60/SampleAnimation.mp4`

## Customization

You can modify `main.py` to create your own animations:
- Change the `SampleAnimation` class name
- Add new animations in the `construct()` method
- Experiment with different shapes, colors, and transformations
- Add your own mathematical formulas using `MathTex()`

## Additional Manim Commands

```bash
# Render without preview
python3 -m manim main.py SampleAnimation

# Render in low quality (faster)
python3 -m manim -ql main.py SampleAnimation

# Render in high quality
python3 -m manim -qh main.py SampleAnimation

# Show last frame only
python3 -m manim -s main.py SampleAnimation
```

## Learn More

- [Manim Community Documentation](https://docs.manim.community/en/stable/)
- [Example Gallery](https://docs.manim.community/en/stable/examples.html)
- [Tutorials](https://docs.manim.community/en/stable/tutorials/quickstart.html)

## Video Specifications

- **Resolution**: 1080p (1920x1080)
- **Frame Rate**: 60 FPS
- **Duration**: ~19 seconds
- **Format**: MP4
- **Size**: ~943KB 