def add_features(df):
    df['year'] = df['posting_date'].dt.year

    return df