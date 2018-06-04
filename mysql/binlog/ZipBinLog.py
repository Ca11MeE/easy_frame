import re, uuid


def zip_as_bin(file):
    f = open(file, 'r', encoding='utf8')
    bstr = f.read()
    # 去除注释与空格,换行等
    bstr = re.sub('\\s+', ' ', re.sub('<!--.*-->', ' ', bstr))
    z_s=zip_str(bstr)
    print(z_s)
    print(len(z_s))
    b_s=un_zip_str(z_s)
    print(b_s)
    print(len(b_s))
    bs = []
    for b in str.encode(bstr):
        bs.append(b)
    # 返回唯一标识值
    return uuid.uuid3(uuid.NAMESPACE_DNS, bstr)


def bindigits(n, bits):
    s = bin(n & int("1" * bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

def zip_str(string):
    # 压缩内容
    z_result = ''
    for s in string:
        c = ord(s)
        # print(c)
        # b=bin(c)
        # print(b)
        # 强制延伸64位
        bd = bindigits(c, 64)
        # print(bd)
        # 除去0(四位一除)
        bd = re.sub('00000000', '#', bd)
        # print(bd)
        bd = re.sub('0000', '@', bd)
        # print(bd)
        bd = re.sub('00', '!', bd)
        # print(bd)
        bd = re.sub('\#\#\#\#\#\#\#\#', '^', bd)
        # print(bd)
        bd = re.sub('\#\#\#\#', '%', bd)
        # print(bd)
        bd = re.sub('\#\#', '$', bd)
        # print(bd)
        # 整理1(两位数会造成解码混乱)
        for i in range(9):
            # print('i=',i)
            num = 9 - i
            bd = re.sub('1{' + str(num) + '}', str(num), bd)
        # 组合字符分节符
        bd = re.sub('\%\$\#', '\\\\', bd)

        z_result = z_result + str(bd)+','
    return z_result

# 解压
def un_zip_str(string):
    un_z_result=''
    list=string.split(',')
    # 除去最后一个值放干扰
    list.pop(len(list)-1)
    for bd in list:
        bd = re.sub('\\\\', '%$#', bd)
        bd = re.sub('\$', '##', bd)
        bd = re.sub('\%', '####', bd)
        bd = re.sub('\^', '########', bd)
        bd = re.sub('\!', '00', bd)
        bd = re.sub('\@', '0000', bd)
        bd = re.sub('\#', '00000000', bd)
        # print(bd)
        # 解压1
        base = ''
        for i in range(9):
            num=i+1
            base=base+'1'
            bd=re.sub(str(num),base,bd)
            # print(bd)
        # print(bd)
        # 转换为字符串
        un_z_result=un_z_result+chr(int(bd, 2))
    return un_z_result

zip_as_bin('test.xml')