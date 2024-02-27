# import os.path
# from waitress import serve
# from app import app
# import ssl
# # 以下为尝试以https运行，目前暂时失败。注意，flask自带的server只支持http协议
# context = ssl.create_default_context()
# context.load_cert_chain('server.crt', 'server.key')
# # certificate_path = os.path.abspath('C:/Users/86189/server.crt')
# # key_path = os.path.abspath('C:/Users/86189/server.key')
# # ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
# # ssl_context.load_cert_chain(certfile=certificate_path, keyfile=key_path,password='Bjjswan667')
# if __name__ == '__main__':
#     serve(app, listen='*:5000', url_scheme='https', ssl_context=context)
