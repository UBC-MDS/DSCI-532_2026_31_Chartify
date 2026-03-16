"""Chartify: A Shiny dashboard for exploring Spotify/YouTube music data with AI-assisted querying."""
from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from shinywidgets import output_widget, render_plotly
from chatlas import ChatGithub
import querychat
from dotenv import load_dotenv


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from df_filter import filter_data

load_dotenv()


try:
    from . import get_data as gd
except ImportError:
    import get_data as gd

# Load dataset and build sorted artist list for the Dashboard filter dropdown.
df = gd.get_data()
artists = list(df.Artist.unique())
artists.sort()

# Maps UI metric labels to dataframe column names; used by scatter plot and filters.
METRIC_COLUMN_MAP = {
    "Streams": "Stream",
    "Likes": "Likes",
    "Views": "Views",
    "Comments": "Comments",
}

# Audio features plotted in the scatter grid; MinMaxScaler normalizes them for comparison.
NUMERICAL_FEATURES = [
    "Danceability", "Energy", "Loudness", "Speechiness",
    "Acousticness", "Instrumentalness", "Liveness",
    "Valence", "Tempo", "Duration_min",
]

# Human-readable labels for subplot axes and hover tooltips.
FEATURE_DISPLAY_NAMES = {
    "Duration_min": "Song Length",
    "Danceability": "Danceability",
    "Energy": "Energy",
    "Loudness": "Loudness",
    "Speechiness": "Speechiness",
    "Acousticness": "Acousticness",
    "Instrumentalness": "Instrumentalness",
    "Liveness": "Liveness",
    "Valence": "Mood",
    "Tempo": "Tempo",
}

# AI chat client for natural-language queries over the dataset; powers the AI Assistant tab.
qc = querychat.QueryChat(
    df,
    "df",
    client=ChatGithub(model="gpt-4o-mini"),  # free tier model
    greeting="Hi! Ask me anything about this music dataset. Try: 'Show me all songs by Drake' or 'Filter to songs with over 100 million streams'",
)

