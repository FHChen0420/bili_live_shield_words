# coding: utf-8
import re

# <DATA BEGIN>
# 拼音对应的常用汉字
hz_xi="夕兮吸汐西希析昔茜奚唏栖息悉惜淅犀晰腊锡皙溪嘻嬉窸稀蹊蟋曦习席袭洗喜戏系细隙"
hz_jin_jing="巾今斤金矜津筋禁仅尽紧谨锦劲进近浸烬晋京径经荆惊晶睛鲸井景净竞竟靓敬静境镜颈精"
hz_pin_ping="拼贫频品聘乒平评凭坪屏瓶苹萍"
hz_ba="八巴扒叭坝把吧芭爸拔疤笆粑耙罢捌跋靶魃霸"
hz_jiu="九久旧纠臼究鸠玖灸咎疚韭赳柩酒阄救厩就揪啾舅鹫"
hz_bai="白百伯呗佰拝败拜柏掰摆"
hz_du="妒杜肚笃毒独度读堵渎犊椟赌渡嘟督睹镀" # 排除：竺都
hz_liu_lu="六刘柳浏流留琉硫碌溜馏遛榴瘤卢庐芦陆卤虏炉录鸬赂鹿颅绿鲁禄鲈路噜撸辘戮橹璐鹭露" # 重复：六碌
hz_si_shi="四司丝死寺似私祀伺饲驷食思斯肆嗣厮撕嘶十尸士氏什示矢石史市失仕世式师时识始饰视鸤虱实驶事势使侍诗试施恃柿是蚀拭适室狮拾屎峙舐轼逝硕匙释湿谥弑誓嗜噬螫" # 重复：似食
#hz_wei="卫为韦未危伪伟围纬尾违苇位委味畏威娓维惟唯帷萎偎谓尉喂猥痿微蔚薇魏巍"
hz_wei_1="卫未位味畏维萎谓尉喂蔚"
hz_wei_2="为伟围维唯魏"
hz_ni="尼拟泥妮昵逆倪匿腻溺霓" # 排除：你

# 部分英文字母的处理规则字典（一般替换为希腊字母或全角字母）
letter={
    "a":"α", "A":"Α",
    "k":"κ", "K":"Κ",
    "l":"ｌ", "L":"Ｌ",
    "o":"ο", "O":"Ｏ",
    "r":"ꭇ", "R":"Ꮢ",
    "t":"τ", "T":"Т",
    "x":"χ", "X":"Χ",
    "y":"у", "Y":"Υ",
}

