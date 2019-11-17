# SPTAG-rpc-service
encapsulation of microsoft/SPTAG python API into rpc service.

## Installation
Install [SPTAG](https://github.com/microsoft/SPTAG/) in docker, and put SPTAG_rpc_server.py in /path/to/Release

Then Run:
```bash
python3 SPTAG_rpc_server.py
```

After running rpc server, you can use Ctrl+p plus Ctrl+q to put the docker container in background.

## Demo Client Api
```python
import numpy as np
from SPTAG_rpc_demo_client import SPTAG_RpcDemoClient, DataBean


if __name__ == "__main__":
    client = SPTAG_RpcDemoClient("127.0.0.1", "8888")
    beans = []
    for i in range(5):
        vec = i * np.ones((10,), dtype=np.float32)
        beans.append(DataBean(_id=f"s{i}", vec=vec))
    
    index_name = "test"
    print("Adding Data:", client.add_data(index_name, beans))
    
    print("*"*100)
    print("Test Search")
    q = DataBean(_id=f"s{0}", vec=0 * np.ones((10,), dtype=np.float32))
    print(client.search(index_name, [q], 3))
    
    print("*"*100)
    print("Test Delete:", client.delete_data(index_name, [q]))
    
    print("*"*100)
    print("Test Search After Deletion")
    print(client.search(index_name, [q], 3))
    
    print("*"*100)
    print("Test Delete Index:", client.delete_index(index_name))

```

## Test SearchClient and SearchService

### export test_index_input.txt
```bash
python3 export_test_index_input.py
```

### copy test_index_input.txt into docker
```bash
docker cp mm_index_input.txt 25042d741f07:/app/Release/
```

### enter in SPTAG-docker, create index by indexbuilder
```bash
docker attach 25042d741f07
./indexbuilder -d 10 -v Float  -i ./test_index_input.txt -o data/test_index -a BKT -t 2 Index.DistCalcMethod=L2
```

### start SPTAG Search Service
```bash
python3 SPTAG_rpc_search_server.py -i test_index
```

### test Search Client Api
```python
import numpy as np
from SPTAG_rpc_search_client import SPTAG_RpcSearchClient, DataBean


if __name__ == "__main__":
    client = SPTAG_RpcSearchClient("127.0.0.1", "8888")
    print("Test Search")
    q = DataBean(_id=f"s{0}", vec=0 * np.ones((10,), dtype=np.float32))
    print(client.search([q], 3))
```
