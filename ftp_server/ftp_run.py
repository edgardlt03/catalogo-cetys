from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

authorizer = DummyAuthorizer()
authorizer.add_user("webcraft", "12345", ".", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("0.0.0.0", 21), handler)
server.serve_forever()
