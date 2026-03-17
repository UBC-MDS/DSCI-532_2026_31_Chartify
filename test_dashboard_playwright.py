# Running tests:
# python -m pytest test_dashboard_playwright.py -v --browser firefox
from shiny.playwright import controller
from shiny.run import ShinyAppProc
from shiny.pytest import create_app_fixture
from playwright.sync_api import Page

app = create_app_fixture("src/app.py")


def test_default_metric_cards_are_correct(page: Page, app: ShinyAppProc) -> None:
    '''  Each card should contain the values with $NOT artist upon load.
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
     output within the top 5 dataframe. If there isn't this would indicate that something 
    about the reactive calculation and filtered did not work as expected.'''
    page.goto(app.url)

    platform = controller.InputRadioButtons(page, "filter_platform")
    top5 = controller.OutputDataFrame(page, "top_5")

    platform.set("Spotify")
    top5.expect_nrow(5,  timeout=10000)
    top5.expect_cell("Spotify", row=0, col=2, timeout=10000)