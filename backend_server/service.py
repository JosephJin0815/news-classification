"""Backend Service"""
import operations
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

def add(num1, num2):
    print("add is called with %d and %d" % (num1, num2))
    return num1 + num2

def getOneNews():
    """get one news"""
    print("getOneNews is called")
    return operations.getOneNews()

def getNewsSummariesForUser(user_id, page_num):
    """get news summaries for a user"""
    print("get_news_summaries_for_user is called with %s and %s" % (user_id, page_num))
    return operations.getNewsSummariesForUser(user_id, page_num)

# service.py
def logNewsClickForUser(user_id, news_id):
    """ Log a click event for user """
    print("log_news_click_for_user is called with %s and %s" % (user_id, news_id))
    return operations.logNewsClickForUser(user_id, news_id)


RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(getOneNews, "getOneNews")
# register the method to RPC server
RPC_SERVER.register_function(getNewsSummariesForUser, 'getNewsSummariesForUser')
RPC_SERVER.register_function( logNewsClickForUser, 'logNewsClickForUser')

print("Starting RPC server on %s:%d" % (SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()
