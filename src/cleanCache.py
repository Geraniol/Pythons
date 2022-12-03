#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 清除指定目录下的系统垃圾文件
# path 参数指定需要清理的目录
# 默认值为清理当前文件所在目录

def cleanCache(path=False):
    import os
    import shutil
    if not path:
        import sys
        path = sys.path[0]
    for cp, dns, fns in os.walk(path):
        for n in fns+dns:
            if n[0:2] == "._" or n in ["Thumbs.db", ".DS_Store", "__MACOSX"]:
                try:
                    try:
                        shutil.rmtree(cp+"/"+n)
                    except:
                        os.remove(cp+"/"+n)
                    print("Deleted: "+cp+"/"+n)
                except:
                    print("Error: "+cp+"/"+n)
    print("所有缓存文件已被清除。")


if __name__ == "__main__":
    cleanCache()
