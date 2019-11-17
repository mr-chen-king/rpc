import numpy as np
import SPTAG
import os
import rpyc
from rpyc.utils.server import ThreadedServer
import sys
import getopt


DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


class SPTAG_RpcDemoService(rpyc.Service):

    def exposed_search(self, p_data, p_resultNum):
        global SPTAG_index
        print("*"*80)
        print("search called")
        p_data = np.array(p_data, dtype=np.float32)

        returns = []
        for t in range(p_data.shape[0]):
            result = SPTAG_index.SearchWithMetaData(p_data[t], p_resultNum)
            res = []
            for i, _id in enumerate(result[2]):
                res.append({
                    result[2][i].decode().strip(): result[1][i]
                })
            returns.append(res)
        return returns


if __name__ != "__main__":
    print("SPTAG_RpcDemoService can only run as main")
    sys.exit()


try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:")
except getopt.GetoptError:
    print('SPTAG_rpc_search_server.py -i <indexname>')
    sys.exit(2)

INDEX_NAME = ""
for opt, arg in opts:
    if opt == '-h':
        print('usage: SPTAG_rpc_search_server.py -i <indexname>')
        sys.exit()
    elif opt == "-i":
        INDEX_NAME = arg

if INDEX_NAME == "":
    print('usage: SPTAG_rpc_search_server.py -i <indexname>')
    sys.exit()

print("loading index:", INDEX_NAME)
index_name = os.path.join(DATA_DIR, INDEX_NAME)
SPTAG_index = SPTAG.AnnIndex.Load(index_name)
SPTAG_index.SetSearchParam("MaxCheck", '1024')


print("SPTAG_Search_Service Serve on", 8888)
t = ThreadedServer(SPTAG_RpcDemoService, port=8888)
t.start()

