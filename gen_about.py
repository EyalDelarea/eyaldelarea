#!/usr/bin/env python3
"""Generate a small animated neon isometric 3D accent for the About section."""
import os
OUT = os.path.dirname(os.path.abspath(__file__))

A   = "#22d3ee"   # cyan
A2  = "#a855f7"   # purple
TOP = "#5eead4"; LEFT="#0891b2"; RIGHT="#0e7490"

def cube(cx, cy, a, H, cls, delay, dur, top=TOP, left=LEFT, right=RIGHT):
    b=a/2
    t=f"{cx},{cy-b} {cx+a},{cy} {cx},{cy+b} {cx-a},{cy}"
    l=f"{cx-a},{cy} {cx},{cy+b} {cx},{cy+b+H} {cx-a},{cy+H}"
    r=f"{cx},{cy+b} {cx+a},{cy} {cx+a},{cy+H} {cx},{cy+b+H}"
    return f'''  <g class="{cls}" style="animation-delay:{delay}s;animation-duration:{dur}s">
    <polygon points="{l}" fill="{left}"/>
    <polygon points="{r}" fill="{right}"/>
    <polygon points="{t}" fill="{top}"/>
  </g>'''

def main():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <defs>
    <filter id="g" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="3.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      .orbit {{ transform-box: fill-box; transform-origin: 120px 130px;
               animation: spin 9s linear infinite; }}
      @keyframes spin {{ from{{transform:rotate(0)}} to{{transform:rotate(360deg)}} }}
      .float {{ transform-box: fill-box; transform-origin: center;
               animation: fl ease-in-out infinite; }}
      @keyframes fl {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-10px)}} }}
      .pop {{ transform-box: fill-box; transform-origin: center bottom;
              animation: pop ease-in-out infinite; }}
      @keyframes pop {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-4px)}} }}
      .tw {{ animation: tw 2s ease-in-out infinite; }}
      @keyframes tw {{ 0%,100%{{opacity:.25}} 50%{{opacity:1}} }}
    </style>
  </defs>

  <!-- isometric base plate -->
  <g opacity="0.85" filter="url(#g)">
    <polygon points="120,150 196,194 120,238 44,194" fill="none" stroke="{A2}" stroke-width="1.5" opacity="0.5"/>
    <polygon points="120,166 168,194 120,222 72,194" fill="none" stroke="{A}" stroke-width="1.2" opacity="0.4"/>
  </g>

  <!-- stacked tower of cubes (builds/deploys) -->
  <g filter="url(#g)">
{cube(120,150,30,22,"pop",0.0,3.0)}
{cube(120,120,30,22,"pop",0.4,3.0)}
{cube(120,90,30,22,"pop",0.8,3.0,top=A,left=LEFT,right=RIGHT)}
  </g>

  <!-- a floating cube above the tower -->
  <g filter="url(#g)">
{cube(120,44,18,14,"float",0.2,2.6,top=A2,left="#7c3aed",right="#6d28d9")}
  </g>

  <!-- orbiting nodes -->
  <g class="orbit">
    <circle class="tw" cx="120" cy="60" r="4" fill="{A}"/>
    <circle class="tw" cx="120" cy="200" r="4" fill="{A2}" style="animation-delay:.7s"/>
    <circle class="tw" cx="50" cy="130" r="3" fill="{A}" style="animation-delay:1.1s"/>
    <circle class="tw" cx="190" cy="130" r="3" fill="{A2}" style="animation-delay:1.5s"/>
  </g>
</svg>
'''
    with open(os.path.join(OUT,"about-3d.svg"),"w") as f:
        f.write(svg)
    print("wrote about-3d.svg")

main()
