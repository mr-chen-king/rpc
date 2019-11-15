from xmlrpc.server import SimpleXMLRPCServer
import numpy as np
import SPTAG
import os
import shutil


DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


def add_data(index_name, p_data, p_meta, algo="BKT", dist="L2"):
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


def delete_data(index_name, p_data):
    index_name = os.path.join(DATA_DIR, index_name)
    i = SPTAG.AnnIndex.Load(index_name)
    ret = i.Delete(p_data, p_data.shape[0])
    i.Save(index_name)
    return ret


def search(index_name, p_data, p_resultNum):
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


def delete_index(index_name):
    try:
        index_name = os.path.join(DATA_DIR, index_name)
        shutil.rmtree(index_name)
        return True
    except:
        return False


if __name__ == '__main__':
    server = SimpleXMLRPCServer(('127.0.0.1', 8888))
    server.register_function(add_data, "add_data")
    server.register_function(delete_data, "delete_data")
    server.register_function(search, "search")
    server.register_function(delete_index, "delete_index")
    print("Listening for Client")
    server.serve_forever()


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

