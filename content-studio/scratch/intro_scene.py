"""Adegan perkenalan standar (setelah hook) untuk semua reels. Dipakai oleh generator set adegan lewat INTRO_HTML(pid) dan INTRO_JS.
Foto: foto/profil-seminar.jpg (foto pertama di Profile - Aldy Syahreza.pdf, dipotong dari gambar asli 853x1280). Aturan lama 'foto wajah hanya di cover carousel' dikecualikan untuk adegan ini (izin Aldy, 8 Nov 2026)."""
INTRO_TEXT = "Hai, kenalin, saya Aldy Syahreza. Belasan tahun saya membangun dan mendampingi lebih dari seratus brand, lintas industri, dari branding sampai strategi marketing."
INTRO_SHORT = "Sebelumnya, kenalin. Saya Aldy Syahreza. Belasan tahun mendampingi lebih dari seratus brand lintas industri, dari branding sampai strategi marketing."
def INTRO_HTML(p='in'):
    card = lambda i, top, big, sub, col: ('<div class="a" id="%s%d" data-obj style="left:560px;top:%dpx;width:440px;height:128px;border-radius:26px;background:#fff;box-shadow:var(--sh);padding:20px 26px">'
        '<div class="disp" style="font-size:40px;line-height:1;white-space:nowrap;color:%s">%s</div><div style="margin-top:10px;font:700 24px/1.2 var(--f-body);color:#6B6560;white-space:nowrap">%s</div></div>') % (p, i, top, col, big, sub)
    return ('<section class="sc" id="%sx">'
        '<div class="a" id="%sph" data-obj style="left:84px;top:430px;width:440px;height:590px;border-radius:30px;overflow:hidden;box-shadow:var(--sh);background:#B84A2E;transform:rotate(-2deg)"><img src="../foto/profil-seminar.jpg" style="width:100%%;height:100%%;object-fit:cover;object-position:50%% 20%%;display:block"></div>'
        '<div class="a disp" id="%snm" style="left:560px;top:430px;width:440px;font-size:78px;line-height:.92">ALDY<br>SYAHREZA</div>'
        '<div class="a mono" id="%srl" style="left:560px;top:612px;font-size:22px;color:var(--terra)">branding &amp; digital marketing</div>'
        '%s%s%s</section>') % (p, p, p, p,
        card(1, 668, '10+ TAHUN', 'membangun dan mendampingi', '#0F0E0C'),
        card(2, 812, '100+ BRAND', 'lintas industri', '#B84A2E'),
        card(3, 956, '360°', 'branding sampai marketing', '#C8944A'))
# Waktu lokal (detik rancangan); sesuaikan jangkar kata per set: hai, saya, belasan, seratus, lintas, branding
INTRO_JS = r"""
function(t){var P='in';pop($(P+'ph'),t,.15,.5,' rotate(-2deg)');up($(P+'nm'),t,.6,.4,40);up($(P+'rl'),t,1.0,.3,16);
  pop($(P+'1'),t,2.2,.4);pop($(P+'2'),t,4.6,.4);pop($(P+'3'),t,7.0,.4)}
"""
if __name__ == '__main__':
    import json, sys
    v3 = open('/home/user/content-studio/animatic/animatic-v3.html', encoding='utf-8').read()
    head = v3[:v3.index('<div class="bgpaper" id="bgp"></div>')]
    body = '<div class="bgpaper" id="bgp"></div>' + INTRO_HTML().replace('visibility:hidden', '') + '</div></body></html>'
    html = head + body.replace('<section class="sc" id="inx">', '<section class="sc" id="inx" style="visibility:visible">')
    html = html.replace('opacity:0', 'opacity:1')
    open('/home/user/content-studio/animatic/_intro_preview.html', 'w', encoding='utf-8').write(html)
    print('ok')
