"""Create responsive variants from supplied originals; never alter originals."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json
ROOT=Path(__file__).resolve().parents[1];assets=ROOT/'src/assets';manifest={}
for name in ['joel.avif','marc.avif','adam.jpeg','gerard.jpeg','linus.png']:
 source=assets/name;im=ImageOps.exif_transpose(Image.open(source)).convert('RGB');variants=[]
 for width in sorted({min(320,im.width),min(640,im.width)}):
  out=assets/(source.stem+'-'+str(width)+'.webp');resized=im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS);resized.save(out,'WEBP',quality=82,method=6)
  variants.append({'file':out.name,'width':resized.width,'height':resized.height,'bytes':out.stat().st_size})
 manifest[source.stem]={'original_bytes':source.stat().st_size,'variants':variants}
logo=Image.open(assets/'logo-mark.png').convert('RGB')
logo.resize((96,60),Image.Resampling.LANCZOS).save(assets/'logo-mark-96.webp','WEBP',quality=88,method=6)
fontdir=Path('/System/Library/Fonts/Supplemental')
font=ImageFont.truetype(str(fontdir/'Arial.ttf'),72);small=ImageFont.truetype(str(fontdir/'Arial.ttf'),24)
card=Image.new('RGB',(1200,630),'#202029');draw=ImageDraw.Draw(card)
card.paste(logo,(76,92));draw.text((76,390),'Nintec Solutions',font=font,fill='white');draw.text((80,495),'Nintec360  /  Nintec Finance  /  Nintec Compliance',font=small,fill='#c1b1f4')
draw.line((80,562,1120,562),fill='#7250d6',width=3);card.save(assets/'social-card.png',optimize=True)
favicon=Image.new('RGBA',(64,64),(0,0,0,0));mini=logo.resize((64,40),Image.Resampling.LANCZOS);favicon.paste(mini,(0,12));favicon.save(assets/'favicon.png',optimize=True)
(ROOT/'src/image-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
