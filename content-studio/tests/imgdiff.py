# Skor beda dua gambar: rata-rata selisih piksel (0-255) dan % piksel yang berbeda jelas (>40).
import sys
from PIL import Image,ImageChops
a=Image.open(sys.argv[1]).convert('RGB');b=Image.open(sys.argv[2]).convert('RGB')
size=b.size;a=a.resize(size,Image.LANCZOS)
d=ImageChops.difference(a,b).convert('L');h=d.histogram();n=size[0]*size[1]
mean=sum(i*c for i,c in enumerate(h))/n;big=sum(h[41:])/n*100
print('ukuran=%dx%d beda_rata=%.2f piksel_beda=%.2f%%'%(size[0],size[1],mean,big))
