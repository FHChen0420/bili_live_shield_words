# B站直播弹幕反屏蔽处理

识别并处理B站直播弹幕中的全局屏蔽字，主要应用于VTB直播同传/歌词弹幕

注意：B站屏蔽字是在不断变化的，本代码也会随缘更新

使用方法示例：
from BiliLiveShieldWords import deal # [as 别名] 导入处理函数
print(deal("初心"))
# 结果：初`心
