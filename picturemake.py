# from PIL import Image
from bs4 import BeautifulSoup
data=BeautifulSoup(open("./up_mother/Pathway/up_mother_map/map00010.html"))
maps=data.map
rects=data.map.select("area[onmouseover]")
for rect in rects:
    print(rect["onmouseover"])