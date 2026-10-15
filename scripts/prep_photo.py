"""
Prepare the portrait photo for clean ASCII conversion:
  1. Remove background (rembg) so the subject is isolated
  2. Bilateral-smooth away noise/textures while keeping edges sharp
  3. Tone stretch so skin lands near bright and hair/lines stay dark
  4. Darken linework (difference-of-gaussians ridges) for eyes, smile, and facial contours
  5. Square crop framing head & upper body cleanly
  6. Composite onto white canvas

Output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.
Usage: python scripts/prep_photo.py [input.jpg] [output.png]
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, ".."))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO_ROOT, "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO_ROOT, "source-prepped.png")

LINE_WEIGHT = 0.65

print(f"Loading {INP}...")
raw_img = Image.open(INP).convert("RGBA")
cut = remove(raw_img)
rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1])  # 0 = background
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

# Smooth skin/texture while keeping prominent edges
smooth = gray
for _ in range(3):
    smooth = cv2.bilateralFilter(smooth, 9, 40, 9)

# Tone stretch over subject pixels
lo, hi = np.percentile(smooth[alpha > 80], [3, 90])
tone = np.clip((smooth.astype(np.float32) - lo) / max(hi - lo, 1), 0, 1)

# Difference of Gaussians to enhance facial contours & eyes
fine = cv2.GaussianBlur(smooth, (0, 0), 1.5).astype(np.float32)
coarse = cv2.GaussianBlur(smooth, (0, 0), 6.0).astype(np.float32)
lines = np.clip((coarse - fine) / 40.0, 0, 1)
out = np.clip(tone - LINE_WEIGHT * lines, 0, 1) * 255.0

# Feather onto pure white background
mask = cv2.GaussianBlur(alpha.astype(np.float32) / 255.0, (0, 0), 1.0)
out = out * mask + 255.0 * (1.0 - mask)

# Head and upper body crop
# Locate subject bounds
ys, xs = np.where(alpha > 40)
min_y, max_y = ys.min(), ys.max()
min_x, max_x = xs.min(), xs.max()

# Center on upper torso & head:
head_top = min_y
# Choose a framing centered around face
cx = (min_x + max_x) // 2
# Head & chest region height is roughly 65% of full body height
crop_height = int((max_y - min_y) * 0.72)
side = max(int((max_x - min_x) * 1.3), crop_height)
# Center y around face / upper chest
cy = min_y + int(side * 0.48)

canvas = np.full((side, side), 255, np.uint8)
x0 = cx - side // 2
y0 = cy - side // 2

# Source region to copy
sx0, sx1 = max(0, x0), min(out.shape[1], x0 + side)
sy0, sy1 = max(0, y0), min(out.shape[0], y0 + side)

# Target placement
dx0 = max(0, -x0)
dy0 = max(0, -y0)
dx1 = dx0 + (sx1 - sx0)
dy1 = dy0 + (sy1 - sy0)

canvas[dy0:dy1, dx0:dx1] = out[sy0:sy1, sx0:sx1].astype(np.uint8)

Image.fromarray(canvas, mode="L").save(OUT)
print(f"Saved {OUT} ({canvas.shape[1]}x{canvas.shape[0]})")
