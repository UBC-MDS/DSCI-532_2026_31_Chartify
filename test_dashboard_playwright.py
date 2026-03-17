# Running tests:
# python -m pytest test_dashboard_playwright.py -v --browser firefox
from shiny.playwright import controller
from shiny.run import ShinyAppProc
from shiny.pytest import create_app_fixture
from playwright.sync_api import Page

app = create_app_fixture("src/app.py")


def test_default_metric_cards_are_correct(page: Page, app: ShinyAppProc) -> None:
    '''Each card should contain the values with $NOT artist upon load.
    
    If not/failed, something about the original/first load of the Dashboard did not go 
    according to plan.'''
    page.goto(app.url)

    avg_streams = controller.OutputText(page, "card_avg_stream")
    avg_likes = controller.OutputText(page, "card_avg_likes")
    avg_views = controller.OutputText(page, "card_avg_views")

    avg_streams.expect_value("112,763,800",  timeout=10000)
    avg_likes.expect_value("274,716",  timeout=10000)
    avg_views.expect_value("11,078,490",  timeout=10000)


def test_platform_spotify_filter_for_top5(page: Page, app: ShinyAppProc) -> None:
    ''' After filtering Spotify Radio button, there should be only spotify related
     output within the top 5 dataframe and with expected values. 
     
    If there isn't this would indicate that something about the reactive calculation 
    and filtering did not work as expected.'''
    page.goto(app.url)

    platform = controller.InputRadioButtons(page, "filter_platform")
    top5 = controller.OutputDataFrame(page, "top_5")
    artist = controller.InputSelectize(page, "artist")

    artist.set("ABBA", timeout=10000)
    platform.set("Spotify", timeout=10000)
    top5.expect_nrow(5,  timeout=10000)
    top5.expect_cell("Spotify", row=0, col=2, timeout=10000)
    top5.expect_cell("Dancing Queen", row=0, col=0, timeout=10000)
    top5.expect_cell("252,601,051", row=4, col=3, timeout=10000)

def test_metric_select_changes_makes_no_unintended_updates(page: Page, app: ShinyAppProc) -> None:
    """Cycles through all four metric options, which should only change the scatter plot, and verifies
    the Top 5 table remains intact and remains to be sorted by just the steams count for the artist selected +
    value card are also the same. Without this test passing - there is indication of a break in fundamental 
    dashboard logic and intended interactions."""
    page.goto(app.url)

    metric = controller.InputSelect(page, "filter_metric")
    top5 = controller.OutputDataFrame(page, "top_5")
    avg_streams = controller.OutputText(page, "card_avg_stream")
    avg_likes = controller.OutputText(page, "card_avg_likes")
    avg_views = controller.OutputText(page, "card_avg_views")

    for m in ["Likes", "Views", "Comments", "Streams"]:
        metric.set(m)

        top5.expect_cell("Tell Em", row=0, col=0, timeout=10000)
        top5.expect_cell("Beautiful Havoc", row=3, col=1, timeout=10000)
        top5.expect_cell("78,913,057", row=5, col=4, timeout=10000)

        avg_streams.expect_value("112,763,800",  timeout=10000)
        avg_likes.expect_value("274,716",  timeout=10000)
        avg_views.expect_value("11,078,490",  timeout=10000)

        
def test_scatter_plot_has_traces(page: Page, app: ShinyAppProc) -> None:
    '''Scatter plot should render 20 traces (10 features × 1 scatter + 1 trend line) on default load.
    
    If not/failed, either the Plotly widget failed to mount, a feature was dropped from 
    NUMERICAL_FEATURES, or the trend line generation in the scatter_plot render function broke.'''
    #Used Claude and Sonnet 4.6 to write the confirm plotly scatterplot works as intended
    page.goto(app.url)

    plotly_div = page.locator("#scatter_plot .js-plotly-plot")
    plotly_div.wait_for(state="visible", timeout=15000)

    # Assert exact trace count: 10 features × (1 scatter + 1 trend line) = 20
    trace_count = page.eval_on_selector( 
        "#scatter_plot .js-plotly-plot",
        "el => el._fullData.length"
    )
    assert trace_count == 20