from mysql.remote import Cell

# 工厂模式获取远程细胞实例
def getCell(file_name,remote_path):
    return Cell.get_cell(file_name=file_name,remote_path=remote_path)