# 屏蔽词列表
words =  [ 
    ### 一般屏蔽词（易变动）
    "即位", "修正", "领导", "特权", "候选", "警察", "军队", "部队", "政府", "领袖", 
    "在任", "下台", "冷战", "小熊", "汪洋", "提案", "红通", "腐败", "总理", "总统",
    "圣战", "吼哇", "卫兵", "国歌", "和谐", "河蟹", "八路", "郭嘉", "果加", "菓加",  
    "天安", "安门", "审查", "番号", "之那", "赤字", "出访", "民众", "国会", "选举",
    "生事", "闹事", "闹剧", "游行", "颠覆", "起义", "抗争", "革命", "乱暴", "暴乱",
    "分裂", "萨德", "煽动", "倒台", "政策",
    "囚禁", "施虐", "虐待", "捆绑", "割腕", "剥削", "贿赂", "匕首", "鞭尸", "自残",
    "借贷", "贷款", "传销",
    "疫情", "新冠", "包粉", "白粉", "媚药",
    "中出", "高潮", "被透", "走光", "诱惑", "双飞", "梆硬", "女同", "男同", "工口",
    "喘气", "喘息", "呻吟", "处男", "绅士", "性癖", "无码", "开冲", "抖m" , "h漫" ,
    "胖次", "欧派", "罩杯", "嘿咻", "内内", "吹气", "掏耳", "助眠", "蛋大", "脏病",
    "重口", "勃起", "出轨", "黑化", "叫鸡", "痴汉", "进裙", "奶头", "鸡儿", "给日",
    "肉便", "玩逼", "看腿",
    "肥猪", "下贱", "你妈", "月半", "送妈", "嘴臭", "拉屎", "撤硕", "我日", "低俗",
    "憨批",
    "美国", "米国", "台湾", "香港", "澳门", "成都", "日吹",
    "油管", "推特", "微博", "新浪", "抖音", "优酷", 
    "皇帝", "皇宫", "庙堂", "磕头", "还愿", "安乐", "包养", "清真",
    "赌博", "扑克", "彩票", "发票", "博彩", "菠菜", "硫酸", "甲烷", "煤气",
    "四六", "五四", "七一", "七五", "九八",
    "黑魂", "如龙",
    "即为", "试看", "豪迈", "耳语", "迷途", "触摸", "初心", "慎重", "三尺", "鲍鱼",
    "许愿", "代打", "躺平", "要素", "上街", "读错", "下乡", "闪灵", "退钱",
    "百年", "鸡脖", "红魔", "庆典", "广场", "秃鹰", "细腻", "泼墨", "发酵", "电竞",
    "一哥", "动森", "鸣人", "映画", "老母", "青蛙", "秃子", "矮子", "口误", "连睡",
    "黑幕", "猎奇", "冲塔", "逆行", "太安", "膜导",
    "与正", "蒂亚", "稻上", "飞草", "熊学", "伐龙", "家明", "马云", "唐可", "泽东",
    "ロリ", "はま", "ハマ", "しな", "シナ", "くま", "エロ",

    "hw", "gc", "cjp", "cnm", "gay", "ghs", "kui", "lsp", "nmb", "nmd", "ply", "tmd", "usl", "xxd",
    "boki", "dang", "drug", "fuck", "isis", "knee", "kuma", "loli", "sina", "yuan",
    "bajiu", "bitch", "luoli", "obama", "ruler", "sager", "secom", "shina", "hentai", "reddit", "signal", "tiktok",
    "excited", "youtube", "exciting", "onedrive", "revolution", "neverforget",
    "535", "586", "604", "809", "817", "881", "918", "1926", "1953", "1979", "1989", "g7", "j8", "g20", "r19",
    "不想活", "自由门", "咖啡因", "死灵魂", "白衬衫", "生理期", "空气炮", "黑历史", "就去泡", "一本道",
    "被传染", "网易云", "爱奇艺", "支付宝", "劈腿男", "缘之空", "一起死", "稻田上", "安眠药", "接班人", 
    "纪念日", "为自由", "莉莉安", "李医生", "右大人", "绞肉机", "不唱歌", "女菩萨", "毕业歌", "老鼠台", 
    "梦大师", "脱衣服", "我要射", "度一下", "来一发", "小柜子", "奇酷比", "比基尼", "【萝莉", "就这？",
    "性骚扰", "妖妖灵", "蛋炒饭", "异教徒", "跑得快", "顶不住", "劳动法", "斯大林", "这垃圾", "未成年",
    "麻酥酥", "兼职加", "水好多", "滚出去", "黄段子", "给我滚", "没衣服", "玻璃心", "黎明杀", "逃生2",
    "四一二", "五三五", "八一七", "九一八", "九九六", "一九二六", "一九五三", 
    "自由之门", "继续前进", "并肩同行", "焕然一新", "二氧化碳", "阿里巴巴", "恐怖分子", "恐怖份子", "田所浩二", "蒙古上单",
    "身经百战", "黑框眼镜", "谈笑风生", "无可奉告", "活不下去", "飘飘欲仙", "分割人生", "坟头蹦迪", "b站员工" , "波涛汹涌",
    "我是黄金", "没有敌人", "少女之心", "奥斯曼人", "奥数魔刃", "奥数魔人", "孩子的鞋", "花花公子", "不想回忆", "最大限度",
    "脑子瓦特",
    "黑暗之魂", "求生之路", "上古卷轴", "侠盗飞车", "尸体派对", "动物之森",
    "1月23", "7月1日", "7月5日", "7月13", "8月17日", "12月28", "你是你我是我", #汉字格式的日期也会被屏蔽，这里没写出来

    ### 字符间隔相关
    "回#1来#3谢", "姐#1姐#5[逼b]", "妹#1妹#5[逼b]", "6#2月#24", "[逼b]#3看#1吗", "搜#3这#1个", "投#3比#1赛", "看#3头#1像", "同#3性#3恋",
    "道#3上#3飞", "名#3字#3看", "我#3是#3处", "下#3面#3好", "[白干]#3一#3下", "少#3女#3[下自]", "直#3播#3[日草艹操曰]",
    "射#4身#1上", "童#4收#1养", "买#4烟#1花", "删#4评#1论", "v#4b#3o", "天#4安#4门", "萝#4莉#4控", "[你尼]#4[妈吗玛马]#4[币比逼必猪狗b]",
    "手#5指#5插", "[鲁撸露]#5一#5发", "徐#5上#5爽", "[徐许]#5[上玩]#5[碧双霜]",
    "[日草艹操干曰死烧解]#6[你我他她它]#5[妈吗马嘛母m]", "r#1i#6[你我他她它]#5[妈吗马嘛母m]", "文#6古#6花", "看#6地#6方", "不#6钱#6[啊3]",
    "准#1备#3纸#1巾", "那#1个#4奶#1奶", "羊#1羊#4结#1婚", "学#1生#4学#1生", "妈#1妈#6唱#1歌", "不#1论#6生#1死", "找#1工#1作#3加",
    "你#3画#3我#3猜", "清#6透#6世#6界", "w#4e#4i#4b#4o", "一#6个#6人#6寂#6寞",
    
    "吉#1[尔儿]", "野#1[爹妈]", "射#1[爆爽]", "法#1[会能弄]", "乳#1[头首量]", "称#1[王皇帝]", "涩#1[气批片p]", "精#1[美日湛子]", "魂#1[一二三123]",
    "大#1[麻吊弔胸波奶]", "点#1[人1cfl]", "死#1[吧妈法ね]", "色#1[图情皮批逼戒b]",
    "[逼b]#1里", "[批阴]#1毛", "[吞吃]#1精", "[左右]#1倾", "[两二2]#1会", "[玩双晕]#1奶", "[杀去爽干操草爹妈]#1死", "[处下熟]#1女", "[调传宗]#1教", "[鸡己性]#1吧", "[湿射硬]#1了",
    "[贫小平双]#1乳", "[条包孢窑梯]#1子", "[插吸]#1[你他她它]", "[.。·]#1[cf]", "[傻沙煞撒]#1[逼比笔]",
    "网#2恋", "巨#2乳", "自#2尽", "涩#2情", "人#2权", "逼#2真", "[逼b]#2毛", "湿#2视#2频",
    "支#3那", "去#3搜", "百#3d", "自#3杀", "共#3产", "毛#3东", "手#3银", "涩#3图", "肉#3棒",
    "[涩色]#3网", "被#3[日草艹操曰]", "[习習吊弔]#3大", "[草艹操]#3b", "[下压]#3注", "[黄色h]#3片", "[做作坐座]#3爱", 
    "六#4四", "八#4九", "车#4震", "援#4交", "后#4入", "天#4门", "流#4世", "主#4席", "黄#4网", "阴#4道", "赤#4毒",
    "明#4[泽z]", "[小进]#4平", "[连再]#4任", "[看好]#4胸", "[日草艹操干曰吃]#4[姐妹奶姨吊弔]", 
    "留#5水", "性#5爱", "威#5雄",
    "康#6买", "罗#6莉", "宽#6衣", "萝#6[利俐]", "[逼b]#6紧", "[习習]#6[近进]",
    
    ### 拼音/部首组合相关
    "[两量凉梁良粮粱]#4[加家架假甲嫁佳贾驾茄夹+]#4[和河何呵喝核合盒贺禾荷]", #待补充
    "[%s]#1[%s]"%(hz_wei_1,hz_ni),
    "[%s]#1尼"%(hz_wei_2),
    "[%s]#1都"%(hz_bai),
    "[%scx]#2[%s呼砰怦秤抨]"%(hz_xi,hz_pin_ping),
    "[%s]#2p"%(hz_xi),
    "[%s8⑧]#3[%s]"%(hz_ba,hz_jiu),
    "[%s]#3[9⑨]"%(hz_ba),
    "[%scx]#3[%s]"%(hz_xi,hz_jin_jing),
    "[%s斥芹斩析祈折所]#3[%s呼乎砰怦秤抨p]"%(hz_jin_jing,hz_pin_ping), 
    "[%s6⑥]#3[%s舍捨]"%(hz_liu_lu,hz_si_shi),
    "[%s]#3[4④]"%(hz_liu_lu),
    
    ### 以下屏蔽词已做其它处理（见rules）
    # "hk", "tg", "tw", "xi", "zf", "abs", "sex", "tam", "xjp", "anal", "arms", "asmr", "fldf", "ntop", "baidu", "antifa", "tmmsme", "yayeae",
    # "mama", "mimi", "ilibilib", "pilipili", "dilidili", "niconico",
    # "爸爸", "弯弯", "湾湾", "啪啪", "啪#2啪#2啪", "鸡#2鸡", "光#3光", "共#4共", "点点点", "大大大大大", "嘀哩嘀哩", "加速加速",
    # "书记", "想死", "屏蔽", "干妈", "64", "73", "89", "404",
   
    ### 字母+汉字（仅作简单处理）
    "si法", "你ma", "mei药", "媚yao", "lu#2发",  "看#3id", "加#4qq", "diao#3大", "ri#1[我你]", 

    ### 以下词汇屏蔽已失效
    # "神社", "垃圾", "人妻", "改变", "签约", "失望", "控制", "节奏", "赤裸", "天城",
    # "黑手", "集会", "光荣", "虾膜", "成人", "中央", "万岁", "萝莉", "没了", "死了",
    # "71", "1921", "av", "sb", "小学生", "不习惯", "发不出", "风平浪静", "老不死的",
]

