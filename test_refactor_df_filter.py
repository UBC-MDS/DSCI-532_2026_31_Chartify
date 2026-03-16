import pandas as pd
import pytest
from df_filter import filter_data
 
 
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Artist": ["Taylor Swift", "Drake", "Taylor Swift", "ABBA"],
        "most_playedon": ["Spotify", "Youtube", "Youtube", "Spotify"],
        "streams": [1000, 2000, 1500, 3000],
    })
 
def test_filter_by_artist_case_insensitive(sample_df):
    """Filtering by artist should be case-insensitive and return only matching rows."""
    result = filter_data(sample_df, "taylor swift", "Both")
    assert len(result) == 2
    assert all(result["Artist"] == "Taylor Swift")
 
def test_filter_by_platform_excludes_other_platform(sample_df):
    """Filtering by a specific platform should exclude rows from other platforms."""
    result = filter_data(sample_df, "", "Spotify")
    assert len(result) == 2
    assert all(result["most_playedon"] == "Spotify")
    assert "Youtube" not in result["most_playedon"].values