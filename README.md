# B站直播弹幕反屏蔽处理

识别并处理B站直播弹幕中的全局屏蔽字，目前主要用于提高VTB直播时的同传/歌词弹幕的存留率

注意：B站屏蔽字是在不断变化的，本代码也会随缘更新

代码示例：

from BiliLiveShieldWords import deal # [as 别名] 导入处理函数

print(deal("初心 asmr"))

'''
初`心 αsmr
'''