# 反屏蔽处理规则字典，键为正则匹配表达式（字符串, pat），值为处理结果（字符串或函数, rep）
rules = {
    ### 连续半角空格处理
    " +" :" ",
    ### 单字/特殊字符
    "(?<![花牡虾海车香])蛤(?![蜊蚧子蜃])":"Ha", "蛤": "Ge",
    "翠": "翆", "尻": "𡱧", "爬": "Pa", "痒": "𤶪", "淫":"Yin", "岿": "巍", "屌": "吊", "党": "Dαng", "奠": "Dian",
    "[àáâãäåÀÁÂÃÄÅāǎ]": "a", "[èéêëÈÉÊËēě]": "e", "[ìíîïÌÍÎÏīǐ]": "i", "[òóõôöÒÓÔÕÖōǒ]": "o", "[ùúûüÙÚÛÜūǔ]": "u", "[ǖǘǚǜü]": "v",
    "⑤": "(5)", "⑥": "(6)", "⑧": "(8)", "⑨": "(9)", "⑩": "(10)", "０": "0", "５": "5", "６": "6", "９": "9", "×": "x",
    ### 英文非常规处理规则
    "(?i)(h ?)(k)": lambda x: x.group(1) + letter[x.group(2)],
    "(?i)(t)( ?w| ?g| ?a ?m)": lambda x: letter[x.group(1)] + x.group(2),
    "(?i)(a)(rm ?s| ?b ?s| ?n ?a ?l| ?n ?t ?i ?f ?a)": lambda x: letter[x.group(1)] + x.group(2),
    "(?i)m ?([ai]) ?(?=m ?\\1)": lambda x: x.group() + "\u0592",
    "(?i)([dp]) ?i ?l ?i ?(?=\\1 ?i ?l ?i)": lambda x: x.group() + "\u0592",
    "(?i)i ?l ?i ?b ?(?=i ?l ?i ?b)": lambda x: x.group() + "\u0592",
    "(?i)n ?i ?c ?o ?(?=n ?i ?c ?o)": lambda x: x.group() + "\u0592",
    "(?i)([.,。，·] ?)(c.?n|c.?o.?m|t ?k)": lambda x: x.group(1) + "\u0592\u0592" + x.group(2),
    "(?i)(a)(.*?j)(.*?p)": lambda x:
        (letter[x.group(1)] + x.group()[1:])
        if measure(x.group(2),7) and measure(x.group(3),7) else x.group(),
    "(?i)(a)(.*?s)(.*?m)(.*?r)": lambda x: #asmr四个字母任意顺序排列均会被屏蔽，这里只考虑常见情况
        (letter[x.group(1)] + x.group()[1:])
        if measure(x.group(2),4) and measure(x.group(3),4) and measure(x.group(4),4) else x.group(),
    "(?i)(f.*?)(l)(.*?d)(.*?f)": lambda x:
        (x.group(1)+letter[x.group(2)]+x.group(3)+x.group(4))
        if measure(x.group(1),7) and measure(x.group(3),7) and measure(x.group(4),7) else x.group(),
    "(?i)(s.*?)(e.*?)(x)": lambda x:
        (x.group(1)+x.group(2)+letter[x.group(3)])
        if measure(x.group(1),3) and measure(x.group(2),3) else x.group(),
    "(?i)(x)(.*?j)(.*?p)": lambda x:
        (letter[x.group(1)]+x.group(2)+x.group(3))
        if measure(x.group(2),5) and measure(x.group(3),5) else x.group(),
    "(?i)(n.*?)(t.*?)(o)(.*p)": lambda x:
        (x.group(1)+x.group(2)+letter[x.group(3)]+x.group(4))
        if measure(x.group(1),4) and measure(x.group(2),2) and measure(x.group(4),2) else x.group(),
    "(?i)r(?=( ?[^ ]){0,5} ?i( ?[^ ]){0,5} ?o( ?[^ ]){0,5} ?t( ?[^ ]){0,5} ?s)": lambda x: letter[x.group()], # r#6i#6o#6t#6s
    "(?i)(y.*?)(a.*?)(y.*?)(e.*?)(a)(.*?e)": lambda x:
        ("".join(x.groups()[:4]) + letter[x.group(5)] + x.group(6))
        if measure(x.group(1),4) and measure(x.group(2),4) and measure(x.group(3),4)
        and measure(x.group(4),4) and measure(x.group(6),4) else x.group(),
    "(?i)(t)(.*?m)(.*?m)(.*?s)(.*?m)(.*?e)": lambda x:
        (letter[x.group(1)]+"".join(x.groups()[1:]))
        if measure(x.group(2),6) and measure(x.group(3),6) and measure(x.group(4),6)
        and measure(x.group(5),6) and measure(x.group(6),6) else x.group(),
    ### 中文/数字非常规处理规则
    "(年|月|天|小 ?时|分 ?钟|分) ?(前)": lambda x: x.group(1)+"\u0592"+x.group(2),
    "([草艹操日])\\W*([你我他她它]|[比笔逼]|时光)": lambda x: x.group(1)+"\u0592"+x.group(2),
    "(点 ?){2}(?=点)": lambda x: x.group()+"\u0592",
    "(大 ?){4}(?=大)": lambda x: x.group()+"\u0592",
    "([啪爸弯湾])(?= ?\\1)": lambda x: x.group(1) + "\u0592",
    "加 ?速 ?(?=加 ?速)": lambda x: x.group() + "\u0592",
    "嘀 ?哩 ?(?=嘀 ?哩)": lambda x: x.group() + "\u0592",
    "鸡.*?(?=鸡)": lambda x: fill(x.group(),3),
    "光.*?(?=光)": lambda x: fill(x.group(),4),
    "共.*?(?=共)": lambda x: fill(x.group(),5),
    "啪.*?(?=啪 ?[^ ]? ?啪)": lambda x: fill(x.group(),3),
    "越(?=( ?[^ ]){0,8} ?共)": "Yue",
    "(想 ?)(死)(?! ?你)": lambda x: x.group(1)+"\u0592"+x.group(2),
    "(书 ?)(记)(?! ?舞)": lambda x: x.group(1)+"\u0592"+x.group(2), # "藤原书记"不是屏蔽词
    "(屏 ?)(蔽)(?! ?词)": lambda x: x.group(1)+"\u0592"+x.group(2),
    "(?<!老)(干 ?)(妈)": lambda x: x.group(1)+"\u0592"+x.group(2),
    "[习習](?=.*?平)": lambda x: "Χi",
    "(?ia)(?<!\\w)(x ?)(i)(?! ?\\w)": lambda x: x.group(1)+"\u0592"+x.group(2),
    "(?ia)(?<!\\w)(z ?)(f)(?! ?\\w)": lambda x: x.group(1)+"\u0592"+x.group(2),
    "(?a)(?<!\\w)(6 ?)(4)(?! ?\\w)": lambda x: x.group(1)+"４",
    "(?a)(?<!\\w)(7 ?)(3)(?! ?\\w)": lambda x: x.group(1)+"３",
    "(?a)(?<!\\w)(8)( ?9)": lambda x: "８"+x.group(2),
    "(?a)(?<!\\w)(4 ?0 ?)(4)(?! ?\\w)": lambda x: x.group(1)+"４",
    "(?i)(六|6|⑥|l ?i ?u)(.*?)(四|肆|4|④|s ?i)": lambda x: (x.group(1)+fill(x.group(2),4)+x.group(3)) if not (x.group(1)=="6" and x.group(3)=="4") else x.group(),
    "(?i)([%s贝呗]|b ?a ?i)(?=.*?([%s]|d ?u))"%(hz_bai,hz_du): lambda x: "Ⲃei" if x.group() in "贝呗" else "Ⲃai",
    "([干日草艹操曰].*?)(视.*?)(频)": lambda x: x.group(1)+fill(x.group(2),2)+x.group(3), # "[干日草艹操曰]#7视#1频"
    "([日草艹曰操].*?)(公.*?)(主)": lambda x: x.group(1)+fill(x.group(2),2)+x.group(3), # "操#3公#1主" "[日草艹曰]#9公#1主"
    "([大小妈姐妹哥弟一二三四五六七八九].*?)([小姐妹哥弟一二三四五六七八九].*?)([在来做进])": lambda x:
        (x.group(1)+fill(x.group(2),5+r_pos(x.group(2),"小姐妹哥弟一二三四五六七八九"))+x.group(3))
        if measure(x.group(1),5) and measure(x.group(2),5+r_pos(x.group(2),"小姐妹哥弟一二三四五六七八九")) else x.group(),
    "(?i)([%sail百].*?)([就上去还点被了射].*?)([来射车有点出被].*)"%(hz_du): lambda x:
        (x.group(1)+fill(x.group(2),5+r_pos(x.group(2),"就上去还点被了射"))+x.group(3))
        if measure(x.group(1),7) and measure(x.group(2),5+r_pos(x.group(2),"就上去还点被了射"))
        and not measure(x.group(3),4) else x.group(),
    "([马就].*?)([想上].*?)([鲁撸噜])": lambda x:
        (fill(x.group(1),6+r_pos(x.group(1),"马就"))+x.group(2)+x.group(3))
        if measure(x.group(1),6+r_pos(x.group(1),"马就")) and measure(x.group(2),6) else x.group(),
    ### 保护型处理规则
    "[习習]": lambda x: x.group()+"\u0592",
}
# <DATA END>

