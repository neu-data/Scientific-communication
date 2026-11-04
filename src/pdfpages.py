"""Render PDF pages to contact sheets: python pdfpages.py in.pdf out_prefix [per_sheet]"""
import sys, fitz
from PIL import Image
pdf=fitz.open(sys.argv[1]); pre=sys.argv[2]; n=int(sys.argv[3]) if len(sys.argv)>3 else 8
ims=[]
for p in pdf:
    x=p.get_pixmap(dpi=70); ims.append(Image.frombytes('RGB',(x.width,x.height),x.samples))
print(len(ims),'pages')
w,h=ims[0].size
for i in range(0,len(ims),n):
    b=ims[i:i+n]; cols=4; rows=(len(b)+cols-1)//cols
    sh=Image.new('RGB',(cols*(w+6)+6,rows*(h+6)+6),(120,120,120))
    for j,im in enumerate(b): sh.paste(im,(6+(j%cols)*(w+6),6+(j//cols)*(h+6)))
    sh.save(f'{pre}_{i//n+1:02d}.png')
