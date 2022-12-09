# -*- coding:utf-8 -*-

import sys
import os
with open(sys.path[0]+"/index.html", "wt")as f:
    f.write("<html>\n")
    f.write("<head></head>\n")
    f.write("<body>\n")
    f.write("<style>\n")
    f.write("body { display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; background: #242424; }\n")
    f.write("img { margin: 5px; width: 128px; height: 128px; border-radius: 15px; transition: 0.2s; display: none; }\n")
    f.write("img:hover, img:active { box-shadow: 0 0 10px #88ddff; }\n")
    f.write("</style>\n")
    for cp, dns, fns in os.walk(sys.path[0]):
        for fn in fns:
            if fn.split(".")[-1].upper() in ["PNG", "JPG", "JPEG", "GIF"]:
                f.write("<img id='img' data-src='./thumb/" + fn+"'>\n")
    f.write("<script>\n")
    f.write("function load() { document.getElementById('img').setAttribute('src', document.getElementById('img').getAttribute('data-src')); document.getElementById('img').style.display = 'block'; document.getElementById('img').id = ''; };\n")
    f.write("window.onload = setInterval(() => {load()}, 1);\n")
    f.write("</script>\n")
    f.write("</body>\n")
    f.write("</html>\n")

fs = 0
for cp, dns, fns in os.walk(sys.path[0]):
    for fn in fns:
        if fn.split(".")[-1].upper() in ["PNG", "JPG", "JPEG", "GIF"]:
            fs += os.path.getsize(cp + "/" + fn)
print(fs)

if __name__ == "__main__":
    pass
