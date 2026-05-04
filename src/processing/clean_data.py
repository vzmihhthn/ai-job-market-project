import pandas as pd

def clean_data(df):
    df = df.drop_duplicates()

    # chuẩn hóa tên cột (an toàn)
    df.columns = df.columns.str.strip().str.lower()

    # xử lý salary
    df['salary_usd'] = pd.to_numeric(df['salary_usd'], errors='coerce')

    # xử lý date
    df['posting_date'] = pd.to_datetime(df['posting_date'], errors='coerce')

    # drop những dòng quan trọng bị thiếu
    df = df.dropna(subset=['salary_usd', 'job_title'])

    return df