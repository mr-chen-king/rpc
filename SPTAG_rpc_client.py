from xmlrpc.client import ServerProxy
import numpy as np


class DataBean:
    def __init__(self, _id: str, vec: np.array):
        self._id = _id
        self.vec = vec
        if '\n' in _id:
            raise Exception("_id cannot contain \\n")

        if len(vec.shape) != 1:
            raise Exception("vec must be 1-d vector")

        if vec.dtype != np.float32:
            raise Exception("the dtype of vec must be np.float32")


class SPTAG_RpcClient:

    ALGO_BKT = "BKT"  # SPTAG-BKT is advantageous in search accuracy in very high-dimensional data
    ALGO_KDT = "KDT"  # SPTAG-KDT is advantageous in index building cost,

    DIST_L2 = "L2"
    DIST_Cosine = "Cosine"

    def __init__(self, server_url):
        self.proxy = ServerProxy(server_url)

    def add_data(self, index_name, beans: [DataBean], algo=ALGO_BKT, dist=DIST_L2):
        meta, vecs = self.__get_meta_and_vec_from_beans(beans)
        return self.proxy.add_data(index_name, vecs, meta, algo, dist)

    def delete_data(self, index_name, beans: [DataBean]):
        _, vecs = self.__get_meta_and_vec_from_beans(beans)
        return self.proxy.delete_data(index_name, vecs)

    def search(self, index_name, beans: [DataBean], p_resultNum):
        _, vecs = self.__get_meta_and_vec_from_beans(beans)
        return self.proxy.search(index_name, vecs, p_resultNum)

    def delete_index(self, index_name):
        return self.proxy.delete_index(index_name)

    def __get_meta_and_vec_from_beans(self, beans: [DataBean]):
        if len(beans) == 0:
            raise Exception("beans length cannot be zero!")

        if len(beans) > 1000:
            raise Exception("cannot add more than 1000 beans at once!")

        dim = beans[0].vec.shape[0]
        meta = ""
        vecs = np.zeros((len(beans), dim))

        for i, bean in enumerate(beans):
            meta += bean._id + '\n'
            vecs[i] = bean.vec

        meta = meta.encode()
        return meta, vecs


if __name__ == '__main__':
    client = SPTAG_RpcClient("http://127.0.0.1:8888")
    beans = []
    for i in range(5):
        beans.append(DataBean(_id=f"s{i}", vec=i * np.ones((10,))))

    index_name = "test"
    print("Adding Data:", client.add_data(index_name, beans))

    print("*"*100)
    print("Test Search")
    q = DataBean(_id=f"s{0}", vec=0 * np.ones((10,)))
    print(client.search(index_name, [q], 3))

    print("*"*100)
    print("Test Delete:", client.delete_data(index_name, [q]))

    print("*"*100)
    print("Test Search After Deletion")
    print(client.search(index_name, [q], 3))

    print("*"*100)
    print("Test Delete Index:", client.delete_index(index_name))

