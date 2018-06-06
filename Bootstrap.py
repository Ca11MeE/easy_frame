import boot,mysql

# 启动服务器
if '__main__' == __name__:
    # app.debug=True
    boot.get_app().run(host='0.0.0.0', port=443, ssl_context=(mysql.project_path + '/sslContext/1_zxyzt.cn_bundle.crt', mysql.project_path + '/sslContext/2_zxyzt.cn.key'))
    # _app.run(host='127.0.0.1', port=443, ssl_context=(mysql.project_path + '/sslContext/1_zxyzt.cn_bundle.crt', mysql.project_path + '/sslContext/2_zxyzt.cn.key'))
    # 启动服务器
    # boot.get_app().run(host='0.0.0.0',port=443,ssl_context='adhoc')
