from PIL import Image
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# import requests
# res = requests.get('./up_mother/Pathway/up_mother_map/map00010.html')
# res.encoding = 'utf-8'

def getrectpos(rect:str):
    rect=rect.strip()
    rectpos=[int(x) for x in rect.split(',')]
    return rectpos

data=BeautifulSoup(open('./up_mother/Pathway/up_mother_map/map00010.html'),'html.parser')
maps=data.map
rects=data.map.select("area[onmouseover]")
rectlist=[]
for rect in rects:
    rectlist.append(getrectpos(rect["coords"]))
    # print(rect["coords"])
    # item=BeautifulSoup(rect["onmouseover"][22:-3])
    # print(item.li.li.text)
img=Image.open('./up_mother/Pathway/up_mother_map/map00010.png')
plt.figure("dog")
print(img.size)
plt.imshow(img)
currentAxis=plt.gca()
plt.axis('off')
for rectpos in rectlist:
    rect=patches.Rectangle((rectpos[0], rectpos[1]),rectpos[2]-rectpos[0],rectpos[3]-rectpos[1],linewidth=1,edgecolor='g',facecolor='none')
    currentAxis.add_patch(rect)
plt.savefig("test.png",dpi=300)
