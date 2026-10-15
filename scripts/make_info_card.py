#!/usr/bin/env python3
"""
Generate a Neofetch-style terminal info card SVG (840 x 880) that can sit
beside justus-ascii.svg in place of (or alongside) stats.svg.

Output: info-card.svg
Usage: python scripts/make_info_card.py [output.svg]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, ".."))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO_ROOT, "info-card.svg")

W, H = 840, 880
PAD = 20
TITLEBAR_H = 30

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#e6edf3"
MUTED = "#7d8590"
CYAN = "#22d3ee"
GREEN = "#39d353"
YELLOW = "#f2cc60"
PURPLE = "#bc8cff"
RED = "#ff7b72"
BLUE = "#58a6ff"

lines = [
    ("OS", "Ubuntu Linux / Windows 11", BLUE),
    ("Host", "Developer Workstation @ 2007", MUTED),
    ("Kernel", "justus-core-v2.6", MUTED),
    ("Uptime", "Always coding, learning, building", GREEN),
    ("Shell", "zsh / bash / pwsh", CYAN),
    ("Role", "Software Engineer · Full-Stack Builder", YELLOW),
    ("Focus", "AI & RAG Chatbots · Food-Tech Solutions", PURPLE),
    ("Languages", "TypeScript, JavaScript, Python, HTML/CSS, SQL", INK),
    ("Frameworks", "React, Node.js, Express, Next.js, LangChain", INK),
    ("Tools", "Docker, Git, GitHub Actions, Linux, VS Code", INK),
    ("Current", "RAJU-FOOD-COURT & OFFLINE-RAG-CHAT-BOT", GREEN),
    ("Contact", "GitHub: @justusrobin2007", CYAN),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>'
    '.row { opacity: 0; animation: fadeIn 0.4s ease-out forwards; }'
    '@keyframes fadeIn { from { opacity: 0; transform: translateX(-8px); } to { opacity: 1; transform: translateX(0); } }'
    '</style>',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')

parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
    f'text-anchor="middle">justus@github: ~$ neofetch</text>'
)

# Header banner
start_y = TITLEBAR_H + 45
parts.append(f'<text x="{PAD+20}" y="{start_y}" fill="{CYAN}" font-size="24" font-weight="700">justus</text>')
parts.append(f'<text x="{PAD+105}" y="{start_y}" fill="{MUTED}" font-size="24">@</text>')
parts.append(f'<text x="{PAD+125}" y="{start_y}" fill="{PURPLE}" font-size="24" font-weight="700">github</text>')

sep_y = start_y + 16
parts.append(f'<line x1="{PAD+20}" y1="{sep_y}" x2="{W - PAD - 20}" y2="{sep_y}" stroke="{FRAME}" stroke-width="2"/>')

row_start_y = sep_y + 40
row_step = 42

for i, (key, val, color) in enumerate(lines):
    y = row_start_y + i * row_step
    delay = 0.15 + i * 0.08
    parts.append(f'<g class="row" style="animation-delay: {delay:.2f}s">')
    parts.append(f'<text x="{PAD+20}" y="{y}" fill="{color}" font-size="18" font-weight="700">{key}:</text>')
    parts.append(f'<text x="{PAD+160}" y="{y}" fill="{INK}" font-size="18">{val}</text>')
    parts.append('</g>')

# Color blocks at bottom (neofetch style)
pal_y = row_start_y + len(lines) * row_step + 20
swatch_w, swatch_h = 36, 18
swatches = ["#000000", "#ff7b72", "#39d353", "#f2cc60", "#58a6ff", "#bc8cff", "#22d3ee", "#c9d1d9"]

for i, col in enumerate(swatches):
    parts.append(f'<rect x="{PAD+20 + i*(swatch_w+6)}" y="{pal_y}" width="{swatch_w}" height="{swatch_h}" rx="3" fill="{col}"/>')

for i, col in enumerate(swatches):
    parts.append(f'<rect x="{PAD+20 + i*(swatch_w+6)}" y="{pal_y + swatch_h + 6}" width="{swatch_w}" height="{swatch_h}" rx="3" fill="{col}" opacity="0.6"/>')

parts.append('</svg>')
svg = "".join(parts)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"wrote {OUT}: {W} x {H}")