def get_len(string):
    '''获取正则表达式串string的字段宽度'''
    return len(re.sub(r"\[.+?\]","~",string))

def measure(string,length):
    '''判断字符串string中非空格字符数是否小于length'''
    return get_len(string)-string.count(" ")<length

def fill(string,length):
    '''填补字符串string，使其中的非空格字符数等于length'''
    dots="\u0592"*(length-get_len(string)+string.count(" "))
    return string+dots

def r_pos(string,targets):
    '''查找字符串targets中的字符在字符串string中最后一次出现的位置'''
    r_str=string.replace(" ","")[::-1]
    for index,char in enumerate(r_str):
        if char in targets: return len(r_str)-index-1

def substitute(pat,rep,string):
    '''正则替换函数，是re.sub()的一种修改版本'''
    # 目前有个缺点，如果屏蔽字首尾相同或可拆分为更小的重复单元，则可能无法替换干净。
    # 例如对"ABABA"按"ABA"→"ACA"的替换规则，替换结果为"ACABA"而非"ACACA"。
    def get_min_so(so):
        '''递归函数，获取串总长最短的捕获组'''
        new_so=re.search(pat,so.group()[1:])
        return so if new_so is None else get_min_so(new_so)  
    def min_sub(so):
        '''回调函数，获取替换结果'''
        min_so=get_min_so(so)
        min_rep=re.sub(r"\\(\d)",lambda x:min_so.group(int(x.group(1))),rep) if isinstance(rep,str) else rep(min_so)
        return so.group().replace(min_so.group(),min_rep)
    return re.sub(pat,min_sub,string)

