"""Contact sheets for visual QA: python contact.py <png_dir> <out_prefix> [per_sheet]"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
d=Path(sys.argv[1]); pre=sys.argv[2]; n=int(sys.argv[3]) if len(sys.argv)>3 else 12
files=sorted(d.glob('*.PNG') or d.glob('*.png'),key=lambda p:int(''.join(c for c in p.stem if c.isdigit()) or 0))
w,h=640,360; cols=3
for i in range(0,len(files),n):
    b=files[i:i+n]; rows=(len(b)+cols-1)//cols
    sheet=Image.new('RGB',(cols*w+(cols+1)*8,rows*(h+8)+8),(120,120,120))
    for j,f in enumerate(b):
        im=Image.open(f).convert('RGB').resize((w,h)); x=8+(j%cols)*(w+8); y=8+(j//cols)*(h+8)
        sheet.paste(im,(x,y)); ImageDraw.Draw(sheet).text((x+4,y+4),str(i+j+1),fill=(200,0,0))
    sheet.save(f'{pre}_{i//n+1:02d}.png')
print(len(files))
