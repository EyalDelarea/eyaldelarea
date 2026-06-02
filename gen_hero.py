#!/usr/bin/env python3
"""Generate the animated TB-303 synth hero SVG (Neon Cyber) + preview page."""
import math, os

OUT = os.path.dirname(os.path.abspath(__file__))

P = dict(
    bg1="#0b0b1e", bg2="#1b0b30", grid="#332a5a",
    star="#a78bfa", c_top="#5eead4", c_left="#0891b2", c_right="#0e7490",
    accent="#22d3ee", accent2="#a855f7", text="#e0f2fe", sub="#94a3ff",
    panel="#0e1230", panel2="#161a3a", lcd="#04060f",
)

def stars():
    pts = [(120,60,0),(240,90,1.2),(1040,70,2.1),(960,120,0.6),(1120,60,1.7),
           (1150,150,2.6),(80,140,0.9),(1080,200,1.9),(180,210,1.3),(1010,250,2.3)]
    return "\n".join(
        f'  <circle class="star" cx="{x}" cy="{y}" r="2" fill="{P["star"]}" style="animation-delay:{d}s"/>'
        for x,y,d in pts)

def iso_cube(cx, cy, a, H, delay, dur):
    b=a/2
    top=f"{cx},{cy-b} {cx+a},{cy} {cx},{cy+b} {cx-a},{cy}"
    left=f"{cx-a},{cy} {cx},{cy+b} {cx},{cy+b+H} {cx-a},{cy+H}"
    right=f"{cx},{cy+b} {cx+a},{cy} {cx+a},{cy+H} {cx},{cy+b+H}"
    return f'''  <g class="cube" style="animation-delay:{delay}s;animation-duration:{dur}s">
    <polygon points="{left}" fill="{P['c_left']}"/>
    <polygon points="{right}" fill="{P['c_right']}"/>
    <polygon points="{top}" fill="{P['c_top']}"/>
  </g>'''

def knob(kx, ky, r, dur, label=None, label_dy=None):
    a, a2 = P['accent'], P['accent2']
    g = [f'<circle cx="{kx}" cy="{ky}" r="{r}" fill="{P["panel2"]}" stroke="{a}" stroke-width="2"/>']
    g.append(f'''<g>
      <line x1="{kx}" y1="{ky}" x2="{kx}" y2="{ky-r+3}" stroke="{a2}" stroke-width="2.4" stroke-linecap="round"/>
      <animateTransform attributeName="transform" type="rotate" dur="{dur}s"
        values="-140 {kx} {ky};140 {kx} {ky};-140 {kx} {ky}" repeatCount="indefinite"/>
    </g>''')
    g.append(f'<circle cx="{kx}" cy="{ky}" r="1.8" fill="{a}"/>')
    if label:
        g.append(f'<text x="{kx}" y="{ky+label_dy}" text-anchor="middle" font-family="\'Courier New\',monospace" font-size="7.5" fill="{a}" opacity="0.85" letter-spacing="0.5">{label}</text>')
    return "\n      ".join(g)

