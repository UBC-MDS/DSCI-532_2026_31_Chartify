# Running just these tests:
# python -m playwright install firefox && python -m pytest test_dashboard_playwright.py -v --browser firefox
from shiny.playwright import controller
from shiny.run import ShinyAppProc
from shiny.pytest import create_app_fixture
from playwright.sync_api import Page, expect

app = create_app_fixture("src/app.py")


def test_default_metric_cards_are_correct(page: Page, app: ShinyAppProc) -> None:
    '''Verifies all three metric cards display correct dataset-wide averages 
    on initial load with no artist filter applied - defaulting to $NOT artist.
    
    If not/failed, the filtered() reactive is not returning the full dataset or set 
    to the correct artist on startup, or the card_avg_stream, card_avg_likes, and/or
    card_avg_views render functions are computing incorrectly.'''
    page.goto(app.url)

    avg_streams = controller.OutputText(page, "card_avg_stream")
    avg_likes = controller.OutputText(page, "card_avg_likes")
    avg_views = controller.OutputText(page, "card_avg_views")

    avg_streams.expect_value("112,763,800",  timeout=10000)
    avg_likes.expect_value("274,716",  timeout=10000)
    avg_views.expect_value("11,078,490",  timeout=10000)


def test_platform_spotify_filter_for_top5(page: Page, app: ShinyAppProc) -> None:
    '''Verifies that selecting an artist and filtering to Spotify-only returns the correct top 5 songs 
    sorted by streams, with only Spotify-platform entries in the expected order.
    
    If not/failed, the platform branch in filter_data() is not correctly excluding YouTube rows, 
    or the top_5 render function is not sorting or slicing the filtered dataframe as intended.'''
    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    platform = controller.InputRadioButtons(page, "filter_platform")
    top5 = controller.OutputDataFrame(page, "top_5")
    artist = controller.InputSelectize(page, "artist")

    artist.set("ABBA", timeout=10000)
    page.wait_for_load_state("networkidle")

    platform.set("Spotify", timeout=10000)
    page.wait_for_load_state("networkidle")

    top5.expect_nrow(5, timeout=15000)

    # Kept getting DOM node errors. Asked Claude & it helped by giving me a function 
    # which uses page.locator() / a lazy descriptor — and finds the fresh node cleanly.
    # to try avoid running into the issue of "Element is not attached to the DOM" which
    # are very unpredictable / inconsistent bugs 
    def _expect_cell(page, output_id, row, col, value, timeout=15000):
        '''helper function to fix "Element is not attached to the DOM" errors'''
        cell = page.locator(f"#{output_id} tbody tr:nth-child({row + 1}) td:nth-child({col + 1})")
        expect(cell).to_have_text(value, timeout=timeout)
    
    _expect_cell(page, "top_5", row=0, col=0, value="Dancing Queen")
    _expect_cell(page, "top_5", row=0, col=2, value="Spotify")
    _expect_cell(page, "top_5", row=4, col=3, value="252,601,051")


def test_metric_select_changes_makes_no_unintended_updates(page: Page, app: ShinyAppProc) -> None:
    '''Verifies that cycling through all four metric options only affects the scatter plot and leaves 
    the Top 5 table order, cell values, and metric cards unchanged.
    
    If not/failed, the filter_metric input is incorrectly wired to filtered() instead of being 
    scoped only to scatter_plot, causing unintended re-sorting of top_5 or recalculation of the metric cards.'''
    page.goto(app.url)

    metric = controller.InputSelect(page, "filter_metric")
    top5 = controller.OutputDataFrame(page, "top_5")
    avg_streams = controller.OutputText(page, "card_avg_stream")
    avg_likes = controller.OutputText(page, "card_avg_likes")
    avg_views = controller.OutputText(page, "card_avg_views")

    for m in ["Likes", "Views", "Comments", "Streams"]:
        metric.set(m)

        top5.expect_cell("Tell Em", row=0, col=0, timeout=5000)
        top5.expect_cell("Beautiful Havoc", row=3, col=1, timeout=5000)
        top5.expect_cell("78,913,057", row=4, col=3, timeout=5000)

        avg_streams.expect_value("112,763,800",  timeout=5000)
        avg_likes.expect_value("274,716",  timeout=5000)
        avg_views.expect_value("11,078,490",  timeout=5000)

def test_scatter_plot_has_traces(page: Page, app: ShinyAppProc) -> None:
    '''Scatter plot should render 20 traces (10 features × 1 scatter + 1 trend line) on default load.
    
    If not/failed, either the Plotly widget failed to mount, a feature was dropped from 
    NUMERICAL_FEATURES, or the trend line generation in the scatter_plot render function broke.'''
    #Used Claude and Sonnet 4.6 to write the confirm plotly scatterplot works as intended
    page.goto(app.url)

    plotly_div = page.locator("#scatter_plot .js-plotly-plot")
    plotly_div.wait_for(state="visible", timeout=20000)

    # "Wait until Plotly has finished its internal render and _fullData is populated.
    # wait_for() passing only confirms the element is in the DOM — Plotly's JS
    # render cycle runs after that, so we poll until _fullData is non-empty."
    page.wait_for_function(
        """() => {
            const el = document.querySelector('#scatter_plot .js-plotly-plot');
            return el && el._fullData && el._fullData.length > 0;
        }""",
        timeout=20000
    )

    # Assert exact trace count: 10 features × (1 scatter + 1 trend line) = 20
    trace_count = page.eval_on_selector( 
        "#scatter_plot .js-plotly-plot",
        "el => el._fullData.length"
    )
    assert trace_count == 20