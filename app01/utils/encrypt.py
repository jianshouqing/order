import hashlib

def md5_string(data_string):
    # 创建一个md5对象
    obj = hashlib.md5()
    # 更新md5对象，传入字节串
    obj.update(data_string.encode('utf-8'))
    # 返回md5哈希值的十六进制表示
    return obj.hexdigest()