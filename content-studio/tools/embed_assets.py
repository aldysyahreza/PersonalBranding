"""Tanam font (assets/fonts-embed.css) dan pustaka (vendor/*.js) ke content-studio.html.
Aman dijalankan berulang: blok di antara penanda <!-- CS:... --> diganti, bukan ditambah.
Pakai: python3 tools/embed_assets.py [content-studio.html]"""
import re,sys,os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f=sys.argv[1] if len(sys.argv)>1 else os.path.join(root,'content-studio.html')
h=open(f,encoding='utf-8').read()
rd=lambda p:open(os.path.join(root,p),encoding='utf-8').read()
fonts='<!-- CS:FONTS -->\n<style id="cs-fonts">\n'+rd('assets/fonts-embed.css')+'</style>\n<!-- /CS:FONTS -->'
vendor='<!-- CS:VENDOR -->\n<script id="cs-lib-h2i">\n'+rd('vendor/html-to-image.js')+'\n</script>\n<script id="cs-lib-jszip">\n'+rd('vendor/jszip.min.js')+'\n</script>\n<!-- /CS:VENDOR -->'
def put(h,tag,block,fallback):
    pat=re.compile(r'<!-- CS:%s -->.*?<!-- /CS:%s -->'%(tag,tag),re.S)
    if pat.search(h):return pat.sub(lambda m:block,h,count=1)
    k=h.index(fallback);return h[:k]+block+'\n'+h[k:]
gf=re.compile(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\n?')
h=gf.sub('',h)
h=put(h,'FONTS',fonts,'<style>')
h=put(h,'VENDOR',vendor,'<script>\n(function(){')
open(f,'w',encoding='utf-8').write(h)
print('OK',f,round(len(h.encode())/1024),'KB')
