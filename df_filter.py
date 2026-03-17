import pandas as pd
import ibis
 
def filter_data(df: ibis.expr.types.relations.Table, artist_input: str, platform_input: str) -> pd.DataFrame:
    """
    Filter a DataFrame by artist name and platform.
 
    Args:
        df: An Ibis Table Expression that contains 'Artist' and 'most_playedon' columns.
        artist: Artist name to filter by. Given by input_selectize("artist", ...)
        platform: Platform to filter by. Given by input_radio_buttons where the choices are choices=["Spotify", "Youtube", "Both"]
 
    Returns:
        A filtered copy of the DataFrame to used as a reactive cal and for other components/outputs.
    """
    artist = artist_input
 
    if artist:
        filtered_df = df.filter([df.Artist == artist])
    else:
        filtered_df = df
 
    if platform_input != "Both":
        filtered_df = filtered_df.filter([filtered_df.most_playedon == platform_input])
 
    return filtered_df.to_pandas()