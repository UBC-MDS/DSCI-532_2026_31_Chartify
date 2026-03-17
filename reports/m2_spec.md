# App Specification

### 2.1 Updated Job Stories

| #   | Job Story                                                                                                                                                                         | Status      | Notes |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ----- |
| 1   | When I have to market a new song, I want to know which platform it is likely to perform better on so I can focus my resources.                                                    | Implemented ✅ |       |
| 2   | When I am writing a new song for Youtube, I want to see the most liked/viewed songs on that platform so I can determine what song features are associated with stream popularity. | Implemented ✅ |       |
| 3   | When I am producing a new song, I want to see what song features perform best with specific KPI metrics so I know how to tailor my production process for high performance.       | Implemented ✅ |       |

### 2.2 Component Inventory

| ID                | Type          | Shiny Widget/Renderer      | Depends On                        | Job Story  |
| ----------------- | ------------- | -------------------------- | --------------------------------- | ---------- |
| `filter_platform` | Input         | `ui.input_radio_buttons()` | None                              | #1, #2     |
| `filter_metric`   | Input         | `ui.input_select()`        | None                              | #3         |
| `input_artist`    | Input         | `ui.input_text()`          | None                              | #1, #2, #3 |
| `filtered`        | Reactive calc | `@reactive.calc`           | `input_artist`, `filter_platform` | #1, #2, #3 |
| `card_avg_views`  | Output        | `@render.text`             | `filtered`                        | #2, #3     |
| `card_avg_stream` | Output        | `@render.text`               | `filtered`                      | #1, #2     |
| `card_avg_likes`  | Output        | `@render.text`               | `filtered`                      | #1, #2     |
| `top_5`           | Output        | `@render.data_frame`       | `filtered`                        | #2         |
| `scatter_plot`    | Output        | `@render.plot`             | `filter_metric`, `filtered`       | #3         |
| `queried_data`    | Reactive calc | `@reactive.calc`           | `qc_vals.df()` (QueryChat state)  | AI Assistant |
| `queried_df_tbl`  | Output        | `@render.data_frame`       | `queried_data`                    | AI Assistant |
| `box_plot`        | Output        | `@render.plot`             | `queried_data`                    | AI Assistant |
| `bar_plot`        | Output        | `@render.plot`             | `queried_data`                    | AI Assistant |
| `export_queried_df` | Output      | `@render.download`         | `queried_data`                    | AI Assistant |


### 2.3 Reactivity Diagram

```mermaid
flowchart TD
  In1[/input_artist/] --> F{{filtered_df}}
  In2[/filter_platform/] --> F
  In3[/filter_metric/] --> P1([plot_metric])
  F --> C1([card_avg_views])
  F --> C2([card_avg_stream])
  F --> C3([card_avg_likes])
  F --> T1([table_top5songs])
  F --> P1

  subgraph AI_Assistant["AI Assistant (QueryChat)"]
    QC[/user queries/] --> QD{{queried_data}}
    QD --> T2([queried_df_tbl])
    QD --> EXP([export_queried_df])
    QD --> BOX([box_plot])
    QD --> BAR([bar_plot])
  end
```

### 2.4 Calculation Details

**`filtered`**

- **Depends on:** `input_artist`, `filter_platform`
- **Transformation:** Filters rows to the selected artist and platform. If specific artist is not selected, artist "Beyonce" is set as default. If specific platform is not selected, platform "Both" is set as default.
- **Consumed by:** `card_avg_views`, `card_avg_stream`, `card_avg_likes`, `table_top5songs`, `plot_metric`

**`card_avg_stream`**

- **Depends on:** `filtered`
- **Transformation:** Computes the mean of the `Stream` column from the filtered dataframe. If all values are 0, returns "0". Result is formatted as a comma-separated integer string (e.g. `836,260,550`).
- **Consumed by:** `ui.value_box` (Avg. Stream card)

**`card_avg_likes`**

- **Depends on:** `filtered`
- **Transformation:** Computes the mean of the `Likes` column from the filtered dataframe. If all values are 0, returns "0". Result is formatted as a comma-separated integer string.
- **Consumed by:** `ui.value_box` (Avg. Likes card)

**`card_avg_views`**

- **Depends on:** `filtered`
- **Transformation:** Computes the mean of the `Views` column from the filtered dataframe. If all values are 0, returns "0". Result is formatted as a comma-separated integer string.
- **Consumed by:** `ui.value_box` (Avg. Views card)

**`top_5`**

- **Depends on:** `filtered`
- **Transformation:** Sorts the filtered dataframe by `Stream` descending and selects the top 5 rows. Only the columns `Track`, `Album`, `most_playedon`, and `Stream` are retained and rendered as a `DataGrid`.
- **Consumed by:** Top 5 Songs card table

**`scatter_plot`**

- **Depends on:** `filter_metric`, `filtered`
- **Transformation:** Maps the selected metric label to its column name via `METRIC_COLUMN_MAP`. Drops rows with NaN in the metric column, then melts the filtered dataframe from wide to long format using all available `NUMERICAL_FEATURES` as value variables. Each row in the melted dataframe represents one (song, audio feature) pair, plotted with the metric on the x-axis and feature values on the y-axis, coloured by feature name.
- **Consumed by:** Scatter plot widget

### 2.5 AI Assistant (QueryChat) Components

**`queried_data`**

- **Depends on:** `qc_vals.df()` (QueryChat state driven by user natural-language queries)
- **Transformation:** Returns the dataframe produced by the QueryChat AI assistant based on the user's queries. Applies `MinMaxScaler` to `NUMERICAL_FEATURES` for downstream visualizations.
- **Consumed by:** `queried_df_tbl`, `export_queried_df`, `box_plot`, `bar_plot`

**`queried_df_tbl`**

- **Depends on:** `queried_data`
- **Transformation:** Renders the filtered Chartify dataframe as an interactive `DataGrid` table in the AI Assistant tab. Displays all columns from the queried result set.
- **Consumed by:** "Filtered Chartify Data" card table

**`export_queried_df`**

- **Depends on:** `queried_data`
- **Transformation:** Provides a CSV download of the queried dataframe. Filename: `chartify_data.csv`.
- **Consumed by:** "Download Queried Table as CSV" button

**`box_plot`**

- **Depends on:** `queried_data`
- **Transformation:** Renders a box plot for the musical feature distribution via the queried result set.
- **Consumed by:** `ui.output_plot` ("Musical Feature Distribution")


**`bar_plot`**

- **Depends on:** `queried_data`
- **Transformation:** Renders a bar chart as a breakdown for how many songs are most played on Youtube Vs Spotify via the queried result set.
- **Consumed by:** `ui.output_plot` ("Songs by Platform")