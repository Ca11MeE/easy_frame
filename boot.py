from flask import Flask
import mysql,os,re
from mysql import Pool
import properties

# 定义容器(同时防止json以ascii解码返回)
app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 处理各模块中的自动注入以及组装各蓝图
# dir_path中为蓝图模块路径,例如需要引入的蓝图都在routes文件夹中,则传入参数'/routes'
def map_apps(dir_path):

    path=os.getcwd()+dir_path
    list=os.listdir(path)
    # list.remove('__pycache__')
    while 0<len(list):
        try:
            file=list.pop(0)
            print('加载',file)
            f_model=__import__('routes.'+re.sub('\.py','',file),fromlist=True)
            app.register_blueprint(f_model.app)
        except:
            pass

def get_app():
    return app

# 启动服务器
if '__main__' == __name__:
    # print('加载数据库模块')
    mysql.pool = Pool.Pool()
    # print('加载完毕')
    for path in properties.blueprint_path:
        map_apps(path)
    # app.debug=True
    app.run(host='0.0.0.0', port=443, ssl_context=(mysql.project_path + '/sslContext/1_zxyzt.cn_bundle.crt', mysql.project_path + '/sslContext/2_zxyzt.cn.key'))
    # _app.run(host='127.0.0.1', port=443, ssl_context=(mysql.project_path + '/sslContext/1_zxyzt.cn_bundle.crt', mysql.project_path + '/sslContext/2_zxyzt.cn.key'))


    # _app.run(host='0.0.0.0',port=443,ssl_context='adhoc')

