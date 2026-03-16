import pandas as pd
 
 
def filter_data(df: pd.DataFrame, artist_input: str, platform_input: str) -> pd.DataFrame:
    artist = artist_input.strip()
 
    if artist:
        filtered_df = df[df["Artist"].str.lower() == artist.lower()].copy()
    else:
        filtered_df = df.copy()
 
    if platform_input != "Both":
        filtered_df = filtered_df[filtered_df["most_playedon"] == platform_input]
 
    return filtered_df