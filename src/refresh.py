# -*- coding:utf-8 -*-

# 通过刷新点显示工作状态、
# 程序完成一步后调用 refresh() 刷新界面显示
# length 参数表示刷新点字符串的长度
# 将 length 设定为其它控制台信息的最长长度

dot = 0


def refresh(length=3):
    global dot
    dot += 1
    dots = ""
    for i in range(dot):
        dots += "."
    for i in range(length-dot):
        dots += " "
    print(dots, end="\r")
    if dot == length:
        dot = 0
