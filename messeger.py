#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

import win32api
import win32con
import win32gui

import mywin32con as con
from handle import HandleGetter
from hexHelper import d2bK, d2xK
from key import keyDict


def _makeLong(position):
    return win32api.MAKELONG(*position)


def clickInput(handle, position, button, delay=0):
    """
    :param handle:
    :param position: tuple
    :param button:
        LEFT_BUTTON = 1
        RIGHT_BUTTON = 0
        MID_BUTTON = 2
    :param delay: sleep time(default 0)
    :return: None
    """
    long = _makeLong(position)
    if button == con.LEFT_BUTTON:
        win32gui.PostMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long)
        time.sleep(delay)
        win32gui.PostMessage(handle, win32con.WM_LBUTTONUP, 0X00000000, long)
    elif button == con.RIGHT_BUTTON:
        win32gui.PostMessage(handle, win32con.WM_RBUTTONDOWN, win32con.MK_LBUTTON, long)
        time.sleep(delay)
        win32gui.PostMessage(handle, win32con.WM_RBUTTONUP, 0X00000000, long)
    elif button == con.MID_BUTTON:
        print("中键还没写，你急啥")


def doubleClick(handle, position, button):
    """
    wParam 指示各种虚拟密钥是否关闭。 此参数可以是以下一个或多个值。
    MK _CONTROL 0x0008 CTRL 键关闭。
    MK _LBUTTON 0x0001 鼠标左键关闭。
    MK _MBUTTON 0x0010 鼠标中键关闭。
    MK _RBUTTON 0x0002 鼠标右键关闭。
    MK _SHIFT 0x0004 SHIFT 键关闭。
    MK _XBUTTON1 0x0020 X 按钮关闭。
    MK _XBUTTON2 0x0040 第二个 X 按钮关闭。
    """
    long = _makeLong(position)
    if button == con.LEFT_BUTTON:
        win32gui.PostMessage(handle, win32con.WM_LBUTTONDBLCLK, 0x000001, long)
        win32gui.PostMessage(handle, win32con.WM_LBUTTONUP, 0X00000000, long)
    elif button == con.RIGHT_BUTTON:
        win32gui.PostMessage(handle, win32con.WM_RBUTTONDBLCLK, 0x0000, long)
        win32gui.PostMessage(handle, win32con.WM_RBUTTONUP, 0X00000000, long)
    elif button == con.MID_BUTTON:
        print("中键还没写，你急啥")


# 暂时未发现repeat对实际效果产生的影响
def _makeKeydownLPara(scancode, previous_state: int, extended: int, repeat=1):
    """
    :param scancode: 扫描码，通过scancode读取
    :param previous_state: 前状态，DOWN为1，UP为0，持续点击时会用到这个参数
    :param extended: 若为拓展键，该值为1
         such as the right-hand ALT and CTRL keys that appear on an enhanced 101- or 102-key keyboard
    :param repeat:重复次数，默认为1
    :return:int
    """
    # 转换状态，对于WM_KEYDOWN消息，该值始终为0
    transitionState = "0"
    # 前状态，对于WM_KEYDOWN消息，该值始终为0
    previousState = str(previous_state)
    # 上下文，对于WM_KEYDOWN消息，该值始终为0
    contextCode = "0"
    # 保护勿使用
    unused = "0000"
    # 拓展键
    extended = str(extended)
    # 扫描码
    scanCode = d2bK(scancode, 8)[2:]
    # 重复次数
    repeatCount = d2bK(repeat, 16)[2:]
    lpStr = transitionState + previousState + contextCode + unused + extended + scanCode + repeatCount
    return int(lpStr, 2)


def _makeKeyupLPara(scancode, extended: int, repeat=1):
    """
    :param scancode: 扫描码，通过scancode读取
    :param extended: 若为拓展键，该值为1
         such as the right-hand ALT and CTRL keys that appear on an enhanced 101- or 102-key keyboard
    :param repeat:重复次数，默认为1
    :return: int
    """
    # 转换状态，对于WM_KEYUP消息，该值始终为1
    transitionState = "1"
    # 前状态，对于WM_KEYUP消息，该值始终为1
    previousState = "1"
    # 上下文，对于WM_KEYDOWN消息，该值始终为0
    contextCode = "0"
    # 保护勿使用
    unused = "0000"
    # 拓展键
    extended = str(extended)
    # 扫描码
    scanCode = d2bK(scancode, 8)[2:]
    # 重复次数
    repeatCount = d2bK(repeat, 16)[2:]
    lpStr = transitionState + previousState + contextCode + unused + extended + scanCode + repeatCount
    return int(lpStr, 2)