def synth():
    a, a2 = P['accent'], P['accent2']
    W, H = 640, 226
    s = []
    # panel
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="12" fill="url(#panel)" stroke="{a}" stroke-width="2.4"/>')
    s.append(f'<rect x="7" y="7" width="{W-14}" height="{H-14}" rx="9" fill="none" stroke="{a}" stroke-width="1" opacity="0.22"/>')
    # band dividers
    s.append(f'<line x1="10" y1="86" x2="{W-10}" y2="86" stroke="{a}" stroke-width="1" opacity="0.18"/>')
    s.append(f'<line x1="10" y1="150" x2="{W-10}" y2="150" stroke="{a}" stroke-width="1" opacity="0.18"/>')
    # --- branding ---
    s.append(f'<text x="16" y="34" font-family="Georgia,serif" font-style="italic" font-size="22" font-weight="700" fill="{a}">Roland</text>')
    s.append(f'<text x="16" y="50" font-family="\'Courier New\',monospace" font-size="7" fill="{a2}" letter-spacing="1.5" opacity="0.8">WAVEFORM</text>')
    s.append(f'<text x="{W-16}" y="34" text-anchor="end" font-family="Georgia,serif" font-style="italic" font-size="20" font-weight="700" fill="{P["text"]}">Bass Line</text>')
    # --- band 1: six knobs ---
    labels = ["TUNING","CUT OFF","RESO","ENV MOD","DECAY","ACCENT"]
    kxs = [148,216,284,352,420,488]
    for i,kx in enumerate(kxs):
        s.append(f'<text x="{kx}" y="20" text-anchor="middle" font-family="\'Courier New\',monospace" font-size="7.5" fill="{a}" opacity="0.85" letter-spacing="0.5">{labels[i]}</text>')
        s.append("<g>" + knob(kx, 50, 15, 4+i*0.9) + "</g>")
    # --- band 2: mode knobs / display / TB-303 / volume ---
    for i,(kx,lab) in enumerate([(40,"SHUFFLE"),(98,"SCALE"),(156,"TEMPO")]):
        s.append("<g>" + knob(kx, 116, 12, 5+i*0.7, lab, 24) + "</g>")
    # display (LCD) with scrolling waveform
    dx,dy,dw,dh = 210, 96, 158, 42
    s.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="4" fill="{P["lcd"]}" stroke="{a}" stroke-width="1.6"/>')
    s.append(f'<text x="{dx+8}" y="{dy+13}" font-family="\'Courier New\',monospace" font-size="8" fill="{a2}" letter-spacing="1">PATTERN 001 · ACID</text>')
    mid = dy + 30
    lam, amp = 40, 9
    wpts = " ".join(f"{x},{mid-amp*math.sin(2*math.pi*x/lam):.1f}" for x in range(0, dw*2+8, 3))
    s.append(f'''<g clip-path="url(#lcd)">
      <g><polyline points="{wpts}" fill="none" stroke="{a}" stroke-width="1.8" transform="translate({dx},0)"/>
      <animateTransform attributeName="transform" type="translate" dur="1.5s" values="0 0;{-lam} 0" repeatCount="indefinite"/></g>
    </g>''')
    # TB-303 label + volume
    s.append(f'<text x="392" y="108" font-family="\'Courier New\',monospace" font-size="15" font-weight="700" fill="{a2}">TB-303</text>')
    s.append(f'<text x="392" y="122" font-family="\'Courier New\',monospace" font-size="7.5" fill="{a}" opacity="0.8" letter-spacing="1">COMPUTER CONTROLLED</text>')
    s.append("<g>" + knob(600, 116, 20, 7, "VOLUME", 32) + "</g>")
    # --- band 3: step LEDs + keyboard ---
    kb_x, kb_y, kb_w = 24, 196, 592
    white_n = 14
    ww = kb_w/white_n
    # running step LEDs above keys
    steps = 16
    sx0, sgap = kb_x+4, (kb_w-8)/steps
    for i in range(steps):
        x = sx0 + i*sgap
        s.append(f'<rect class="step" x="{x:.1f}" y="158" width="{sgap-3:.1f}" height="9" rx="2" fill="{a}" stroke="{a}" stroke-width="0.6" style="animation-delay:{i*0.12:.2f}s"/>')
    # white keys
    for i in range(white_n):
        x = kb_x + i*ww
        s.append(f'<rect x="{x:.1f}" y="{kb_y}" width="{ww-1.5:.1f}" height="24" rx="2" fill="#0a0d22" stroke="{a}" stroke-width="1.3"/>')
    # black keys (after white indices)
    blacks = [0,1,3,4,5,7,8,10,11,12]
    for i in blacks:
        bx = kb_x + (i+1)*ww - ww*0.3
        s.append(f'<rect x="{bx:.1f}" y="{kb_y}" width="{ww*0.6:.1f}" height="15" rx="1.5" fill="{a}" fill-opacity="0.55" stroke="{a}" stroke-width="1"/>')
    # bottom labels
    s.append(f'<circle class="led" cx="{kb_x+5}" cy="187" r="4" fill="{a2}"/>')
    s.append(f'<text x="{kb_x+14}" y="190" font-family="\'Courier New\',monospace" font-size="7" fill="{a}" opacity="0.8" letter-spacing="1">RUN/STOP</text>')
    s.append(f'<text x="{kb_x+kb_w}" y="190" text-anchor="end" font-family="\'Courier New\',monospace" font-size="7" fill="{a2}" opacity="0.8" letter-spacing="1">ACCENT · SLIDE</text>')
    inner = "\n    ".join(s)
    return f'''  <g transform="translate(280,142)">
    <defs><clipPath id="lcd"><rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="4"/></clipPath></defs>
    {inner}
  </g>'''

