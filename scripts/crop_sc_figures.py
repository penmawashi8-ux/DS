# 午後問題の図を IPA の問題冊子 PDF から切り出して sc/<回ID>/fig/ に保存する。
# 使い方: 各回の問題PDFを pdftoppm -r 200 -gray -png pdf/<回ID>_sc_pm_qs.pdf <dir>/<回ID> で画像化し，
#   python3 scripts/crop_sc_figures.py <dir> [<回ID>_<問>_<図> ...]
# 座標は 1/4 縮小したページ画像（358x506）上の位置。切り出した後に余白を詰める。
from PIL import Image, ImageOps
import json,sys,os
S = sys.argv.pop(1) if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]) else "pdfpages"
FIG={ # key: (exam,q,name): [(page,(x0,y0,x1,y1)),...]  thumbnail coords (x4)
 ("2023r05a",1,"fig2"):[(3,(35,113,295,256))],
 ("2023r05a",2,"fig1"):[(8,(25,42,328,242))],
 ("2023r05a",4,"fig1"):[(23,(38,225,305,290))],
 ("2023r05a",4,"fig2"):[(25,(35,42,328,142))],
 ("2024r06a",1,"fig1"):[(2,(38,158,330,349))],
 ("2024r06a",2,"fig1"):[(12,(70,348,295,441))],
 ("2024r06a",3,"fig1"):[(23,(50,60,305,358))],
 ("2024r06a",4,"fig3"):[(32,(30,22,324,442)),(33,(32,42,328,165))],
 ("2024r06h",1,"fig2"):[(4,(35,165,320,250))],
 ("2024r06h",2,"fig1"):[(13,(45,255,325,368))],
 ("2024r06h",3,"fig1"):[(23,(30,48,332,176))],
 ("2025r07a",2,"fig1"):[(8,(55,353,348,442))],
 ("2025r07a",3,"fig1"):[(16,(45,170,340,266))],
 ("2025r07a",3,"fig4"):[(20,(52,50,305,230))],
 ("2025r07a",3,"fig5"):[(21,(65,38,298,150))],
 ("2025r07a",4,"fig1"):[(26,(82,283,302,393))],
 ("2025r07a",4,"fig3"):[(27,(38,228,345,398))],
 ("2025r07h",1,"fig2"):[(6,(38,196,318,290))],
 ("2025r07h",1,"fig3"):[(8,(35,40,322,223))],
 ("2025r07h",2,"fig3"):[(16,(70,140,282,250))],
 ("2025r07h",3,"fig1"):[(20,(42,348,312,432))],
 ("2025r07h",3,"fig3"):[(21,(40,231,335,345))],
 ("2025r07h",3,"fig4"):[(22,(30,42,310,212))],
 ("2025r07h",3,"fig7"):[(24,(52,282,348,402))],
 ("2025r07h",3,"fig9"):[(26,(45,97,318,403))],
 ("2025r07h",4,"fig1"):[(29,(42,165,348,308))],
}
only=sys.argv[1:]
for (e,q,n),parts in FIG.items():
    if only and f"{e}_{q}_{n}" not in only: continue
    ims=[]
    for p,(x0,y0,x1,y1) in parts:
        pg=Image.open(f"{S}/{e}-{p:02d}.png").convert("L")
        c=pg.crop((x0*4,y0*4,x1*4,y1*4))
        bb=ImageOps.invert(c).point(lambda v:255 if v>60 else 0).getbbox()
        c=c.crop((max(bb[0]-12,0),max(bb[1]-12,0),min(bb[2]+12,c.width),min(bb[3]+12,c.height)))
        ims.append(c)
    W=max(i.width for i in ims); H=sum(i.height for i in ims)+30*(len(ims)-1)
    out=Image.new("L",(W,H),255); y=0
    for i in ims: out.paste(i,(0,y)); y+=i.height+30
    out=out.quantize(16).convert("L")
    os.makedirs(f"sc/{e}/fig",exist_ok=True)
    out.save(f"sc/{e}/fig/q{q}_{n}.png",optimize=True)
    print(e,q,n,out.size,os.path.getsize(f"sc/{e}/fig/q{q}_{n}.png")//1024,"KB")
