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
(ROOT/'src/image-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
