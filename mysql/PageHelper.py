import re

# 打包分页信息
def pkg_page_info(page_num=1, page_size=1,page_model=[]):
    if 0 >= len(page_model):
        # print(locals())
        return locals()
    else:
        page_info={}
        # 选取对应key写入数据
        for key in page_model:
            # print(key)
            if re.match('.*[nN][uU][mM].*',string=key):
                page_info[key]=page_num
            if re.match('.*[sS][iI][zZ][eE].*',string=key):
                page_info[key]=page_size
        # print(page_info)
        return page_info

# 解包分页信息
def depkg_page_info(page_info):
    for key in page_info:
        # print(key)
        if re.match('.*[nN][uU][mM].*', string=key):
            _page_num = page_info[key]
        if re.match('.*[sS][iI][zZ][eE].*', string=key):
            _page_size = page_info[key]
    return  'limit ' + str((int(_page_num) - 1) * int(_page_size)) + ',' + str(_page_size)
