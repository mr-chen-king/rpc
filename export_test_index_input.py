import numpy as np


with open("test_index_input.txt", "w") as f:
    for i in range(5):
        _id = f"s{i}"
        vec = i * np.ones((10,), dtype=np.float32)
        vec_str = "|".join([str(i) for i in vec.tolist()])
        f.write(f"{_id}\t{vec_str}\n")
