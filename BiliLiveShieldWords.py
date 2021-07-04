# coding: utf-8
import re

# <DATA BEGIN>
# 拼音对应的常用汉字
hz_xi="夕兮吸汐西希析昔茜奚唏栖息悉惜淅犀晰腊锡皙溪嘻嬉窸稀蹊蟋曦习席袭洗喜戏系细隙"
hz_jin_jing="巾今斤金矜津筋禁仅尽紧谨锦劲进近浸烬晋京径经荆惊晶睛鲸井景净竞竟靓敬静境镜颈精"
hz_pin_ping="拼贫频品聘乒平评凭坪屏瓶苹萍"
hz_ba="八巴吧疤笆拔跋把靶伯坝爸罢"
hz_jiu="纠究啾揪九久韭酒旧疚救就舅鹫"
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
    "t":"τ", "T":"Т",
    "x":"χ", "X":"Χ",
}

# 屏蔽词列表
words =  [ 
    ### 一般屏蔽词（易变动）
    "即位", "修正", "领导", "红通", "腐败", "起义", "特权", "警察", "军队", "政府",
    "与正", "在任", "抗争", "革命", "冷战", "小熊", "汪洋", "包子", "孢子", "提案",
    "颠覆", "圣战", "吼哇", "卫兵", "国歌", "和谐", "河蟹", "八路", "家明", "游行", 
    "郭嘉", "果加", "菓加", "天安", "安门", "审查", "屏蔽", "番号",
    "杀死", "囚禁", "施虐", "虐待", "捆绑", "割腕", "匕首", "生事", "疫情", "新冠", 
    "大麻", "包粉",
    "色戒", "湿了", "射了", "硬了", "中出", "高潮", "调教", "被透", "走光", "诱惑",
    "喘气", "喘息", "呻吟", "处女", "处男", "绅士", "抖m" , "h漫" , "性癖", "无码",
    "胖次", "欧派", "罩杯", "大胸", "嘿咻", "下女", "内内", "吹气", "掏耳", "助眠",
    "肥猪", "下贱", "死吧", "你妈", "死妈", "去死", "月半", "己吧", "送妈", "死法",
    "si法",
    "台湾", "香港", "日吹", "精美", "精日", "弯弯", "油管", "推特", "微博", "新浪",
    "抖音", "优酷", "鸣人", "动森", "梯子",
    "皇帝", "庙堂", "磕头", "传教", "宗教", "还愿", "安乐", "包养", "一哥",
    "赌博", "扑克", "彩票", "发票", "博彩", "菠菜", "硫酸", "甲烷", "煤气",
    "四六", "五四", "七一", "七五", "九八",
    "爸爸", "即为", "试看", "豪迈", "耳语", "迷途", "触摸", "初心", "慎重", "三尺",
    "许愿", "代打", "躺平", "熊学", "伐龙", "要素",
    "ロリ", "はま", "ハマ", "しな", "シナ", "くま", "死ね", "映画", 

    "hw", "gc", "zf", "kui", "lsp", "usl", "xxd", "drug", "knee", "kuma", "loli", "sina", 
    "bajiu", "luoli", "sager", "shina", "hentai", "reddit", "signal", "tiktok", "youtube",
    "revolution", "ilibilib", "pilipili", "dilidili", 
    "64", "71", "73", "404", "535", "586", "604", "809", "881", "918", "1921", "1926", "1953", "1979", "1989", "g7", "g20", "j8",
    "不想活", "自由门", "咖啡因", "死灵魂", "白衬衫", "生理期", "空气炮", "黑历史", "就去泡", "一本道", "被传染", "网易云", "爱奇艺",
    "纪念日", "为自由", "莉莉安", "李医生", "右大人", "绞肉机", "不唱歌", "女菩萨", "发不出", "老鼠台", "缘之空", "一起死",
    "四一二", "五三五", "八一七", "九一八", "九九六", "一九二六", "一九五三",
    "自由之门", "继续前进", "并肩同行", "焕然一新", "奥斯曼人", "二氧化碳", "阿里巴巴", "恐怖分子", "恐怖份子",
    "身经百战", "黑框眼镜", "谈笑风生", "无可奉告", "活不下去", "飘飘欲仙", "动物之森", "分割人生", "坟头蹦迪", "嘀哩嘀哩",
    "你是你我是我",

    ### 以下屏蔽词已做其它处理
    # "hk", "tg", "tw", "abs", "sex", "tam", "xjp", "anal", "arms", "asmr", 
    # "fldf", "fuck", "mama", "baidu", "bitch", "tmmsme", "yayeae",   
    # "书记", "想死", "许愿", "啪啪", "啪啪啪", "点点点", #其余部分见rules 

    ### 以下词汇屏蔽已失效
    # "神社", "垃圾", "人妻", "改变", "签约", "失望", "控制", "节奏", "赤裸", "天城",
    # "黑手", "集会", "光荣", "虾膜", "成人", "中央", "万岁", "萝莉",
    # "av", "sb", "小学生", "不习惯", "毕业歌", "风平浪静", "老不死的",

    ### 字符间隔相关
    "v#4b#3o", "道#3上#3飞", "名#3字#3看", "我#3是#3处", "下#3面#3好", "看#3i#1d", "直#3播#3[日草操]", "射#4身#1上", "天#4安#4门",
    "手#5指#5插", "文#6古#6花", "看#6地#6方", "不#6钱#6啊", "那#1个#4奶#1奶", "羊#1羊#4结#1婚", "清#6透#6世#6界", "w#4e#4i#4b#4o", "一#6个#6人#6寂#6寞",
    "[贫小平]#1乳", "色#1[逼b]", "[傻沙煞撒]#1[逼比笔]", "[插吸]#1[你他她它]", "称#1[王皇帝]", "[.。·]#1[cf]", "点#1[人1cfl]", 
    "8#29", "巨#2乳", "[草操]#3b", "被#3[日草操]", "少女#3[下自]", "[做作坐座]#3爱", "去#3搜", "下#3注", "百#3d", "光#3光",
    "六#4四", "八#4九", "[看好]#4胸", "车#4震", "小#4平", "再#4任", "明#4泽", "援#4交", "后#4入", "天#4门", "流#4世", "留#5水", "性#5爱",
    
    ### 拼音组合相关
    "[%s]#1[%s]"%(hz_wei_1,hz_ni),
    "[%s]#1尼"%(hz_wei_2),
    "[%s]#1都"%(hz_bai),
    "[%scx]#2[%s]"%(hz_xi,hz_pin_ping),
    "[%s]#2p"%(hz_xi),
    "[%s8⑧]#3[%s]"%(hz_ba,hz_jiu),
    "[%s]#3[9⑨]"%(hz_ba),
    "[%scx]#3[%s呼]"%(hz_xi,hz_jin_jing),
    "[%s]#3[%s呼乎p]"%(hz_jin_jing,hz_pin_ping), 
    "[%s6⑥]#3[%s舍捨]"%(hz_liu_lu,hz_si_shi),
    "[%s]#3[4④]"%(hz_liu_lu),
]

