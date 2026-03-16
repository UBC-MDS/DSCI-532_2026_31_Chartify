import pandas as pd
 
def filter_data(df: pd.DataFrame, artist_input: str, platform_input: str) -> pd.DataFrame:
    """
    Filter a DataFrame by artist name and platform.
 
    Args:
        df: The source DataFrame containing 'Artist' and 'most_playedon' columns.
        artist: Artist name to filter by. Given by input_selectize("artist", ...)
        platform: Platform to filter by. Given by input_radio_buttons where the choices are choices=["Spotify", "Youtube", "Both"]
 
    Returns:
        A filtered copy of the DataFrame to used as a reactive cal and for other components/outputs.
    """
    artist = artist_input.strip()
 
    if artist:
        filtered_df = df[df["Artist"].str.lower() == artist.lower()].copy()
    else:
        filtered_df = df.copy()
 
    if platform_input != "Both":
        filtered_df = filtered_df[filtered_df["most_playedon"] == platform_input]
 
    return filtered_df