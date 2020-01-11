import numpy as np
import SPTAG
import os
import shutil
import rpyc
from rpyc.utils.server import ThreadedServer


DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


class SPTAG_RpcDemoService(rpyc.Service):
    def exposed_add_data(self, index_name, p_data, p_meta, algo="BKT", dist="L2"):
        print("*"*100)
        print("add_data")
        p_data = np.array(p_data, dtype=np.float32)
        index_name = os.path.join(DATA_DIR, index_name)
        if os.path.exists(index_name):
            i = SPTAG.AnnIndex.Load(index_name)
        else:
            i = SPTAG.AnnIndex(algo, 'Float', p_data.shape[1])
        i.SetBuildParam("NumberOfThreads", '4')
        i.SetBuildParam("DistCalcMethod", dist)
        p_num = p_data.shape[0]
        success = i.AddWithMetaData(p_data, p_meta, p_num)
        if success:
            i.Save(index_name)
        return success

    def exposed_delete_data(self, index_name, p_data):
        print("*"*100)
        print("delete_data")
        p_data = np.array(p_data, dtype=np.float32)
        index_name = os.path.join(DATA_DIR, index_name)
        i = SPTAG.AnnIndex.Load(index_name)
        ret = i.Delete(p_data, p_data.shape[0])
        i.Save(index_name)
        return ret

    def exposed_search(self, index_name, p_data, p_resultNum):
        print("*"*100)
        print("search")
        p_data = np.array(p_data, dtype=np.float32)
        index_name = os.path.join(DATA_DIR, index_name)
        j = SPTAG.AnnIndex.Load(index_name)
        j.SetSearchParam("MaxCheck", '1024')
        returns = []
        for t in range(p_data.shape[0]):
            result = j.SearchWithMetaData(p_data[t], p_resultNum)
            res = []
            for i, _id in enumerate(result[2]):
                res.append({
                    result[2][i].decode().strip(): result[1][i]
                })
            returns.append(res)
        return returns

    def exposed_delete_index(self, index_name):
        print("*"*100)
        print("delete_index")
        try:
            index_name = os.path.join(DATA_DIR, index_name)
            shutil.rmtree(index_name)
            return True
        except:
            return False


if __name__ == '__main__':
    print("SPTAG_Demo_Service Serve on", 8000)
    t = ThreadedServer(SPTAG_RpcDemoService, port=8000, protocol_config={'allow_public_attrs': True})
    t.start()

# def test_api():
# import numpy as np
#
# n = 12
# x = np.ones((n, 10), dtype=np.float32) * np.reshape(np.arange(n, dtype=np.float32), (n, 1))
# m = ''
# for i in range(12):
#    m += str(i) + '\n'
#
# m = m.encode()
#
# add_data("test", x, m)
#
# delete_data("test", x[:1])
#
# search("test", x[:1], 3)
#
# delete_index("test")