# 反屏蔽处理规则字典，键为正则匹配表达式（字符串, pat），值为处理结果（字符串或函数, rep）
rules = {
    ### 单字/特殊字符
    "翠": "Cui", "尻": "Kao", "爬": "Pa", "痒": "Yang", "淫":"Yin", "岿": "巍", "屌": "吊", "蛤": "Ha",
    "[àáâãäåÀÁÂÃÄÅāǎ]": "a", "[èéêëÈÉÊËēě]": "e", "[ìíîïÌÍÎÏīǐ]": "i", "[òóõôöÒÓÔÕÖōǒ]": "o", "[ùúûüÙÚÛÜūǔ]": "u", "[ǖǘǚǜü]": "v",
    "⑤": "(5)", "⑥": "(6)", "⑧": "(8)", "⑨": "(9)", "⑩": "(10)", "０": "0", "５": "5", "６": "6", "９": "9", "×": "x",
    ### 英文非常规处理规则
    "(?i)(h ?)(k)": lambda x: x.group(1) + letter[x.group(2)],
    "(?i)(t)( ?w| ?g| ?a ?m)": lambda x: letter[x.group(1)] + x.group(2),
    "(?i)(a)(rm ?s| ?b ?s| ?n ?a ?l)": lambda x: letter[x.group(1)] + x.group(2),
    "(?i)(m ?a ?m ?)(a)": lambda x: x.group(1) + letter[x.group(2)],
    "(?i)(a)(.*?s)(.*?m)(.*?r)": lambda x: #asmr四个字母任意顺序排列均会被屏蔽，这里只考虑常见情况
        (letter[x.group(1)] + x.group()[1:])
        if measure(x.group(2),4) and measure(x.group(3),4) and measure(x.group(4),4) else x.group(),
    "(?i)([.,。，·] ?)(c.?n|c.?o.?m)": lambda x: x.group(1) + "\u0592\u0592" + x.group(2),
    "(?i)fuck": "f**k",
    "(?i)bitch": "b***h",
    "(?i)bai(.*?)du": lambda x: "Bai"+x.group(1)+"Ꭰu",
    "(?i)(f.*?)(l)(.*?d)(.*?f)": lambda x:
        (x.group(1)+letter[x.group(2)]+x.group(3)+x.group(4))
        if measure(x.group(1),7) and measure(x.group(3),7) and measure(x.group(4),7) else x.group(),
    "(?i)(s.*?)(e.*?)(x)": lambda x:
        (x.group(1)+x.group(2)+letter[x.group(3)])
        if measure(x.group(1),3) and measure(x.group(2),3) else x.group(),
    "(?i)(x)(.*?j)(.*?p)": lambda x:
        (letter[x.group(1)]+x.group(2)+x.group(3))
        if measure(x.group(2),5) and measure(x.group(3),5) else x.group(),
    "(?i)(y.*?)(a.*?)(y.*?)(e.*?)(a)(.*?e)": lambda x:
        ("".join(x.groups()[:4]) + letter[x.group(5)] + x.group(6))
        if measure(x.group(1),4) and measure(x.group(2),4) and measure(x.group(3),4)
        and measure(x.group(4),4) and measure(x.group(6),4) else x.group(),
    "(?i)(t)(.*?m)(.*?m)(.*?s)(.*?m)(.*?e)": lambda x:
        (letter[x.group(1)]+"".join(x.groups()[1:]))
        if measure(x.group(2),6) and measure(x.group(3),6) and measure(x.group(4),6)
        and measure(x.group(5),6) and measure(x.group(6),6) else x.group(),
    ### 中文/数字非常规处理规则
    "(年|月|天|小时|分) ?(前)": lambda x: x.group(1)+"\u0592"+x.group(2),
    "([草操日])\\W*([你我他她它]|[比笔逼]|时光)": lambda x: x.group(1)+"\u0592"+x.group(2),
    "(点 ?点 ?)(点)": lambda x: x.group(1)+"\u0592"+x.group(2)+"\u0592",
    "想 ?死(?! ?你)": "想\u0592死",
    "书 ?记(?! ?舞)": "书\u0592记", # "藤原书记"不是屏蔽词，但是不考虑这种情况
    "(?i)(六|6|⑥|l ?i ?u)(.*?)(四|肆|4|④|s ?i)": lambda x: (x.group(1)+fill(x.group(2),4)+x.group(3)) if not (x.group(1)=="6" and x.group(3)=="4") else x.group(),
    "([干湿].*?)(视.*?)(频)": lambda x: x.group(1)+fill(x.group(2),3)+x.group(3), # "湿#2视#2频"与"干#7视#1频"统一处理，大概率还有其他"X+视频"的情况
    "(?i)([%s贝]|b ?a ?i)(.*?)([%s]|d ?u)"%(hz_bai,hz_du): lambda x: x.group(1) + x.group(2) + "Ꭰu", # 这里的字符Ꭰ是/u13A0。本条规则不一定处理得干净
    "(?i)([大小一姐妹哥弟].*?)([一小姐妹哥弟].*?)([在来做])": lambda x:
        (x.group(1)+fill(x.group(2),5+r_pos(x.group(2),"一小姐妹哥弟"))+x.group(3))
        if measure(x.group(1),5) and measure(x.group(2),5+r_pos(x.group(2),"一小姐妹哥弟")) else x.group(),
    "(?i)([%sail].*?)([就上去还点].*?)([来射车有点].*)"%(hz_du): lambda x:
        (x.group(1)+fill(x.group(2),5+r_pos(x.group(2),"就上去还点"))+x.group(3))
        if measure(x.group(1),7) and measure(x.group(2),5+r_pos(x.group(2),"就上去还点"))
        and not measure(x.group(3),4) else x.group(),
    # 下列三条规则已被简化
    #"(.? ?7 ?)(3 ?.?)": lambda x: (x.group(1)+"\u0592"+x.group(2)) if re.match("(?a)^\\W? ?7 ?$",x.group(1)) and re.match("(?a)^3 ?\\W?$",x.group(2)) else x.group(),
    #"(.? ?6 ?)(4 ?.?)": lambda x: (x.group(1)+"\u0592"+x.group(2)) if re.match("(?a)^\\W? ?6 ?$",x.group(1)) and re.match("(?a)^4 ?\\W?$",x.group(2)) else x.group(),
    #"(.? ?8 ?)(9)": lambda x: (x.group(1)+"\u0592"*2+x.group(2)) if re.match("(?a)^\\W? ?8 ?$",x.group(1)) else x.group(),
    ### 保护型处理规则
    "啪":"帕",
    "习": "习\u0592",
}
# <DATA END>

