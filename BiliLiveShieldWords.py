# coding: utf-8
# <DATA BEGIN>
import re
# 拼音对应的常用汉字
hz_xi="夕兮吸汐西希析昔茜奚唏栖息悉惜淅犀晰腊锡皙溪嘻嬉窸稀蹊蟋曦习席袭洗喜戏系细隙"
hz_jin_jing="巾今斤金矜津筋禁仅尽紧谨锦劲进近浸烬晋京径经荆惊晶睛鲸井景净竞竟靓敬静境镜颈精浄"
hz_pin_ping="拼贫频品聘乒平评凭坪屏瓶苹萍"
hz_ba="八巴扒叭坝把吧芭爸拔疤笆粑耙罢捌跋靶魃霸"
hz_jiu="九久旧纠臼究鸠玖灸咎疚韭赳柩酒阄救厩就揪啾舅鹫"
hz_jiu_1="九久纠究鸠玖灸韭赳阄揪啾"
hz_bai="白百伯佰拜柏掰" # 排除：败摆
hz_du_1="度渡镀肚杜堵睹赌读渎犊椟独毒嘟督笃妒" # 排除：竺都
hz_du_2="度渡镀肚杜堵睹独毒都"
hz_liu_lu="六刘柳浏流留琉硫碌溜馏遛榴瘤卢庐芦陆卤虏炉录鸬赂鹿颅绿鲁禄鲈路噜撸辘戮橹璐鹭露" # 重复：六碌
hz_si_shi="四司丝死寺似私祀伺饲驷食思斯肆嗣厮撕嘶十尸士氏什示矢石史市失仕世式师时识始饰视鸤虱实驶事势使侍诗试施恃柿是蚀拭适室狮拾屎峙舐轼逝硕匙释湿谥弑誓嗜噬螫" # 重复：似食
#hz_wei="卫为韦未危伪伟围纬尾违苇位委味畏威娓维惟唯帷萎偎谓尉喂猥痿微蔚薇魏巍"
hz_wei_1="卫未位味畏维萎谓尉喂蔚"
hz_wei_2="为伟围维唯魏"
hz_wei_3="为未伪纬苇委味畏维惟萎谓尉蔚"
hz_ni="尼拟泥妮昵逆倪匿腻溺霓" # 排除：你呢
hz_ma="马妈吗码玛蚂犸麻嘛骂蟆抹"
#hz_bo="卜伯驳拨波泊勃柏玻剥饽钵铂菠啵脖舶博渤搏箔播薄簸"
hz_fa="乏发伐法罚阀砝"
hz_lun="仑伦论抡沦纶囵轮"
hz_gong="公工功供宫攻恭弓躬龚蚣拱巩汞共贡"
# 常见标点符号
p_marks=".,!?+*/#%&^$`(){}…@~\"\'\\;:<>|=·。，！？；：￥“”‘’—（）【】「」\-\[\]" # 用于正则表达式的[]内
f1="(?<![\s\d\u4E00-\u9FA5])"
f2="(?![\s\d\u4E00-\u9FA5])"
sp="\U000E0020" #旧版机制分隔符，由U+0592改为U+E0020

