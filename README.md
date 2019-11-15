# SPTAG-rpc-service
encapsulation of microsoft/SPTAG python API into rpc service.

## Installation
Install [SPTAG](https://github.com/microsoft/SPTAG/) in docker, and put SPTAG_rpc_server.py in /path/to/Release

Then Run:
```bash
python3 SPTAG_rpc_server.py
```

After running rpc server, you can use Ctrl+p plus Ctrl+q to put the docker container in background.

## Client Api
```python
import numpy as np
from SPTAG_rpc_client import SPTAG_RpcClient, DataBean

client = SPTAG_RpcClient("http://127.0.0.1:8888")
beans = []
for i in range(5):
    vec = i * np.ones((10,), dtype=np.float32)
    beans.append(DataBean(_id=f"s{i}", vec=vec))

index_name = "test"
print("Adding Data:", client.add_data(index_name, beans))

print("*"*100)
print("Test Search")
q = DataBean(_id=f"s{0}", vec=0 * np.ones((10,), dtype=np.float32))

print("*"*100)
print("Test Delete:", client.delete_data(index_name, [q]))

print("*"*100)
print("Test Search After Deletion")
print(client.search(index_name, [q], 3))

print("*"*100)
print("Test Delete Index:", client.delete_index(index_name))

```