def generate_rule(word):
    '''根据屏蔽词word，生成相应的处理规则，添加到字典rules中'''
    # word中，“#”后的数字表示需要间隔多少个字符才不会被屏蔽。
    # 如果word不含“#”，则默认在第一个字符后添加“\u0592”。
    try:
        groups=re.split(r"#[1-9]",word)
        n=len(groups)-1
        if n==0:
            pat = "(?i)" + " ?".join(word)
            rep = lambda x: x.group()[0] + "\u0592" + x.group()[1:]
            rules[pat] = rep
            return
        fills=[int(i) for i in re.findall(r"#([1-9])",word)]
        pat="(?i)" + "".join(["("+groups[i]+".*?)" for i in range(n)]) + "(%s)"%groups[n]
        rep="lambda x: (" + "+".join(["fill(x.group(1),%d)"%(get_len(groups[0])+int(fills[0]))] +
            ["x.group(%d)"%(i+1) for i in range(1,n+1)]) + ") if " + \
            " and ".join(["measure(x.group(%d),%d)"%(i+1,get_len(groups[i])+int(fills[i])) for i in range(n)]) + \
            " else x.group()"
        rules[pat] = eval(rep)
    except Exception as e:
        pass

# 对屏蔽词做处理，并添加到处理规则中
for word in words:
    generate_rule(word)

def deal(string):
    '''对字符串string按字典rules中的规则进行反屏蔽处理'''
    # 外部请调用这个函数。
    string=re.sub(r" +"," ",string) # 合并连续半角空格
    for k, v in rules.items():
        string = substitute(k, v, string)
    return string

def test(string):
    '''打印字符串string的反屏蔽处理结果'''
    print("[处理前]",string)
    print("[处理后]",deal(string))
    
if __name__ == '__main__':
    test("asmr")
    test("花瓣纷扬 我们连呼吸也不禁遗忘")
    test("colorful and free")
    test("Oh baby, can't you see?")
    test("【Melt 马上就要到车站了】")
    test("picopico 东京")
    test("bilibili bilili")
    while True:
        string=input("[处理前] ")
        print("[处理后] "+deal(string))