add_space = lambda x: x.group()+" "
insert_space = lambda x: x.group()[0]+" "+x.group()[1:]

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
    ### 一般屏蔽词（易变动）   1.0版本，填充字符即可解决
    "即位", "在任", "下台", "倒台", "候选", "选举", "上位", "选拔",
    "总理", "总统", "纪委", "政府", "国会", "议会", "特首",
    "修正", "特权", "政策", "提案", "出访", "审查", 
    "天安", "安门", "赤字", "民众", "中共", "国歌", "金砖", "康米", "人大",
    "生事", "闹事", "闹剧", "游行", "颠覆", "煽动", "乱暴", "暴乱", "动乱", "暴动",
    "分裂", "抗议", "罢工", "冷战", "圣战", "革命", "起义", "抗争", "厌世", "人肉",
    "国难", "歧视", "政变",
    "军队", "部队", "萨德", "履带", "卫兵", "警察", "八路", "番号", "军人", "兵团",
    "囚禁", "施虐", "虐待", "捆绑", "割腕", "剥削", "匕首", "鞭尸", "自残", "灌肠",
    "中出", "高潮", "被透", "走光", "诱惑", "双飞", "梆硬", "女同", "男同", "工口",
    "喘气", "喘息", "娇喘", "呻吟", "处男", "绅士", "性癖", "黄游", "裸镜", "半裸",
    "胖次", "罩杯", "嘿咻", "吹气", "掏耳", "助眠", "耳语", "蛋大", "脏病", "开冲",
    "重口", "勃起", "出轨", "黑化", "叫鸡", "痴汉", "进裙", "鸡儿", "爽爆", "无修",
    "肉便", "玩逼", "看腿", "跳蛋", "御姐", "迷途", "无码", "果体", "裙底", "换妻",
    "脱光", "丝袜", "漏点", "媚药", "很太", "热舞", "牛子", "给口", "发情", "交配",
    "膝下",
    "肥猪", "下贱", "你妈", "月半", "送妈", "嘴臭", "拉屎", "撤硕", "低俗", "憨批",
    "刁大", "禽兽", "畜生", "吃屎", "智障", "小丑", "杂种", "该死",
    "美国", "米国", "台湾", "香港", "澳门", "日吹", "韩国",
    "油管", "推特", "新浪", "抖音", "优酷", "淘宝", "虎牙", "斗鱼", "战旗",
    "皇帝", "皇宫", "庙堂", "磕头", "安乐", "包养", "清真", "还愿", "黑魂", "如龙",
    "赌博", "扑克", "彩票", "发票", "博彩", "菠菜", "借贷", "贷款", "传销", "贿赂",
    "新冠", "防疫", "疫情", "硫酸", "甲烷", "煤气", "氨水", "氨气", "包粉", "白粉",
    "四六", "五四", "七一", "七五", "九八",
    "即为", "试看", "豪迈", "触摸", "初心", "慎重", "三尺", "鲍鱼", "河蟹", "洗地",
    "代打", "躺平", "要素", "上街", "读错", "下乡", "闪灵", "集资", "奥运", "种台",
    "盗取", "茅台", "痔疮", "利益", "费钱", "不办", "变质",
    "百年", "鸡脖", "庆典", "广场", "秃鹰", "细腻", "泼墨", "发酵", "快排", "终共",
    "一哥", "动森", "鸣人", "映画", "老母", "青蛙", "口误", "连睡", "内设", "平总",
    "黑幕", "猎奇", "冲塔", "逆行", "太安", "弹舌", "螳臂", "挡车", "全套", "自重", 
    "牛芝", "比心", "横幅", "饭友", "尚气", "赛艇", "催人", "催吐", "月经", "大法",
    "小熊", "吼哇", "吼啊", "之那", "膜导", "长者", "長者", "郭嘉", "果加", "菓加",
    "与正", "蒂亚", "稻上", "飞草", "熊学", "伐龙", "家明", "马云", "唐可", "泽东",
    "小瓶", "晓平", "超良", "虫也", "虫合", "换声", "代开", "国动", "气弹", "网球",
    "追思", "佐助", "腊肉", "抑郁", "发漂", "咧嘴", "莉娅", "丽娅", "汪洋", "楚晨",
    "冈本", "藏人", "妇女", "太君", "入赘", "度良", "哄睡", "嗑药", "三胖", "多震",
    "造f" , "抖m" , "妹y" , "h漫" , "h肉" , 
    "ロリ", "はま", "ハマ", "しな", "シナ", "くま", "エロ",

    "gc", "hw", "hk", "qd", "rh", "zf",
    "abs", "cjp", "cnm", "gay", "ghs", "kui", "lsp", "nmb", "nmd", "ntr", "ply", "roc", "scp", "soe", "tmd", "usl", "wic", "wjb", "xxd",
    "anal", "arms", "boki", "dang", "drug", "frog", "fuck", "knee", "kuma", "liya", "loli", "nmsl", "rori", "sina", "tank", "yuan",
    "anmen", "baidu", "bajiu", "bitch", "ching", "elder", "luoli", "obama", "ruler", "sager", "secom", "shina",
    "antifa", "father", "hentai", "huanqi", "panzer", "reddit", "signal", "tiktok", "twitch",
    "excited", "youtube", "exciting", "onedrive", "zhongguo", "revolution", "neverforget",
    "64", "73", "404", "535", "586", "604", "809", "817", "881", "918", "1926", "1953", "1979", "1989", "j8", "g20", "r19", "5km", "100kg",
    "不想活", "自由门", "咖啡因", "死灵魂", "白衬衫", "生理期", "空气炮", "黑历史", "一本道", "养老金",
    "被传染", "网易云", "爱奇艺", "支付宝", "劈腿男", "缘之空", "一起死", "稻田上", "安眠药", "接班人", 
    "纪念日", "为自由", "李医生", "右大人", "绞肉机", "不唱歌", "女菩萨", "毕业歌", "老鼠台", "网上搜",
    "梦大师", "脱衣服", "我要射", "来一发", "小柜子", "奇酷比", "比基尼", "【萝莉", "就这？", "逃生2" ,
    "性骚扰", "妖妖灵", "蛋炒饭", "异教徒", "跑得快", "牺牲品", "劳动法", "斯大林", "未成年", "小红书",
    "麻酥酥", "兼职加", "水好多", "滚出去", "黄段子", "给我滚", "没衣服", "玻璃心", "黎明杀", "不过审",
    "色蝴蝶", "色天使", "振动棒", "震动棒", "战车道", "臂当车", "小黄油", "小黄书", "炸学校", "你全家",
    "小幸运", "换平台", "顶不住", "顶得住", "按回车", "找爸爸", "欧金金", "拼多多", "熊出没", "上床了",
    "有神明", "一直播", "看名字", "报警了", "金小姐", "被墙了", "大三元", "甜蜜蜜", "不作为", "再教育",
    "求救信", "这垃圾", "咀嚼音", "被消灭", "鲨了你", "家暴男", "胸好大", "死很多", "一夜情",
    "开黄腔", "空心菜",
    "四一二", "五三五", "八一七", "九一八", "九九六", "一九二六", "一九五三", 
    "自由之门", "继续前进", "并肩同行", "焕然一新", "二氧化碳", "阿里巴巴", "恐怖分子", "恐怖份子", "田所浩二", "蒙古上单",
    "身经百战", "黑框眼镜", "谈笑风生", "无可奉告", "微小的事", "活不下去", "飘飘欲仙", "分割人生", "坟头蹦迪", "b站员工" ,
    "我是黄金", "没有敌人", "少女之心", "奥斯曼人", "孩子的鞋", "花花公子", "不想回忆", "最大限度", "那个男人", "那位大人", 
    "脑子瓦特", "恐怖漫画", "乡关何处", "有容乃大", "是全裸的", "最后一课", "狼吞虎咽", "时间机器", "疲劳驾驶", "区别对待",
    "的混合物", "波涛汹涌", "报复社会", "官方签约", "我还活着", "贤者模式", "侃侃而谈", "约德尔人", "社会主义", "要开会了",
    "健身教练", "为所欲为", "特别待遇", "人生经验", "银河联邦", "活塞运动", "再来一次",
    "黑暗之魂", "求生之路", "上古卷轴", "侠盗飞车", "尸体派对", "动物之森",
    "31年", "80年代", "110吗", "1月23", "7月1日", "7月5日", "7月13", "8月17日", "12月28", 
    "命运共同体", "这就是中国", "克里斯托弗", "你是你我是我", "南无阿弥陀佛", "热爱105度", #汉字格式的日期也会被屏蔽，这里没写出来
    
    # 1.0保护性屏蔽
    "视频", "公主", "超市",

    ### 字符间隔相关
    "奥#1数#1[魔默]", "一#1口#1[气吃喝]", "收#1[妹弟女]#1[妹弟儿]", "[有搞]#1黄#1色", "下#1面#2[松紧]", "回#1来#3谢", "观#1众#3v", "还#1没#3封", "[姐妹]#1[姐妹]#5[逼b]", "弟#1弟#6大", 
    "射#2出#1来", "湿#2视#2频", "[01]#2找#2[01]",
    "[逼b]#3看#1吗", "搜#3这#1个", "投#3比#1赛", "看#3头#1像", "看#3昵#1称", "看#3内#1裤", "戴#3绿#1帽", "吃#3菊#1花", "摸#3屁#1股", "h#3动#1[画漫]", "6#3月#24",
    "同#3性#3恋", "道#3上#3飞", "名#3字#3看", "我#3是#3处", "下#3面#3好", "习#3d#3d", "看#3洗#3澡", "少#3女#3[下自]", "直#3播#3[日草艹操曰]",
    "射#4身#1上", "童#4收#1养", "买#4烟#1花", "[删关]#4评#1论", "改#4中#1国", "花#4全#1裸", "天#4安#4门", "萝#4莉#4控", "正#4太#4控", "加#4速#4器", "习#4大#4大", 
    "[你尼]#4[妈马吗码蚂玛犸嘛母m家]#4[币比逼必猪狗b]", "[大小妈姐妹哥弟一二三四五六七八九]#4[小姐妹哥弟一二三四五六七八九]#5[在来做进]",
    "手#5指#5插", "徐#5上#5爽", "许#5艾#5莉", "谢#5日#5双", "下#5面#5痒", "崔#5塔#5娜", "包#5含#5雪", "露#5水#5露",
    "[马周]#5上#5[文梦琴]", "[鲁撸露]#5一#5发", "[徐许]#5[上玩日]#5[碧双霜雪]", "[马就]#5[想上]#5[鲁撸噜门们]", "日#5[和河]#5[吗马码玛蚂犸]",
    "[%sail百败掰摆柏伯]#6[就上去还点被了射让]#5[来射车有点出被入抽]"%(hz_du_1), "[日草艹操干曰死烧解透跳杀]#6[你尼我他她它]#5[妈马吗码蚂玛犸嘛母m家]",
    "文#6古#6花", "看#6地#6方", "不#6钱#6[啊3]", "[谢x]#6s#6w",
    "找#1工#1作#3加", "准#1备#3纸#1巾", "都#1是#3衣#1服", "那#1个#4奶#1奶", "羊#1羊#4结#1婚", "学#1生#4学#1生", "妈#1妈#6唱#1歌", "不#1论#6生#1死", "[姐妹哥]#1[姐妹哥]#6大#1腿",
    "[01]#2还#1是#2[01]", "你#3画#3我#3猜", "闭#3关#3锁#3国", "不#3穿#3衣#3服", "清#6透#6世#6界", "一#6个#6人#6寂#6寞", "不#1要#6这#1种#1事#1情",
    "[.]#6c#6c", "[.]#1g#1a", "a#6j#6p", "s#2e#2x", "t#6l#6y", "v#4b#3o", "v#2p#2n", "x#4j#4p", "x#6y#6z", "a#3s#3m#3r", "f#6l#6d#6f", "n#2t#1o#1p", "r#64#60#63",
    "n#2t#2t#1o#1p", "r#6i#6o#6t#6s", "w#4e#4i#4b#4o", "t#6m#6m#6s#6m#6e", "y#4a#4y#4e#4a#4e", "7#1[.]#15", "1#1[.]#12#13", "9#6m#6k", "1#32#33#34#35#36#37#38#39#30",
    
    "吉#1[尔儿]", "野#1[爹妈]", "射#1[爆爽]", "暴#1[饮食]", "就#1[职職]", "腐#1[败敗]", "称#1[王皇帝]", "微#1[博搏勃]", "奶#1[头汁水]", "想#1[日草艹曰射]",
    "涩#1[气批片p]", "精#1[美日湛子]", "乳#1[头首量水摇沟]", "魂#1[一二三123]", "大#1[麻吊弔胸波奶胃]", "点#1[人1cfl]", "死#1[吧妈法ね]", "色#1[图情皮批逼戒狼b]",
    "[逼b]#1里", "[批阴]#1毛", "[吞吃]#1精", "[左右]#1倾", "[狂猛]#1吃", "[愚暴]#1民", "[红紅]#1[魔通]", 
    "[两二2]#1会", "[玩双晕]#1奶", "[处下熟]#1女", "[调传宗]#1教", "[鸡己几寄性]#1[吧巴八8⑧]", "[湿射硬]#1了", "[欧猫毛]#1派", "[人我给]#1日", "[色肉性]#1欲",
    "[兄弟妹]#1控", "[贫小平双]#1乳", "[条包孢窑梯秃矮]#1子", "[杀去爽干操草爹妈饿]#1死", "[插吸]#1[你他她它]", "[.。·]#1[cf]",
    "网#2恋", "巨#2乳", "自#2尽", "涩#2情", "逼#2真", "翻#2墙", "蓝#2灯", "渣#2男", "人#2权", "[逼b]#2[黑毛]", "黑#2[逼b]", "[傻沙煞撒]#2[逼比笔]",
    "支#3那", "去#3搜", "百#3d", "共#3产", "毛#3东", "手#3银", "涩#3图", "肉#3棒", "邪#3教", "果#3聊", "裸#3体", "粉#3奶", "内#3射", "子#3宫", "排#3卵", "艾#3薇",
    "自#3[杀殺慰]", "鸡#3[巴八8⑧]", "[涩色]#3网", "被#3[日草艹操曰]", "[习習吊弔]#3大", "[草艹操]#3b", "[下压]#3注", "[黄色h]#3片", "[做作坐座]#3[爱暖]", "[加+]#3[微薇v]", 
    "六#4四", "八#4九", "车#4震", "援#4交", "后#4入", "流#4世", "主#4席", "黄#4网", "赤#4毒", "近#4评", "孤#4儿", "倒#4车", "[阴陰]#4道", 
    "明#4[泽z]", "近#4苹", "[小进]#4平", "[连再]#4任", "[看好]#4胸", "吃#4[比逼币笔]", "[日草艹操干曰吃]#4[姐妹奶姨吊弔]", 
    "留#5水", "性#5爱", "威#5雄",
    "罗#6莉", "宽#6衣", "彭#6s", "[彭澎p]#6帅", "萝#6[利俐]", "[逼b]#6紧", "[习習]#6[近进]", "幼#8[比逼b]",
    
    ### 拼音/部首组合相关
    "[%s]#1[一1]#1下"%(hz_du_2),
    "[%s]#3大#1大"%(hz_xi),
    "[%s]#3没#1了"%(hz_ma),
    "[%s摆败干]#3[一1]#4下"%(hz_bai), # 顺带处理"干#3一#3下"
    "[两量凉梁良粮粱]#4[加家架假甲嫁佳贾驾茄夹+]#4[和河何呵喝核合盒贺禾荷]", #待补充
    "[裸棵菓粿踝]#1聊",
    "[%s]#1[%s]"%(hz_wei_1,hz_ni),
    "[%s]#1尼"%(hz_wei_2),
    "[%s]#3博"%(hz_wei_3),
    "[%s]#1[%s读赌]"%(hz_bai,hz_du_2),
    "百#3[渡镀d]", "白#3[度渡镀]", # "百度",
    "[%s伪]#3娘"%(hz_du_1),
    "[形型刑邢行]#1[%s]"%(hz_pin_ping),
    "[%scx]#2[%s呼砰怦秤抨]"%(hz_xi,hz_pin_ping),
    "[%s]#2p"%(hz_xi),
    "[%s8⑧]#3[%s]"%(hz_ba,hz_jiu),
    "[%s]#3[9⑨]"%(hz_ba),
    "[%scx]#3[%s青蜻箐]"%(hz_xi,hz_jin_jing),
    "[%s青蜻箐斥芹斩析祈折所]#3[%s呼乎砰怦秤抨p]"%(hz_jin_jing,hz_pin_ping), 
    "[%s6⑥]#3[%s舍捨]"%(hz_liu_lu,hz_si_shi),
    "[%s]#3[4④]"%(hz_liu_lu),
    "x#3[%s]"%(hz_jiu_1),
    "康#6[买卖麦脉埋迈霾]",
    "[%s洪哄烘]#17"%(hz_gong),
    
    ### 以下屏蔽词已做其它处理（见rules）
    # "tw", "xi", "tam", "isis", "mama", "mimi", "ilibilib", "pilipili", "dilidili", "niconico", "89",
    # "弯弯", "绿绿", "湾湾", "内内", "色色", "啪啪", "啪#2啪#2啪", "鸡#2鸡", "光#3光", "共#4共", "点点点", "大大大大大", "嘀哩嘀哩", "加速加速",
    # "书记", "想死", "干妈",
   
    ### 字母+汉字（仅作简单处理）
    "si法", "你ma", "mei药", "媚yao", "吃shi", "lu#2发",  "看#3id", "加#4qq", "[微薇]#4bo", "dio#3[大小]", "diao#3[大小]", "ri#1[我你]", "d#3u#3娘",

    ### 以下词汇屏蔽已失效
    # "领袖", "领导", "大会", "会议", "疫情", "和谐", "许愿", "退钱", "厕所", "巨人", "人妻", "伞兵", "屏蔽",
    # "神社", "改变", "签约", "失望", "控制", "节奏", "赤裸", "天城", "成都", "爸爸", "没封", "电竞",
    # "黑手", "集会", "光荣", "虾膜", "成人", "中央", "万岁", "萝莉", "没了", "死了",
    # "痒", "爬", "奠", "6年", "71", "1921", "av", "g7", "ma", "sb", "tg", 
    # "小学生", "不习惯", "发不出", "就去泡", "莉莉安", "风平浪静", "老不死的",
]

