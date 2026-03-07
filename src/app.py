from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from chatlas import ChatAnthropic
import querychat
from dotenv import load_dotenv
load_dotenv()

try:
    from . import get_data as gd
except ImportError:
    import get_data as gd


# Import the dataset
df = gd.get_data()

# Create a list of Artist Names for the ui.input_selectize()
artists = list(df.Artist.unique())
artists.sort() # Sort the list of artists alphabetically

METRIC_COLUMN_MAP = {
    "Streams": "Stream",
    "Likes": "Likes",
    "Views": "Views",
    "Comments": "Comments",
}

NUMERICAL_FEATURES = [
    "Danceability", "Energy", "Loudness", "Speechiness",
    "Acousticness", "Instrumentalness", "Liveness",
    "Valence", "Tempo", "Duration_min",
]



qc = querychat.QueryChat(
    df,
    "df",
    client=ChatAnthropic(model="claude-haiku-4-5-20251001"),
    greeting="Hi! Ask me anything about this music dataset. Try: 'Show me all songs by Drake' or 'Filter to songs with over 100 million streams'",
)



app_ui = ui.page_navbar(

    ui.nav_panel("Dashboard",

        ui.layout_sidebar(

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

            ui.row(
                ui.column(4, ui.value_box(title="Avg. Stream",
                                        value=ui.output_ui("card_avg_stream"))),
                ui.column(4, ui.value_box(title="Avg. Likes",
                                        value=ui.output_ui("card_avg_likes"))),
                ui.column(4, ui.value_box(title="Avg. Views",
                                        value=ui.output_text("card_avg_views"))),
            ),

            ui.br(),

            ui.output_plot("scatter_plot", height="800px"),

            ui.br(),

            ui.column(12, ui.card(ui.h4("Top 5 Songs"), ui.output_data_frame("top_5"))),
        ),
    ),

    ui.nav_panel("AI Assistant",
    ui.page_sidebar(
        qc.sidebar(),
        ui.layout_columns(
            ui.card(
                ui.card_header("Box Plot"),
                ui.p("Box Plot visualization."),
                col_widths=8
            ),
            ui.card(
                ui.card_header("Bar Chart"),
                ui.output_plot("bar_plot"),
                col_widths=4
            ),
            col_widths=[8, 4]
        ),
        ui.card(
            ui.card_header("Filtered Chartify Data"),
            ui.output_data_frame("queried_df_tbl")
        ),
        ui.layout_columns(
            ui.download_button("export_queried_df", "Download as CSV")
        ),
        fillable=True,
        ),
    ),

    title="Chartify",


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
        }
        .bslib-value-box .value-box-value,
        .bslib-value-box .value-box-title,
        .bslib-value-box p,
        .bslib-value-box span {
            color: white !important;
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
    """),
)


def server(input, output, session):

    qc_vals = qc.server()
    # qc_vals.df(), will give filtered df later

    @reactive.calc
    def queried_data():
        return qc_vals.df()
    
    @render.data_frame
    def queried_df_tbl():
        return queried_data()

    @render.download(filename="chartify_data.csv")
    def export_queried_df():
        yield queried_data().to_csv(index=False)

    @reactive.calc
    def filtered():
        artist = input.artist().strip()
        platform = input.filter_platform()
        filtered_df = df[df["Artist"].str.lower() == artist.lower()] if artist else df.copy()
        if platform != "Both":
            filtered_df = filtered_df[filtered_df["most_playedon"] == platform]
        return filtered_df

    @output
    @render.plot
    def scatter_plot():
        data = filtered().copy()
        metric_label = input.filter_metric()
        metric_col = METRIC_COLUMN_MAP.get(metric_label, "Stream")

        if data.empty or metric_col not in data.columns:
            fig, ax = plt.subplots(facecolor="#191414")
            ax.text(0.5, 0.5, "No data to display", ha="center", va="center", color="white")
            ax.set_facecolor("#191414")
            return fig


        features_present = [f for f in NUMERICAL_FEATURES if f in data.columns]
        data[features_present] = MinMaxScaler().fit_transform(data[features_present])

        ncols = 3
        nrows = -(-len(features_present) // ncols)
        fig, axes = plt.subplots(nrows, ncols, figsize=(15, 4 * nrows), facecolor="#191414")
        axes = axes.flatten()

        BRAND_COLORS = [
            "#1DB954", "#FC55FF", "#3FFF00", "#FF7733",
            "#A0D6A0", "#FF6B9D", "#00D4FF", "#FFE135",
            "#FF4500", "#9B59B6"
        ]

        for i, feature in enumerate(features_present):
            ax = axes[i]
            ax.set_facecolor("#1e1e1e")
            plot_data = data[[metric_col, feature]].dropna()
            ax.scatter(plot_data[metric_col], plot_data[feature],
                    color=BRAND_COLORS[i % len(BRAND_COLORS)], alpha=0.7, s=60, edgecolors="none")
            m, b = np.polyfit(plot_data[metric_col], plot_data[feature], 1)
            x_line = np.linspace(plot_data[metric_col].min(), plot_data[metric_col].max(), 100)
            ax.plot(x_line, m * x_line + b, color="white", linewidth=1.2, alpha=0.6)
            ax.set_title(feature, color="white", fontsize=10, fontweight="bold")
            ax.set_xlabel(f"{metric_label} (millions)", color="white", fontsize=8)
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x/1e6:.0f}M"))
            ax.tick_params(colors="white")
            for spine in ax.spines.values():
                spine.set_edgecolor("#1DB954")

        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)

        fig.suptitle(f"Audio Features vs {metric_label}: {input.artist()}",
                    color="white", fontsize=14, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.96])  # leave room for suptitle
        plt.subplots_adjust(hspace=0.5, wspace=0.35)
        return fig

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

    @output
    @render.data_frame
    def top_5():
        df_top5 = filtered()
        df_top5 = df_top5.sort_values(by=['Stream'], ascending = False)
        df_top5 = df_top5.rename(columns={"most_playedon":"Most Played On", "Stream":"Streams"})
        df_top5 = df_top5[['Track', 'Album', 'Most Played On', 'Streams']].iloc[:5]
        df_top5["Streams"] = df_top5["Streams"].apply(lambda x : "{:,.0f}".format(x))
        return render.DataGrid(df_top5)

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


app = App(app_ui, server)