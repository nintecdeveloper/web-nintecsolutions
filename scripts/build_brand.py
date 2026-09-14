"""Export the approved circuit identity as outlined SVG and small raster fallbacks.
Run only when branding changes (fonttools + cairosvg); normal builds copy committed assets.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import cairosvg
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'src/assets/brand';OUT.mkdir(exist_ok=True)
def lettering(text,font_path,x,y,width,fill):
 font=TTFont(font_path);glyphs=font.getGlyphSet();cmap=font.getBestCmap();advance=0;parts=[]
 for char in text:
  name=cmap[ord(char)];pen=SVGPathPen(glyphs);glyphs[name].draw(pen)
  parts.append(f'<path transform="translate({advance} 0)" d="{pen.getCommands()}"/>');advance+=glyphs[name].width
  if text=='SOLUTIONS':advance+=900
 if text=='SOLUTIONS':advance-=900
 scale=width/advance
 return f'<g fill="{fill}" transform="translate({x} {y}) scale({scale} {-scale})">'+''.join(parts)+'</g>'
defs='<defs><linearGradient id="circuit" gradientUnits="userSpaceOnUse" x1="0" y1="204" x2="204" y2="0"><stop stop-color="#00c8e8"/><stop offset=".48" stop-color="#5362ff"/><stop offset=".78" stop-color="#8025f5"/><stop offset="1" stop-color="#05c8ed"/></linearGradient></defs>'
icon='<g fill="none" stroke="url(#circuit)" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"><path d="M25 157V57C25 23 64 8 88 33L151 96M66 82V112L125 171C153 200 188 184 188 151V51M79 78L133 130"/><circle cx="25" cy="176" r="17"/><circle cx="66" cy="64" r="17"/><circle cx="145" cy="143" r="17"/><circle cx="188" cy="29" r="17"/></g>'
def svg(body,w,h):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'
(OUT/'nintec-icon.svg').write_text(svg(defs+icon,216,204))
for theme,main,sub in [('light','#171c2b','#3c4150'),('dark','#ffffff','#d3d7e2')]:
 body=defs+'<g transform="translate(0 1) scale(.30)">'+icon+'</g>'
 body+=lettering('Nintec','/System/Library/Fonts/Supplemental/Arial Bold.ttf',80,44,157,main)
 body+=lettering('SOLUTIONS','/System/Library/Fonts/Supplemental/Arial.ttf',82,62,153,sub)
 (OUT/f'nintec-logo-horizontal-{theme}.svg').write_text(svg(body,240,64))
for name,size in [('favicon',64),('apple-touch-icon',180),('nintec-icon',512)]:
 # Square canvas with transparent breathing room; never stretch the circuit.
 body=defs+'<g transform="translate(20 26)">'+icon+'</g>'
 cairosvg.svg2png(bytestring=svg(body,256,256).encode(),write_to=str(OUT/(name+'.png')),output_width=size,output_height=size)
# Preserve the existing OG layout/copy; replace only the branding component.
logo=(OUT/'nintec-logo-horizontal-dark.svg').read_text();inner=logo[logo.index('>')+1:logo.rindex('</svg>')]
body='<rect width="1200" height="630" fill="#202029"/><g transform="translate(76 120) scale(3.8)">'+inner+'</g>'
body+='<text x="80" y="495" font-family="Arial,sans-serif" font-size="24" fill="#c1b1f4">Nintec360  /  Nintec Finance  /  Nintec Compliance</text><path d="M80 562H1120" stroke="#7250d6" stroke-width="3"/>'
cairosvg.svg2png(bytestring=svg(body,1200,630).encode(),write_to=str(OUT/'social-card.png'))
print('Brand SVGs and PNG fallbacks exported')
