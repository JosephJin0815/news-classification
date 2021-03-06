import operator
import os
import sys

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
SERVER_HOST = 'localhost'
SERVER_PORT = 5050

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def getPreferenceForUser(user_id):
    """ Get user's pereference in an ordered class list """
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':user_id})
    # if this is a new user,
    # there is no model, and there is no preference
    if model is None:
        return []
    # sort by the perferance value in descending order
    sorted_tuples = sorted(list(model['preference'].items()), key=operator.itemgetter(1), reverse=True)
    # get all the key
    sorted_list = [x[0] for x in sorted_tuples]
    # get all value list
    sorted_value_list = [x[1] for x in sorted_tuples]
    # if all the preference value are same, there is no preference
    # since the array is sorted, we only need to compare the
    # first and the last value.
    # since the value is float, we cannot compare directly
    if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return []

    return sorted_list

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(getPreferenceForUser, 'getPreferenceForUser')
print("Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT))
RPC_SERVER.serve_forever()
