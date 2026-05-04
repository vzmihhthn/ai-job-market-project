from src.ingestion.load_data import load_csv
from src.processing.clean_data import clean_data
from src.processing.feature_engineering import add_features

def main():
    
    # df = load_csv("data/raw/ai_job_dataset.csv")
    df = load_csv("data/raw/ai_job_dataset1.csv")
    print("After load:", df.shape)

    df = clean_data(df)
    print("After clean:", df.shape)

    df = add_features(df)
    print("After feature:", df.shape)

    # df.to_csv("data/processed/jobs_cleaned.csv", index=False)
    df.to_csv("data/processed/jobs_cleaned1.csv", index=False)

if __name__ == '__main__':
    main()