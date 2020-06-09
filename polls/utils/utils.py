import time
from django.core import signing
import hashlib
from django.core.cache import cache  #引入缓存模块



# 加密
def encrypt(obj):
    """加密"""
    value = signing.dumps(obj, key='liming', salt='www.gongliming.com')
    value = signing.b64_encode(value.encode()).decode()
    return value


# 解密
def decrypt(src):
    """解密"""
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key='liming', salt='www.gongliming.com')
    return raw


# 创建token
def create_token(username):
    """生成token信息"""
    # 1. 加密头信息
    header = encrypt({'typ': 'JWP', 'alg': 'default'})
    # 2. 构造Payload
    payload = {"username": username, "iat": time.time()}
    payload = encrypt(payload)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    # 存储到缓存中
    cache.set(username, token, 60*60*12*14)
    return token


def get_payload(token):
    payload = str(token).split('.')[1]
    payload = decrypt(payload)
    return payload


# 通过token获取用户名
def get_username(token):
    payload = get_payload(token)
    return payload['username']
    pass


# 检测token
def check_token(token):
    username = get_username(token)
    print(username)
    results_token = cache.get(username)
    print(results_token)
    print(token)
    if results_token:
        return results_token == token
    return False


# 加密其它内容
def encrypt_other(username):
    """生成token信息"""
    # 1. 加密头信息
    header = encrypt({'typ': 'JWP', 'alg': 'default'})
    # 2. 构造Payload
    payload = {"username": username, "iat": time.time()}
    payload = encrypt(payload)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    # 存储到缓存中
    return token