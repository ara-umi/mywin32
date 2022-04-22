# 个人用后台键鼠模拟库mywin32

---
## 目标

-	通过win32系列库发送足够真实的后台键鼠消息，从而实现对指定窗口的后台模拟。

-	主要应用场景：安卓模拟器上运行的各类脚本。

## 功能

-	寻找模拟器句柄（handle.py，兼容性未测试）,目前用于测试的模拟器有：Nox和LeiDian

-	键鼠模拟（类似后台版的pyaugui，或低配版的大漠插件）

- <font color='red'> 大部分按键的虚拟键码/扫描码未添加，请自行修改key.json</font>

虚拟键码参考：http://www.atoolbox.net/Tool.php?Id=815

扫描码参考：https://blog.csdn.net/qq_37232329/article/details/79926440

## 更新日志

2021.4.22

-	clickInput（中键相关未编写）

-	pressKey/pressKeyConstant

-	activate/mouseActivate