# Main app UI: navbar with Dashboard (filtered scatter + Top 5) and AI Assistant tabs.
app_ui = ui.page_navbar(

    ui.nav_panel("Dashboard",

        ui.layout_sidebar(

            # Sidebar: artist picker, metric selector, and platform filter.
            ui.sidebar(
                ui.h4("Filters", color='white'),
                ui.input_selectize("artist", 
                               "Select The Artist's Name", 
                               choices=artists, 
                               remove_button=True, 
                               options=(
                                   {
                                        "placeholder": "Enter text"
                                        }
                                   )
                               ),
                ui.input_select("filter_metric", "Metric of Interest",
                                choices=["Streams", "Likes", "Views", "Comments"],
                                selected="Streams"),
                ui.input_radio_buttons("filter_platform", "Platform",
                                    choices=["Spotify", "Youtube", "Both"],
                                    selected="Both"),
                width=300,
                open={"desktop": "open", "mobile": "closed"},
            ),

            # Summary metrics: average streams, likes, and views for the filtered data.
            ui.row(
                ui.column(4, ui.value_box(title="Average Stream Count",
                                        value=ui.output_ui("card_avg_stream"))),
                ui.column(4, ui.value_box(title="Average Like Count",
                                        value=ui.output_ui("card_avg_likes"))),
                ui.column(4, ui.value_box(title="Average View Count",
                                        value=ui.output_text("card_avg_views"))),
            ),

            ui.br(),

            # Top 5 songs by streams; row selection highlights the track in the scatter plot.
            ui.column(12, ui.card(
                ui.div(ui.h4("Top 5 Songs"), style="text-align: center;"),
                ui.output_data_frame("top_5"),
                ui.input_action_button("clear_selection", "Clear selection"),
            )),

            ui.br(),

            # Scatter grid: each subplot shows one audio feature vs selected metric.
            output_widget("scatter_plot", height="1200px"),
        ),
    ),

    # AI Assistant: chat sidebar, box/bar plots of queried data, and downloadable table.
    ui.nav_panel("AI Assistant",
    ui.page_sidebar(
        qc.sidebar(),
        ui.layout_columns(
            ui.card(
                ui.card_header("Musical Feature Distribution"),
                ui.output_plot("box_plot"),
                col_widths=8
            ),
            ui.card(
                ui.card_header("Bar Chart"),
                ui.output_plot("bar_plot"),
                col_widths=4
            ),
            col_widths=[8, 4]
        ),
        ui.layout_columns(
            ui.download_button("export_queried_df", "Download Queried Table as CSV")
        ),
        ui.card(
            ui.card_header("Filtered Chartify Data"),
            ui.output_data_frame("queried_df_tbl")
        ),
        fillable=True,
        ),
    ),

    title="Chartify",

    # Spotify-inspired dark theme: green accents, dark backgrounds, Circular Std font.
    header=ui.tags.style("""
        @import url('https://fonts.googleapis.com/css2?family=Circular+Std&display=swap');

        * { font-family: 'Circular Std', Helvetica, sans-serif; }
        body { background-color: #191414; color: white; }
        .card { background-color: #2a2a2a; border-color: #333333; color: white; }
        .card h4 { color: white; }
        .bslib-value-box {
            background-color: #2a2a2a !important;
            border: 1px solid #1DB954 !important;
            color: white !important;
            text-align: center !important;
        }
        .bslib-value-box .value-box-value,
        .bslib-value-box .value-box-title,
        .bslib-value-box p,
        .bslib-value-box span {
            color: white !important;
            text-align: center !important;
        }
        .bslib-value-box .value-box-showcase {
            background-color: #1DB954 !important;
            color: white !important;
        }
        .form-control { background-color: #2a2a2a; color: white; border-color: #333333; }
        .form-control::placeholder { color: #888888; }

        /* Table header text */
        thead th, .shiny-data-grid thead th {
            color: #000000 !important;
            background-color: #1DB954 !important;
        }
        
        /* Table hover logic*/
         .shiny-data-grid tbody tr:hover {
            background-color: transparent !important;
        }

        .shiny-data-grid tbody tr:hover td {
            background-color: inherit !important;
            color: inherit !important;
            box-shadow: inset 0 1px 0 #1DB954, inset 0 -1px 0 #1DB954;
        }

        /* Selected row - Spotify green instead of blue */
        .shiny-data-grid tbody tr[aria-selected=true],
        .shiny-data-grid tbody tr[aria-selected=true] td {
            background-color: rgba(29, 185, 84, 0.25) !important;
            color: white !important;
        }
                    
        /* Title */
        h1 {
            font-family: 'Circular Std', Helvetica, sans-serif;
            font-weight: 900;
            color: white !important;
            -webkit-text-fill-color: white !important;
        }

        /* Card green outlines */
        .card {
            border: 1px solid #1DB954 !important;
        }
        
        /* Green border on ALL dropdowns/inputs */
        .form-control, .selectize-input, select.form-control {
            border: 1px solid #1DB954 !important;
            background-color: #2a2a2a !important;
            color: white !important;
        }
                    
        /* Fix dropdown background (the select element itself) */
        .shiny-input-select select,
        select {
            background-color: #2a2a2a !important;
            color: white !important;
            border: 1px solid #1DB954 !important;
        }

    
        
        /* Sidebar background */
        .bslib-sidebar-layout > .sidebar {
            background-color: #111111 !important;
                         
        }
                                        
         /* Sidebar collapse toggle */                
        .bslib-sidebar-layout .collapse-toggle {
            color: #1DB954 !important;
            background-color: #111111 !important;
        }
                         
        .bslib-sidebar-layout .collapse-toggle:hover {
            background-color: #1DB954 !important;
            color: black !important;
        }
        
        /* Navbar - black background, white text, Spotify font */
        .navbar {
            background-color: #000000 !important;
        }

        .navbar-brand,
        .navbar .navbar-brand {
            color: white !important;
            font-weight: 900 !important;
            font-size: 1.4rem !important;
        }

        .navbar-nav .nav-link {
            color: #b3b3b3 !important;
        }

        .navbar-nav .nav-link:hover,
        .navbar-nav .nav-link.active {
            color: white !important;
        }

        /* Active tab underline in green */
        .navbar-nav .nav-link.active {
            border-bottom: 2px solid #1DB954 !important;
        }

        /* Filters h4 white */
        .sidebar h4 {
            color: white !important;
        }
        .querychat-sidebar::before,
        .sidebar[data-tab="AI Assistant"]::before {
            content: "ChartBot";
            display: block;
            font-family: 'Circular Std', Helvetica, sans-serif;
            font-weight: 900;
            font-size: 1.8rem;
            color: white;
            padding: 16px 16px 8px 16px;
        }
        .querychat-message.assistant,
        [class*="querychat"] [class*="assistant"] {
            background-color: #2a2a2a !important;
            color: white !important;
            border: 1px solid #1DB954 !important;
            border-radius: 12px !important;
            padding: 10px 14px !important;
        }
        
        /* Chat message bubbles - User */
        .querychat-message.user,
        [class*="querychat"] [class*="user"] {
            background-color: #1DB954 !important;
            color: black !important;
            border-radius: 12px !important;
            padding: 10px 14px !important;
        }

        /* General text visibility in chat */
        [class*="querychat"] p,
        [class*="querychat"] span,
        [class*="querychat"] div {
            color: white !important;
        }

        /* Avatar/icon circle */
        [class*="querychat"] [class*="avatar"],
        [class*="querychat"] svg {
            color: #1DB954 !important;
            border-color: #1DB954 !important;
        }
                         
        /* SQL query code block */
        [class*="querychat"] pre,
        [class*="querychat"] code,
        .querychat-query-box,
        pre code {
            background-color: #1e1e1e !important;
            color: #1DB954 !important;
            border: 1px solid #333333 !important;
            border-radius: 8px !important;
        }

        /* Apply Filter button */
        [class*="querychat"] button,
        .querychat-apply-btn {
            background-color: transparent !important;
            color: #1DB954 !important;
            border: 1px solid #1DB954 !important;
            border-radius: 8px !important;
        }

        [class*="querychat"] button:hover {
            background-color: #1DB954 !important;
            color: black !important;
        }

        /* The card/bubble wrapping the query */
        .querychat-sidebar .card,
        .querychat-sidebar [class*="card"] {
            background-color: #2a2a2a !important;
            border: 1px solid #1DB954 !important;
            color: white !important;
        }

        /* Radio button label visibility */
        .shiny-input-radiogroup label,
        .control-label,
        .radio label { color: white !important; }

        /* Clear selection button - outlined green by default, fully green when clicked */
        #clear_selection {
            background-color: transparent !important;
            color: #1DB954 !important;
            border: 2px solid #1DB954 !important;
            border-radius: 8px !important;
        }
        #clear_selection:hover {
            background-color: rgba(29, 185, 84, 0.2) !important;
            color: #1DB954 !important;
        }
        #clear_selection:active {
            background-color: #1DB954 !important;
            color: black !important;
        }
        
        /* Download Queried Table as CSV button - outlined green by default, fully green when clicked */
        #export_queried_df {
            background-color: #2a2a2a !important;
            color: #1DB954 !important;
            border: 2px solid #1DB954 !important;
            border-radius: 8px !important;
        }
        #export_queried_df:hover {
            background-color: rgba(29, 185, 84, 0.2) !important;
            color: #1DB954 !important;
        }
        #export_queried_df:active {
            background-color: #1DB954 !important;
            color: black !important;
        }
    """),
)


