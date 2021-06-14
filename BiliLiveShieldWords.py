# coding: utf-8
import re
from shield_data import words,rules

def get_len(string):
    # 获取字符串string的长度
    # 在len()的基础上，[]及其中的内容统一视为一个字符。
    return len(re.sub(r"\[.+?\]","~",string))

def measure(string,length):
    # 判断字符串string中非空格字符数是否小于length
    return get_len(string)-string.count(" ")<length

def fill(string,length):
    # 填补字符串string，使其中的非空格字符数等于length
    dots="`"*(length-get_len(string)+string.count(" "))
    return string+dots

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
    # 如果word不含“#”，则默认在第一个字符后添加“`”
    try:
        groups=re.split(r"#[1-9]",word)
        n=len(groups)-1
        if n==0:
            pat = "(?i)" + " ?".join(word)
            rep = word[0] + "`" + word[1:]
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
        #print("[generate fail]%s\n%s"%(word,str(e)))
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
