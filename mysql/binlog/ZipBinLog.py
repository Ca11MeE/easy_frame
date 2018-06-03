import re,uuid

def zip_as_bin(file):
    f=open(file,'r',encoding='utf8')
    bstr=f.read()
    # 去除注释与空格,换行等
    bstr = re.sub('\\s+', ' ', re.sub('<!--.*-->', ' ', bstr))
    bs=[]
    for b in str.encode(bstr):
        bs.append(b)
    # 返回唯一标识值
    return uuid.uuid3(uuid.NAMESPACE_DNS,bstr)