def server(input, output, session):
    """Server logic: reactive data, Dashboard outputs, and AI Assistant integration."""
    qc_vals = qc.server()

    # Reactive dataframe from AI chat; drives the queried table, plots, and CSV export.
    @reactive.calc
    def queried_data():
        return qc_vals.df()

    @render.data_frame
    def queried_df_tbl():
        return queried_data()

    @render.download(filename="chartify_data.csv")
    def export_queried_df():
        yield queried_data().to_csv(index=False)

    # Filters Dashboard data by artist and platform; used by scatter, Top 5, and metric cards.
    @reactive.calc
    def filtered():
        filtered_df = filter_data(df = df,
                            artist_input = input.artist(), 
                            platform_input = input.filter_platform())
        return filtered_df

    # Grid of scatter plots: each audio feature vs selected metric, with trend lines and Top 5 highlight.
    @output
    @render_plotly
    def scatter_plot():
        data = filtered().copy()
        metric_label = input.filter_metric()
        metric_col = METRIC_COLUMN_MAP.get(metric_label, "Stream")

        def empty_fig(message):
            fig = go.Figure()
            fig.add_annotation(text=message, xref="paper", yref="paper",
                               x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="white"))
            fig.update_layout(template="plotly_dark", paper_bgcolor="#191414", plot_bgcolor="#191414")
            return fig
        
        if data.empty or metric_col not in data.columns:
            return empty_fig("No data to display")
        
        if data[metric_col].nunique() < 2:
            return empty_fig(f"No {metric_label} data available for {input.artist()}")

        features_present = [f for f in NUMERICAL_FEATURES if f in data.columns]
        data[features_present] = MinMaxScaler().fit_transform(data[features_present])

        ncols = 3
        nrows = -(-len(features_present) // ncols)
        subplot_titles = [FEATURE_DISPLAY_NAMES.get(f, f) for f in features_present]
        fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=subplot_titles,
                            vertical_spacing=0.08, horizontal_spacing=0.12)

        BRAND_COLORS = [
            "#1DB954", "#FC55FF", "#3FFF00", "#FF7733",
            "#A0D6A0", "#FF6B9D", "#00D4FF", "#FFE135",
            "#FF4500", "#9B59B6"
        ]

        # get selected track from Top 5 table 
        selected_track = None
        try:
            sel = top_5.cell_selection()
            if sel["type"] == "row" and sel.get("rows"):
                top5_data = filtered().sort_values(by=["Stream"], ascending=False).head(5)
                idx = sel["rows"][0]
                if idx < len(top5_data):
                    selected_track = top5_data.iloc[idx]["Track"]
        except Exception:
            pass

        for i, feature in enumerate(features_present):
            row, col = i // ncols + 1, i % ncols + 1
            plot_data = data[[metric_col, feature, "Track"]].dropna()

            # Main scatter with hover showing song title
            fig.add_trace(
                go.Scatter(
                    x=plot_data[metric_col],
                    y=plot_data[feature],
                    mode="markers",
                    marker=dict(
                        color=BRAND_COLORS[i % len(BRAND_COLORS)],
                        size=8,
                        opacity=0.7,
                        line=dict(width=0),
                    ),
                    customdata=plot_data["Track"],
                    hovertemplate="<b>%{customdata}</b><br>" + f"{metric_label}: %{{x:,.0f}}<br>{FEATURE_DISPLAY_NAMES.get(feature, feature)}: %{{y:.3f}}<extra></extra>",
                    name=feature,
                    showlegend=False,
                ),
                row=row, col=col,
            )

            # highlight point for selected track
            if selected_track is not None:
                sel_data = plot_data[plot_data["Track"] == selected_track]
                if not sel_data.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=sel_data[metric_col],
                            y=sel_data[feature],
                            mode="markers",
                            marker=dict(
                                color="#FFFFFF",
                                size=14,
                                opacity=1,
                                line=dict(color="#1DB954", width=3),
                                symbol="circle",
                            ),
                            customdata=sel_data["Track"],
                            hovertemplate="<b>%{customdata}</b> (selected)<br>" + f"{metric_label}: %{{x:,.0f}}<br>{FEATURE_DISPLAY_NAMES.get(feature, feature)}: %{{y:.3f}}<extra></extra>",
                            showlegend=False,
                        ),
                        row=row, col=col,
                    )

            # Trend line
            m, b = np.polyfit(plot_data[metric_col], plot_data[feature], 1)
            x_line = np.linspace(plot_data[metric_col].min(), plot_data[metric_col].max(), 100)
            fig.add_trace(
                go.Scatter(x=x_line, y=m * x_line + b, mode="lines",
                           line=dict(color="white", width=1.2),
                           showlegend=False),
                row=row, col=col,
            )

        fig.update_layout(
            title=dict(
                text=f"Audio Features vs {metric_label}: {input.artist()}",
                font=dict(color="white", family="Circular Std, Helvetica, sans-serif", size=18, weight=900),
                x=0.5,
                xanchor="center",
            ),
            template="plotly_dark",
            paper_bgcolor="#191414",
            plot_bgcolor="#1e1e1e",
            font=dict(color="white"),
            height=320 * nrows,
            margin=dict(t=80, b=150, l=50, r=50),
            autosize=True,
        )
        fig.update_xaxes(tickformat=".2s", tickangle=45, nticks=4,
                        gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="white"))
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="white"))
        return fig

    # Bar chart of song counts by platform (Spotify vs YouTube) for the AI-queried data.
    @output
    @render.plot
    def bar_plot():
        data = queried_data().copy()
        if data.empty or "most_playedon" not in data.columns:
            fig, ax = plt.subplots(figsize=(7, 5), facecolor="#191414")
            ax.text(0.5, 0.5, "No data to display", ha="center", va="center",
                    color="white", fontsize=13)
            ax.set_facecolor("#191414")
            ax.axis("off")
            return fig

        platform_counts = data["most_playedon"].fillna("Unknown").value_counts()
        platforms = ["Spotify", "Youtube"]
        counts = platform_counts.reindex(platforms, fill_value=0)

        fig, ax = plt.subplots(figsize=(7, 5), facecolor="#191414")
        fig.subplots_adjust(left=0.15, right=0.92, top=0.88, bottom=0.12)

        bars = ax.bar(
            platforms,
            counts.values,
            color=["#1DB954", "#FF4500"],
            edgecolor="none",
            width=0.45,
        )

        ax.set_facecolor("#191414")
        ax.set_title("Songs by Platform", color="white", fontsize=14,
                    fontweight="bold", pad=14)
        ax.set_xlabel("Platform", color="#aaaaaa", fontsize=11, labelpad=8)
        ax.set_ylabel("Number of Songs", color="#aaaaaa", fontsize=11, labelpad=8)

        ax.tick_params(axis="both", colors="white", labelsize=11)
        ax.set_xticks(range(len(platforms)))
        ax.set_xticklabels(platforms, fontsize=12, color="white")

        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["left", "bottom"]:
            ax.spines[spine].set_edgecolor("#333333")

        ax.yaxis.set_tick_params(labelcolor="#aaaaaa")
        ax.set_ylim(0, counts.max() * 1.18 if counts.max() > 0 else 10)

        for i, value in enumerate(counts.values):
            ax.text(
                i, value + counts.max() * 0.03,
                f"{value:,}",
                ha="center", va="bottom",
                color="white", fontsize=13, fontweight="bold"
            )

        ax.set_facecolor("#191414")
        return fig

    # Top 5 songs by streams for filtered data; row selection syncs with scatter plot highlight.
    @output
    @render.data_frame
    def top_5():
        df_top5 = filtered()
        df_top5 = df_top5.sort_values(by=['Stream'], ascending=False)
        df_top5 = df_top5.rename(columns={"most_playedon": "Most Played On", "Stream": "Streams"})
        df_top5 = df_top5[['Track', 'Album', 'Most Played On', 'Streams']].iloc[:5]
        df_top5["Streams"] = df_top5["Streams"].apply(lambda x: "{:,.0f}".format(x))
        return render.DataGrid(df_top5, selection_mode="row")

    # Clears the Top 5 table selection when the user clicks "Clear selection".
    @reactive.Effect
    @reactive.event(input.clear_selection)
    async def _():
        await top_5.update_cell_selection(None)

    # Metric cards: average views, streams, and likes for the filtered Dashboard data.
    @output
    @render.text
    def card_avg_views():
        data = filtered()
        if (data["Views"] != 0).any():
            return f"{round(data['Views'].mean(), 0):,.0f}"
        return "0"

    @output
    @render.ui
    def card_avg_stream():
        data = filtered()
        avg = data["Stream"].mean() if (data["Stream"] != 0).any() else 0
        return f"{avg:,.0f}"

    @output
    @render.ui
    def card_avg_likes():
        data = filtered()
        avg = data["Likes"].mean() if (data["Likes"] != 0).any() else 0
        return f"{avg:,.0f}"
    
    # Horizontal boxplot of audio features for the AI-queried data.
    @output
    @render.plot
    def box_plot():
        queried_df = queried_data().copy()
        song_feature = ['Danceability', 'Energy','Loudness', 'Speechiness', 'Acousticness',
                    'Instrumentalness','Liveness', 'Valence', 'Tempo']
        labels = sorted(song_feature)
        BRAND_COLORS = [
            "#1DB954", "#FC55FF", "#3FFF00", "#FF7733",
            "#A0D6A0", "#FF6B9D", "#00D4FF", "#FFE135",
            "#FF4500"
        ]
        boxplot_style = {
            'whiskerprops': {'color': '#D3D3D3'},
            'medianprops': {'color': "#4335FF"},
            'flierprops': {'markerfacecolor': '#778899'},
            'capprops': {'color': '#D3D3D3'}
        }
        color_pairs = dict(zip(song_feature, BRAND_COLORS))
        sorted_color_pairs = {k:v for k, v in sorted(color_pairs.items(), key=lambda item:item[0])}
        if queried_df.empty: # if the AI query returns an empty dataframe populate a No Data To Display Plot.
            fig, ax = plt.subplots(facecolor="#191414")
            ax.text(0.5, 0.5, "No data to display", ha="center", va="center",
                    color="white", fontsize=13)
            ax.set_facecolor("#191414")
            ax.axis("off")
            return fig
                    
        else: # Create a boxplot from the queried dataframe
            queried_df_sorted = queried_df[labels]
            fig_box, ax_box = plt.subplots(facecolor="#191414")
            ax_box.set_facecolor("#1e1e1e")
            tick_labels_display = [FEATURE_DISPLAY_NAMES.get(l, l) for l in labels]
            bplot = ax_box.boxplot(
                queried_df_sorted, 
                patch_artist=True,
                tick_labels=tick_labels_display,
                orientation='horizontal',
                **boxplot_style
                )
            ax_box.tick_params(axis="both", colors="white", labelsize=11)
            plt.gca().invert_yaxis()
            for patch, color in zip(bplot['boxes'], list(sorted_color_pairs.values())):
                patch.set_facecolor(color)
            return fig_box

app = App(app_ui, server)