# 反屏蔽处理规则字典，键为正则匹配表达式（字符串, pat），值为处理结果（字符串或函数, rep）
rules = {
    ### 连续半角空格处理
    " +" :" ",
    ### 单字/特殊字符
    "(?<![花牡虾海车香])蛤(?![蜊蚧子蜃])":"Ha", "蛤": "Ge",
    "翠": "翆", "尻": "𡱧", "淫":"Yin", "岿": "巍", "屌": "吊", "党": "Dαng", "慎": "Shen",
    "[àáâãäåÀÁÂÃÄÅāǎ]": "a", "[èéêëÈÉÊËēě]": "e", "[ìíîïÌÍÎÏīǐ]": "i", "[òóõôöÒÓÔÕÖōǒ]": "o", "[ùúûüÙÚÛÜūǔ]": "u", "[ǖǘǚǜü]": "v",
    "⑤": "(5)", "⑥": "(6)", "⑧": "(8)", "⑨": "(9)", "⑩": "(10)", "０": "0", "５": "5", "６": "6", "９": "9", "×": "x", "♀": "",
    "Ⅰ": "I", "Ⅱ": "II", "Ⅲ": "III", "Ⅳ": "IV",
    ### 英文非常规处理规则
    "(?ia)(?<!\w)(t)( ?w| ?a ?m)(?! ?\w)": lambda x: letter[x.group(1)] + x.group(2),
    "(?ia)(?<!\w)(x ?)(i)(?! ?\w)": lambda x: x.group(1)+sp+x.group(2),
    "(?ia)(?<!\w)(i ?l ?i ?)(b ?i ?l ?i ?b)(?! ?\w)": lambda x: x.group(1)+sp+x.group(2),
    "(?i)i ?s ?(?=i ?s)": lambda x: x.group() + sp,
    "(?i)m ?([ai]) ?(?=m ?\\1)": lambda x: x.group() + sp,
    "(?i)([dp]) ?i ?l ?i ?(?=\\1 ?i ?l ?i)": lambda x: x.group() + sp,
    "(?i)n ?i ?c ?o ?(?=n ?i ?c ?o)": lambda x: x.group() + sp,
    "(?i)([.,。，·] ?)(c.?n|c.?o.?m|t ?k)": lambda x: x.group(1) + sp*2 + x.group(2),
    "(?a)(?<!\w)8 ?.? ?(?=9(?! ?\w))": lambda x: fill(x.group(),3), 
    ### 中文非常规处理规则
    "([草艹操日][ %s]*)([你我他她它比笔逼]|时光|女儿)"%p_marks: lambda x: x.group(1)+sp+x.group(2),
    "(点 ?){2}(?=点)": lambda x: x.group()+sp,
    "(大 ?){4}(?=大)": lambda x: x.group()+sp,
    "([啪绿弯湾内色涩哑])(?= ?\\1)": lambda x: x.group(1) + sp,
    "加 ?速 ?(?=加 ?速)": lambda x: x.group() + sp,
    "嘀 ?哩 ?(?=嘀 ?哩)": lambda x: x.group() + sp,
    "鸡.*?(?=鸡)": lambda x: fill(x.group(),3),
    "光.*?(?=光)": lambda x: fill(x.group(),4),
    "共.*?(?=共)": lambda x: fill(x.group(),5),
    "啪.*?(?=啪 ?\S? ?啪)": lambda x: fill(x.group(),3),
    "越(?=(?: ?\S){0,8} ?共)": "Yue",
    "(想 ?)(死)(?! ?你)": lambda x: x.group(1)+sp+x.group(2),
    "(书 ?)(记)(?! ?舞)": lambda x: x.group(1)+sp+x.group(2),
    "(?<!老)(干 ?)(妈)": lambda x: x.group(1)+sp+x.group(2),
    "(猎 ?)(人)(?=.*?电 ?影)": lambda x: x.group(1)+sp+x.group(2),
    "([买卖].*?硬 ?)(币)": lambda x: x.group(1)+sp+x.group(2),
    "(小 ?学|[初高] ?中)(?=.*?[外语书政])": lambda x: x.group()[0]+sp+x.group()[1:], # 格式：甲#1乙#9丙(#1丁)
    "[习習](?=.*?[平苹])": "Χi",
    "炼(?=.*?铜)": "lian",
    "[撸噜] ?[^\s一]?(?= ?一.*?下)": lambda x: fill(x.group(),3),
    "(?i)([习習].*?)(a)(pp)": lambda x: x.group(1)+letter[x.group(2)]+x.group(3),
    "(?i)([六6⑥]|l ?i ?u)(.*?)([四肆4④]|s ?i)": lambda x: (x.group(1)+fill(x.group(2),4)+x.group(3)) if x.group(1)+x.group(3)!="64" else x.group(),
    "(?i)([%s] ?|f ?a? ?)([%s会能弄]|l ?u ?n)"%(hz_fa,hz_lun): lambda x: x.group(1)+sp+x.group(2),
    "(?i)[加+](?: ?[^\s微薇v]){0,5}(?= ?[微薇v].*?\w)": lambda x: fill(x.group(),7),
    "微(?: ?[^\s信]){0,5}(?= ?信.*?\w)": lambda x: fill(x.group(),7),
    "金(?=[ %s]*[三四])"%p_marks: lambda x: x.group()+sp,
    "工(?=[ %s]*期)"%p_marks: lambda x: x.group()+sp,
    "巨(?=[ %sa-zA-Z]*婴)"%p_marks: lambda x: x.group()+"1",
    ### 保护型处理规则
    "[习習]": lambda x: x.group()+sp,
    "(?i)r(?= ?i.*?[你我他她它].*?[妈吗马嘛母m])": lambda x: letter[x.group()],
    "(?i)t(?= ?a.*?[妈吗马嘛母家])": lambda x: letter[x.group()],
    
    
    ### 2.0版本屏蔽字，填充机制不适用，一般需要加空格（太乱了，啥时候整理一下）
    "尼嚎": "你好", "人妖": "人Yao", "咖喱 ?人": "咖喱Ren", "全 ?家 ?炸": "全 家Zha", "糖尿病": "糖尿bing", "神经质": "神经 质",
    "牲畜": "牲%s 畜"%sp, "快死": "快%s 死"%sp, "坦克": "坦%s 克"%sp, "(?<![小文])丑":"chou", "(?<!愚)蠢(?!蠢?欲动)":"chun",
    
    "母韵": insert_space, "太笨": insert_space, "全家": insert_space, "变态": insert_space, "彩笔": insert_space, 
    "狒狒": insert_space, "闭嘴": insert_space, "双亲": insert_space, "渣女": insert_space, "股间": insert_space, 
    "矮子": insert_space, "小偷": insert_space, "愚蠢": insert_space, "脑子": insert_space, "大妈": insert_space,
    "好吵": insert_space, "琐事": insert_space, "长得": insert_space, "心恶": insert_space,
    "臭小鬼": insert_space, "老太婆": insert_space, "恶心心": insert_space, "脏(?:话|东西)": insert_space,
    "你是个[Pp]": insert_space, "整[形容]": insert_space, "难[看听]": insert_space, "[男女]妖": insert_space, 
    "滚[滚开]": insert_space, "(?<![大小])傻瓜": insert_space, "垃圾(?!游戏)": insert_space,
    
    "%s猴子%s"%(f1,f2): insert_space, "%s猩猩%s"%(f1,f2): insert_space, "%s村人%s"%(f1,f2): insert_space, "%s说话%s"%(f1,f2): insert_space,
    "%s爹妈%s"%(f1,f2): insert_space, "%s笨笨%s"%(f1,f2): insert_space, "%s孤勇者%s"%(f1,f2): insert_space,
    "%s吃的吗%s"%(f1,f2): insert_space, "%s断[手脖]%s"%(f1,f2): insert_space, "%s作[文者啊吧吗么]%s"%(f1,f2): insert_space,
    
    "真(?=[^\s不]{0,3}[傻笨蠢病疯丑矮])": add_space,
    "[嘴脸鼻眼脑舌](?=[^\s\d]{0,6}?[胖矮丑烦笨傻蠢怪臭土大睁垃混])": add_space,
    "[你您他她这那个](?=[^\s\d个]{0,3}?[脸嘴鼻脑舌货猴胖矮丑烦笨傻蠢怪臭土歪睁垃混])": add_space,
    "[你您他这那](?=.*?位.*?要求)": add_space,
    "[你您他她](?=.*?东西)": add_space,
    "睁(?=[^\s睁]{0,3}?[开嘴脸鼻眼脑舌])": add_space,
    "[脸脑鼻口](?=.*?像)" : add_space,
    "像(?=.*?[脸脑鼻口])" : add_space,
    
    "[嘴脸鼻眼脑舌个](?=\S{0,4}?[样歪])": add_space,
    "%s妖(?!(?:[\s\d\u4E00-\u9FA5] ?){2})"%(f1): add_space,
    "%s死(?![\s2-79\u4E00-\u9FA5])"%(f1): "Si",
    "大(?=[^\s\d]?舌)": add_space,
    "[嘴脑](?=[^\s\d]?跟)": add_space,
    "没(?=[妈马码蚂玛犸吗嘛]|眼睛|有?脑子|头脑)": add_space,
    "[妈马吗码蚂玛犸嘛](?=[^\s\d]?没)": add_space,
    "(有[^\s\d]{0,3})(?<!中二)(病)": lambda x: x.group(1)+"bing",
    "[%s你您](?=[^\s\d]?[%s])"%(hz_ni,hz_ma): add_space,
    "[%s](?=[^\s\d]?[%s您])"%(hz_ma,hz_ni): add_space,
    "[日草艹操干曰死烧解透跳杀](?=.*?[你尼我他她它].*?[妈马吗码蚂玛犸嘛母m家])": add_space,
    "[你您他她男女人][^\s人]?(?=[^\s\d]?(?:多.*?话|话.*?多|话%s))"%(f2): add_space,
    "好多(?=[^\s\d]?猴)": add_space, 
    "死(?=\S?[心狗吧吗嘛啊呢哦么宅])": add_space,
    "[病笨傻蠢](?=[^\s\d]{0,2}[样人吧吗嘛啊呢哦么了])": add_space,
    "[胖矮](?=\S{0,3}?样)"
    "[笨傻](?=.{0,2}[逼比笔币Bb])": lambda x: x.group()+" 1",
    "[猪狗](?=\S{0,2}种)": lambda x: x.group()+" / ",
    "[一条](?=[^\s\d条]{0,2}狗)": add_space,
    "雑(?! )": add_space,
    "\d(?=.*?字母表)": add_space,
    "残(?=[疾障\u0800-\u4E00])": add_space, # 后接日文时进行保护性处理
    "(?i)(g[%s]) ?(c)"%(p_marks): lambda x: x.group(1)+" "+sp+x.group(2),
    "呕(?=呕)": "呕 ",
    "(恶[^\s心]?)心": lambda x: " "+x.group(1)+"xin",
    # "吗[？?]?(?![\s\d\u4E00-\u9FA5])": "吗？", # 保护性处理（试行）
    "点\S?(?=胖)": add_space,
}

def fill(string,length):
    '''填补字符串string，使其中的非空格字符数等于length'''
    dots=sp*(length-len(string)+string.count(" "))
    return string+dots

# <DATA END>