def pressKey(handle, key: str, extend=0, show_para=False):
    """
    模拟快速点击按键
    :param handle: 句柄
    :param key: str 按键字符串，详情参考json
    :param extend: 拓展键
    :param show_para: 打印详细参数(调试用)
    :return: None
    """
    markCode = int(keyDict[key]["mark"], 16)
    keydownLPara = _makeKeydownLPara(markCode, 0, extend)
    keyupLPara = _makeKeyupLPara(markCode, extend)

    if show_para:
        print("KEYDOWN:\nwpara:", d2xK(keyDict[key]["vk"], 8), "\tlpara:", d2xK(keydownLPara, 8))
        print("KEYUP:\nwpara:", d2xK(keyDict[key]["vk"], 8), "\tlpara:", d2xK(keyupLPara, 8))

    win32gui.PostMessage(handle, win32con.WM_KEYDOWN, keyDict[key]["vk"], keydownLPara)
    time.sleep(0.2)
    win32gui.PostMessage(handle, win32con.WM_KEYUP, keyDict[key]["vk"], keyupLPara)


# 长按是通过连续发送消息实现的，会有误差，和计算机处理速度也有关系
# 优化可以写成while True到时间了break，感觉没必要，测试结果误差不超过0.1秒
def presKeyConstant(handle, key: str, extend=0, *, press_time=1):
    """
    模拟长按
    :param handle: 句柄
    :param key: str 按键字符串，详情参考json
    :param extend: 拓展键
    :param press_time: 时间
    :return: None
    """
    markCode = int(keyDict[key]["mark"], 16)
    keydownLPara0 = _makeKeydownLPara(markCode, 0, extend)
    keydownLPara1 = _makeKeydownLPara(markCode, 1, extend)
    keyupLPara = _makeKeyupLPara(markCode, extend)

    win32gui.PostMessage(handle, win32con.WM_KEYDOWN, keyDict[key]["vk"], keydownLPara0)
    for loop in range(press_time * 5):
        win32gui.PostMessage(handle, win32con.WM_KEYDOWN, keyDict[key]["vk"], keydownLPara1)
        time.sleep(0.194)
    win32gui.PostMessage(handle, win32con.WM_KEYUP, keyDict[key]["vk"], keyupLPara)


def _makeMouseActiveLpara(msg, hittest):
    hittestCode = d2bK(hittest, 16)[2:]
    msgCode = d2bK(msg, 16)[2:]
    return int(msgCode + hittestCode, 2)


# 实践发现mouseactivate(目前的状态是失败且不好用)，不如能用非鼠标激活的activate
def mouseActivate(handle, top_handle, mouse_message, hittest):
    """
    :param handle: 窗口
    :param top_handle: 顶级父窗口
    :param mouse_message: 激活时鼠标信息，常用WM_LBUTTONDOWN
    :param hittest:
        win32con.HTCLIENT = 1
    :return:
    """
    lpara = _makeMouseActiveLpara(mouse_message, hittest)
    win32gui.SendMessage(handle, win32con.WM_MOUSEACTIVATE, top_handle, lpara)


def activate(handle, top_handle):
    """
    默认采用非鼠标点击的方式激活非最小化窗口(若需要自定义请自行修改)
    wpara：
        低序：
            WM_ACTIVE: 非鼠标方式激活 1
            WM_CLICKACTIVE: 鼠标激活 2
            WA_INACTIVE: 禁用 0
        高序:
            非零说明窗口最小化(待测试)
    lpara: 通常指激活窗口的句柄
    """
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, 0x00000001, top_handle)


# 待测试
def captureChanged(handle):
    win32gui.SendMessage(handle, win32con.WM_CAPTURECHANGED, 0x00000000)


if __name__ == '__main__':
    # simulatorHandle, clientHandle = HandleGetter.LeiDian()
    # print(f"主窗口句柄:{d2xK(simulatorHandle, 8)}\n客户区句柄:{d2xK(clientHandle, 8)}")
    clientHandle = HandleGetter.Genshin()
    activate(clientHandle, clientHandle)

    # position = (100, 100)
    # clickInput(clientHandle, position, con.LEFT_BUTTON)

    startTime = time.time()
    presKeyConstant(clientHandle, "E", press_time=2)
    print(time.time() - startTime)
