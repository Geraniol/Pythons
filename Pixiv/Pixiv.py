# -*- coding:utf-8 -*-


import requests


# -------------------------------- 参数 --------------------------------
# phpsessid: 从已登陆浏览器的 Cookie 中复制 PHPSESSID
phpsessid = ""
# -------------------------------- 参数 --------------------------------


false = true = null = None


userAgent = "Mozilla/5.0"
cookie = "PHPSESSID=" + phpsessid
account = int(phpsessid.split("_")[0])
timeout = 5


pixivHeaders = {
    "User-Agent": userAgent,
    "Cookie": cookie
}

pximgHeaders = {
    "User-Agent": userAgent,
    "referer": "https://www.pixiv.net/"
}


def report(error=""):
    return
    input('运行错误：' + error + "按下回车以继续。")


def getFollowingId(account):
    userId = []
    i = 0
    while True:
        url = "https://www.pixiv.net/ajax/user/" + \
            str(account) + "/following?offset=" + \
            str(100*i) + "&limit=100&rest=show"
        try:
            page = requests.get(url, headers=pixivHeaders, timeout=timeout)
            if page.status_code == 200:
                page = page.text
            else:
                report("第 " + str(i) + " 关注页返回了 " +
                       str(page.status_code) + " 状态码。")
            users = eval(page)["body"]["users"]
            if not users:
                break
            for user in users:
                userId.append(int(user["userId"]))
        except:
            report("读取第 " + str(i) + " 关注页出现错误。")
        i += 1
    return userId


def getAuthorPicId(uid):
    picId = []
    url = "https://www.pixiv.net/ajax/user/" + str(uid) + "/profile/all"
    try:
        page = requests.get(url, headers=pixivHeaders, timeout=timeout)
        if page.status_code == 200:
            page = page.text
        else:
            report(str(uid) + " 用户页返回了 " + str(page.status_code) + " 状态码。")
        pics = eval(page)["body"]["illusts"]
        if not pics:
            report("找不到此用户 " + str(uid) + " 的作品。")
        for pic in pics:
            picId.append(int(pic))
    except:
        report("读取 " + str(uid) + " 用户页出现错误。")
    return picId


def getAllPicUrl(pid, size=["original", "regular", "small", "thumb_mini"][0]):
    picUrl = []
    url = "https://www.pixiv.net/ajax/illust/" + str(pid) + "/pages"
    try:
        page = requests.get(url, headers=pixivHeaders, timeout=timeout)
        if page.status_code == 200:
            page = page.text
        else:
            report(str(pid) + " 作品页返回了 " + str(page.status_code) + " 状态码。")
        urls = eval(page)["body"]
        for url in urls:
            try:
                picUrl.append(url["urls"][size].replace("\\", ""))
            except:
                report("照片类型 " + size + " 无法读取。")
    except:
        report("读取 " + str(pid) + " 作品页出现错误。")
    return picUrl


def getPic(url):
    try:
        page = requests.get(url, headers=pximgHeaders, timeout=timeout)
        if page.status_code == 200:
            return page.content
        else:
            report(url + " 返回了 " + str(page.status_code) + " 状态码。")
    except:
        report("下载 " + url + " 出现错误。")


def getAuthorAllPic(uid):
    from io import BytesIO
    from PIL import Image
    for pid in getAuthorPicId(uid):
        for url in getAllPicUrl(pid, size="thumb_mini"):
            Image.open(BytesIO(getPic(url))).show()


def getAllPic(uid):
    import sys
    import os
    for uid in getFollowingId(account):
        for pid in getAuthorPicId(uid):
            for url in getAllPicUrl(pid, size="thumb_mini"):
                if not os.path.isfile(sys.path[0] + "/thumb/" + str(uid) + "_" + url.split("/")[-1].upper()):
                    with open(sys.path[0] + "/thumb/" + str(uid) + "_" + url.split("/")[-1].upper(), "wb")as f:
                        f.write(getPic(url))


def getAllPicx(uid, pid):
    import sys
    import os
    for url in getAllPicUrl(pid, size="thumb_mini"):
        if not os.path.isfile(sys.path[0] + "/thumb/" + str(uid) + "_" + url.split("/")[-1].upper()):
            with open(sys.path[0] + "/thumb/" + str(uid) + "_" + url.split("/")[-1].upper(), "wb")as f:
                f.write(getPic(url))
            exit()


def getAllPicMult(account):
    import threading
    threads = []
    for uid in getFollowingId(account):
        for pid in getAuthorPicId(uid):
            t = threading.Thread(target=getAllPicx, args=(uid, pid))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()


def cleanZeros():
    import os
    import sys
    for cp, dns, fns in os.walk(sys.path[0]):
        for fn in fns:
            if not os.path.getsize(cp+"/"+fn):
                os.remove(cp+"/"+fn)


# -------------------------------- 示例 --------------------------------
# print("\033c", end="")

# getFollowingId( integer-account ) -> list-UIDs: list of integers
# 输入用户 ID 获取所有关注者 UID
# print(getFollowingId(account))

# getAuthorPicId( integer-UID ) -> list-PIDs: list of integers
# 输入作者 UID 获取作者所有作品 PID
# print(getAuthorPicId(212801))

# getAllPicUrl( integer-PID, string-Size ) -> list-URLs: list of strings
# 输入作品 PID 与类型 Size 获取作品所有图片 URL
# print(getAllPicUrl(78551403))

# getPic( string-URL ) -> bytes-image: image file
# 输入图片 URL 获取图片文件
# if True:
#     from io import BytesIO
#     from PIL import Image
#     Image.open(BytesIO(getPic(
#         "https://i.pximg.net/img-original/img/2019/12/29/00/00/13/78551403_p0.jpg"))).show()
# -------------------------------- 示例 --------------------------------


getAllPicMult(account)


if __name__ == "__main__":
    pass
