from PIL import Image
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re
import sys

#
M = "#DA7736"
P = "#2D9BCE"
S = 'yellow'
both = 'r'

pathway = "map04020"
data_M = './up_mother/Pathway/up_mother_map/{0}.html'.format(pathway)
data_P = './up_father/Pathway/up_father_map/{0}.html'.format(pathway)
data_S = "./shift/Pathway/dominance_map/{0}.html".format(pathway)
img_sc = './map/{0}.png'.format(pathway)


def getrectpos(rect: str):
    rect = rect.strip()
    rectpos = [int(x) for x in rect.split(',')]
    return rectpos


def getKOrect(html):
    print("Processing {0}".format(html))
    dictdata = {}
    data_M = BeautifulSoup(open(html), 'html.parser')
    # maps=data_M.map
    rects = data_M.map.select("area[onmouseover]")
    rectlist = []
    for rect in rects:
        rectpos = getrectpos(rect["coords"])
        # rectlist.append(rectpos)
        key=str(rectpos[0])+"_"+str(rectpos[1])
        # print(rect["coords"])
        item = BeautifulSoup(rect["onmouseover"][22:-3], 'html.parser')
        KO = item.li.li.text.strip().split(":")[0]
        genes = re.findall("Aurat\d*", item.li.li.text)
        if key in dictdata:
            dictdata[key].append([rectpos, genes,KO])
            print("Warnning: The same KO:{0} in one map twice!".format(KO))
            # sys.exit(-1)
            # print(dictdata[KO])
        else:
            dictdata[key] = [[rectpos, genes,KO]]
        # print(KO)
        # print(re.findall("Aurat\d*",item.li.li.text))
    return dictdata


M_KO = getKOrect(data_M)
P_KO = getKOrect(data_P)
S_KO = getKOrect(data_S)

Alldict={}
for key,value in M_KO.items():
    if key not in Alldict:
        Alldict[key]=value
    elif len(value)>len(Alldict[key]):
        Alldict[key]=value
    # if key=="K04459":
    #     print(M_KO[key])
for key,value in P_KO.items():
    if key not in Alldict:
        Alldict[key]=value
    elif len(value)>len(Alldict[key]):
        Alldict[key]=value
    # if key=="K04459":
    #     print(P_KO[key])
for key,value in S_KO.items():
    if key not in Alldict:
        Alldict[key]=value
    elif len(value)>len(Alldict[key]):
        Alldict[key]=value
    # if key=="K04459":
    #     print(S_KO[key])

img = Image.open(img_sc)
Mkoset = set(M_KO.keys())
Pkoset = set(P_KO.keys())
Skoset = set(S_KO.keys())

Msingle = (Mkoset-Pkoset)-Skoset
Psingle = (Pkoset-Mkoset)-Skoset
Ssingle = (Skoset-Mkoset)-Pkoset

Allko = Mkoset|Pkoset|Skoset

Shareko=((Allko-Msingle)-Psingle)-Ssingle

plt.figure("dog")
print(img.size)
plt.imshow(img)
currentAxis = plt.gca()
plt.axis('off')

def addrect(alldict,currentAxis,kos,color):
    for ko in kos:
        # if ko=="K04459":
        #     print(alldict[ko])
        for rectgene in alldict[ko]:
            rect = patches.Rectangle((rectgene[0][0], rectgene[0][1]), rectgene[0][2] - rectgene[0][0], rectgene[0][3] - rectgene[0][1], linewidth=1,
                             edgecolor=color, facecolor='none')
            currentAxis.add_patch(rect)
addrect(Alldict,currentAxis,Msingle,M)
addrect(Alldict,currentAxis,Psingle,P)
addrect(Alldict,currentAxis,Ssingle,S)
addrect(Alldict,currentAxis,Shareko,both)
plt.savefig("{0}_all.png".format(pathway), dpi=300)
