import pandas as pd 
import kagglehub
from kagglehub import KaggleDatasetAdapter
import unicodedata
from sklearn.preprocessing import MinMaxScaler


def get_data():
    # Create a function to normalize Artist Names that have special characters to their closes ASCII equivalents
    # Function created with assistance by Claude AI
    def normalize_text(text):
        if isinstance(text, str):
            # Decompose special characters, the encode to ASCII 
            return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

    # Use KaggleDatasetAdapter to download the dataset programatically
    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "sanjanchaudhari/spotify-dataset/versions/1",
        "cleaned_dataset.csv", 
        pandas_kwargs={"encoding": "latin-1", "on_bad_lines": "skip", "engine": "python", 
                       "compression": "zip"
                       }
        )

    
    # Apply normalization of characters to Artist, Song and Album Names
    df['Artist'] = df['Artist'].apply(normalize_text)
    df['Album'] = df['Album'].apply(normalize_text)
    df['Track'] = df['Track'].apply(normalize_text)
    df['Title'] = df['Title'].apply(normalize_text)
    
    # Create MinMax Scaler for All Song Attributes To Place Them On A Uniform Scale
    scaler = MinMaxScaler(feature_range=(0, 10))
    song_feature = ['Danceability', 'Energy','Loudness', 'Speechiness', 'Acousticness',
                    'Instrumentalness','Liveness', 'Valence', 'Tempo', 'EnergyLiveness']
    
    # Apply scaling to all song feature columns
    for feature in song_feature:
        df[feature] = scaler.fit_transform(df[[feature]])
    
    return df 