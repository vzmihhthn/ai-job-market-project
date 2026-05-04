import pandas as pd 

def load_csv(path):
    df = pd.read_csv(path)  # dùng tham số path luôn cho đúng
    return df