def get_len(string):
    # 获取字符串string的长度
    # 在len()的基础上，[]及其中的内容统一视为一个字符。
    return len(re.sub(r"\[.+?\]","~",string))

def measure(string,length):
    # 判断字符串string中非空格字符数是否小于length
    return get_len(string)-string.count(" ")<length

def fill(string,length):
    # 填补字符串string，使其中的非空格字符数等于length
    dots="\u0592"*(length-get_len(string)+string.count(" "))
    return string+dots

def r_pos(string,targets):
    # 查找字符串targets中的字符在字符串string中最后一次出现的位置
    r_str=string.replace(" ","")[::-1]
    for index,char in enumerate(r_str):
        if char in targets: return len(r_str)-index-1

def substitute(pat,rep,string):
    # 正则替换函数（仅基于本代码的逻辑对re.sub()进行改进）
    # 目前有个缺点，如果屏蔽字首尾部分相同，则可能无法替换干净。例如对"ABABA"按"ABA"→"ACA"的替换规则，
    # 替换结果为"ACABA"而非"ACACA"。目前B站这类屏蔽字比较少，如535，爸爸，啪啪 等。
    def get_min_so(so):
        # 递归函数，获取串总长最短的捕获组
        new_so=re.search(pat,so.group()[1:])
        return so if new_so is None else get_min_so(new_so)  
    def min_sub(so):
        # 回调函数，获取替换结果
        min_so=get_min_so(so)
        min_rep=rep if isinstance(rep,str) else rep(min_so)
        return so.group().replace(min_so.group(),min_rep)
    return re.sub(pat,min_sub,string)

def generate_rule(word):
    # 根据屏蔽词word，生成相应的处理规则
    # word中，“#”后的数字表示需要间隔多少个字符才不会被屏蔽
    # 如果word不含“#”，则默认在第一个字符后添加“\u0592”(看起来像小的∴)
    try:
        groups=re.split(r"#[1-9]",word)
        n=len(groups)-1
        if n==0:
            pat = "(?i)" + " ?".join(word)
            rep = word[0] + "\u0592" + word[1:]
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
    # 对字符串string进行反屏蔽处理
    # 外部请调用这个函数
    string=re.sub(r" +"," ",string) # 合并连续半角空格
    for k, v in rules.items():
        string = substitute(k, v, string)
    return string

def test(string):
    # 打印字符串string的反屏蔽处理效果
    print("[处理前]",string)
    print("[处理后]",deal(string))
    
if __name__ == '__main__':
    test("asmr")
    test("花瓣纷扬 我们连呼吸也不禁遗忘")
    test("colorful and free")
    test("Oh baby, can't you see?")
    test("【Melt 马上就要到车站了】")
    test("picopico 东京")
    test("bilibili bilili")             #这句处理效果不好，有待改进
    while True:
        string=input("[处理前] ")
        print("[处理后] "+deal(string))