def main():
    cubes = "\n".join([
        iso_cube(140,150,30,30,0.0,3.4),
        iso_cube(210,118,22,22,0.7,3.0),
        iso_cube(1040,140,30,30,0.5,3.6),
        iso_cube(1110,180,22,22,1.2,2.9),
        iso_cube(980,200,18,18,1.6,3.2),
    ])
    grid=[]
    for i in range(-2,15):
        x=i*90
        grid.append(f'<line x1="{x}" y1="380" x2="{x+260}" y2="270" stroke="{P["grid"]}" stroke-width="1"/>')
        grid.append(f'<line x1="{x}" y1="270" x2="{x+260}" y2="380" stroke="{P["grid"]}" stroke-width="1"/>')
    grid = "\n    ".join(grid)
    out = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380" font-family="'Segoe UI',Helvetica,Arial,sans-serif">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{P['bg1']}"/><stop offset="1" stop-color="{P['bg2']}"/>
    </linearGradient>
    <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{P['panel2']}"/><stop offset="1" stop-color="{P['panel']}"/>
    </linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      .cube {{ transform-box: fill-box; transform-origin: center; animation: bob ease-in-out infinite; }}
      @keyframes bob {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-12px)}} }}
      .star {{ animation: tw 2.4s ease-in-out infinite; }}
      @keyframes tw {{ 0%,100%{{opacity:.15}} 50%{{opacity:1}} }}
      .title {{ animation: pulse 3.2s ease-in-out infinite; }}
      @keyframes pulse {{ 0%,100%{{opacity:.82}} 50%{{opacity:1}} }}
      .step {{ opacity:.16; animation: seq 1.92s steps(1,end) infinite; }}
      @keyframes seq {{ 0%{{opacity:1;fill:{P['accent2']}}} 6%{{opacity:1;fill:{P['accent2']}}} 7%{{opacity:.16}} 100%{{opacity:.16}} }}
      .led {{ animation: blinkled 1.92s steps(1) infinite; }}
      @keyframes blinkled {{ 0%,12%{{opacity:1}} 13%,100%{{opacity:.25}} }}
      .cursor {{ animation: blink 1s steps(1) infinite; }}
      @keyframes blink {{ 0%,49%{{opacity:1}} 50%,100%{{opacity:0}} }}
    </style>
  </defs>

  <rect width="1200" height="380" fill="url(#bg)"/>
  <g opacity="0.5">
    {grid}
  </g>
{stars()}

{cubes}

  <g filter="url(#glow)">
    <text class="title" x="600" y="74" text-anchor="middle" font-size="50" font-weight="800" fill="{P['text']}">Eyal Delarea</text>
  </g>
  <text x="600" y="112" text-anchor="middle" font-size="19" font-weight="600" fill="{P['accent']}" font-family="'Courier New',monospace">&gt; software developer<tspan class="cursor" fill="{P['accent2']}">_</tspan></text>

{synth()}
</svg>
'''
    with open(os.path.join(OUT,"hero-cyber.svg"),"w") as f:
        f.write(out)
    html='''<!doctype html><html><head><meta charset="utf-8"><title>TB-303 hero</title>
<style>body{margin:0;background:#0d1117;color:#e6edf3;font-family:Arial;padding:24px}
img{width:100%;max-width:1100px;display:block;border:1px solid #30363d;border-radius:12px}
h1{font-weight:800}</style></head><body>
<h1>🎛️ TB-303 hero — Neon Cyber</h1>
<p>6 labelled knobs rotating · scrolling LCD waveform · RUN led · 16-step sequencer · neon keyboard.</p>
<img src="hero-cyber.svg"></body></html>'''
    with open(os.path.join(OUT,"preview.html"),"w") as f:
        f.write(html)
    print("wrote hero-cyber.svg + preview.html")

main()
