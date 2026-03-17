# \[0.4.0\] - 2026-03-17

### Added

-   Implemented Parquet and DuckDB data loading for improved performance and lazy-loading capabilities for #83 via #<PR>
-   Advanced Feature: Option D: Component click-event interaction - implemented Plotly click-event interactivity on scatterplots and data table for #83 via #95
-   Added testing suite of 3 playwright behaviour tests and 1 pytest unit test for filtering logic for #84 via #100 #101

### Changed

-   Addressed: Improved Readability - updated scatterplot feature titles for better readability for #80 via #95
-   Addressed: Layout Optimization - rearranged graphics on main tab by moving top 5 songs table above the scatterplots for #80 via #95
-   Addressed: Function Documentation - added function level comments throughout app.py for code clarity for #80 via #95
-   Addressed: Documentation and Local Setup - resolved environment naming inconsistency and Windows UnicodeDecodeError for #80 via #96
-   Addressed: Robust Error Handling - implemented plotting logic to prevent SVD convergence errors when there is limited song data for #80 via #96
-   Addressed: Make AI download button more visible - enhanced contrast of data export button for #80 via #97
-   Switched data backend from CSV/Pandas to ibis + DuckDB for database level filtering #83 via #<PR>
-   Spec Docs update: revised specification document m4_spec.md to reflect architectural changes and advanced features for #93 via #<PR>

### Fixed

-   **Feedback prioritization issue link:** #80
-   Resolved critical feedback regarding cross-filtering by enabling click-event interactivity on the scatterplots and data table for #80 via #95
-   Resolved non-critical feedback regarding readability for scatterplots by improving feature titles on each subplot for #80 via #95
-   Fixed non-critical feedback on layout on main tab by rearranging the top 5 songs table to be above the scatterplots for better flow for #80 via #95
-   Resolved critical feedback regarding the UnicodeDecodeError on Windows by reactivating `pandas_kwargs` in `get_data.py` with latin-1 encoding and zip compression for #80 via #96
-   Fixed non-critical feedback regarding environment name mismatch in `environment.yml`, changed from `chartify3` to `chartify` for #80 via #96
-   Resolved critical feedback of "SVD did not converge in Linear Least Squares" in the dashboard by implementing `empty_fig()` in `app.py` to detect low variance in track metrics for #80 via #96
-   Resolved critical visibility issue with "Download Queried Table as CSV" button by applying custom CSS theme to maintain visual consistency across the dashboard for #80 via #97
-   Resolved ba chart title "Songs by Platform" on "AI Assistant" tab no longer get cut off at some aspect ratios/browser dimensions for #80 & #86 via #102
  
### Known Issues

-   chartBot chat window lacks dedicated scrollbar, long conversations extend the whole browser window
-   filtered Chartify dataframe on "AI Assistant" tab window extends longer with every subsequent ChartBot query when sidebar is open. When sidebar is closed, dataframe card is at fixed height
-   returned queried dataframe has and displays far too many decimal points


### Release Highlight: Scatterplot and Data Table Interactivity

We implemented two-way interactivity between "Top 5 Songs" table and scatterplot grid. When a user clicks a specific song in table, the dashboard reacts by highlighting the song across all audio feature plots, allowing for immediate visual comparison of the song's features. The user can also hover over plot points to see specific song details.

-   **Option chosen:** D
-   **PR:** #95
-   **Why this option over the others:** We chose Option D to address peer feedback (#80) regarding the static nature of the dashboard. This also fulfills the requirement for the advanced component-to-component interaction for #83.
-   **Feature prioritization issue link:** #83

### Collaboration

-   **CONTRIBUTING.md:** #81

-   **M3 retrospective: What went well**

    -   Consistent progress: We stayed on schedule and successfully shipped all the core features planned for M3
    -   Feature Integration: We successfully connected the backend logic to the UI, ensuring dashboard updates correctly when users interact with it
    -   Technical Ownership: Each team member took clear responsibility for their own sections (eg querychat, scatterplots, etc) to get them finished

-   **M3 retrospective: What can be improved**

    -   Review History: Some PRs were merged without recorded approvals
    -   PR Size Management: While there were some large lines of code (LoC) that were necessary to initialize new features from scratch (eg querychat), we worked on breaking down follow-up updates into smaller pieces
    -   Documentation: Some code updates were pushed without corresponding changes to the design specifications docs during M3

-   **Milestone 4 Collaboration Norms**

    -   Visible Approvals: At least one team member will review the PR before performing merger. Ideally with a quick comment if possible
    -   Balanced Reviewing: We will rotate the PR reviews so that the review workload is shared equally
    -   Smaller Updates: After feature initialized, we will try to keep updates small so they are easier for team members to read and check
    -   Update Docs: If PR changes how the app works, person making the change will also update the project notes in same PR

### Reflection

The Chartify dashboard now allows both high level artist metrics along with a more granular interactive song analysis. The implementation of click-event interactivity (advanced feature option D) has significantly improved the user experience, turning static scatterplots into more of an exploration tool. Additionally the transition of DuckDB and Parquet ensures that the dashboard app is performing optimally by moving the filter logic to the database level, which also reduces memory overhead.

Current limitations primarily involve UI polishing and data presentation. For example, the Chartbot window lacks a dedicated scrollbar, making long conversations with Chartbot annoying to navigate, and the queried data table currently displays excessive decimal places which clutters the interface.

Regarding feedback prioritization, we focused on critical issues such as backend stability and accessibility over smaller cosmetic issues and nice-haves. The full rationale is in #80 and in the Changed section above. 

The most impactful material in this milestone was in lecture 7 on "Databases in Shiny" for performance optimization. Being able to use the Parquet + ibis + DuckDb combo provided a clear framework on how to build scalable Shiny applications. While we were able to create and apply our custom CSS theming, some more in-depth material on CSS customization and dashboard theming would have been helpful.

# \[0.3.0\] - 2026-03-08

### Added

-   setup chatbot and new dashboard tab for natural and interactable querying for #62 via #66
-   table display for chatbot filtered dataset and a download to csv button for #62 via #68
-   bar chart of songs by platform type via filtered chatbot dataset #62 via #73
-   "musical feature distribution" (box plot) via filtered chatbot dataset of average song features for #62 via #74
-   collapsible feature/toggle for sidebar in both dashboard and AI assistant tabs #65 via #69
-   thematic color styling to the "AI Assistant" tab visuals #75 via #69

### Changed

-   some UI design choices according to feedback: further mentioned in `fixed` below for #65 via #67 #69
-   migrated required packages from `environment.yml` into `requirements.txt` with a referance to requirements file for #64 via #71

### Fixed

-   UI table hover, navbar styling, metric card theming for #65 via #69
-   modified artist input selection to now be a dropdown for #65 via #67

### Known Issues

-   X-axis labels on scatter subplots can overlap at smaller window sizes
-   chartBot chat window lacks dedicated scrollbar, long conversations extend the whole browser window
-   filtered Chartify dataframe on LLM tab window extends longer with every subsequent ChartBot query
-   returned queried dataframe has and displays far too many decimal points
-   bar chart title on "AI Assistant" tab may get cut off at some aspect ratios/browser dimensions

### Reflection

At this stage, we have successfully implemented the QueryChat chatbot that has a natural language interface, allowing for a more conversational approach to data exploration. This new feature allows the users to ask complex questions regarding the Spotify dataset such as "show me high energy and danceability songs on Spotify" and see the resulting visualization and table in real-time. We have also successfully addressed Milestone 2's feedback by applying proper theming to the metric cards and fixed the contrast and colors of some elements to improve the accessibility of the interface.

We decided on an intentional deviation from the original Milestone 3 proposal: the transition from violin plots to box plots on the LLM tab. During development we realized that the density of audio metrics were too sparse when filtering the dataframe, which yielded no meaningful kernel density estimations. Following 531 visualization best practices, we pivoted to box plots so as to avoid misleading thin lines/shapes that occur in low density violin plots.

Current limitations include the small number of data points per artist which limits the interpretability of lines of best fit, the lack of a dedicated scrollbar for ChartBot's chat window, and a lack of fixed height for the queried dataframe. Our planned improvements for future milestones include the addition of interactivity to the scatterplot charts, a surface tooltip with a song name on hover, and implementing fixed-height containers for ChartBot's chat window as well as the associated filtered dataframe.

# \[0.2.0\] - 2026-02-28

### Added

-   App specification `m2_spec.md` file via #42 #43
-   Within `m2_spec.md` added component inventory via #48 and mermaid chart via #49
-   created `.gitignore` file for extra files created by kagglehub data loaded via #44
-   Metrics cards displaying average KPI counts via #46 #49
-   Added 2 Posit Connect Cloud links to readme via #57
-   Created Chartify brand styling: Spotify green (`#1DB954`) card outlines, table headers, and sidebar border via #45
-   Circular Std / Helvetica font applied across the dashboard via #45
-   Dark sidebar background (`#111111`) with green border separator via #45
-   reactive.calc via #44
-   Created dropdown menus to select a metric of interest and an artist via #44
-   Clickable choice box to select platform(s) of interest via #47
-   Top 5 songs table for artist of choice via #55
-   Scatter plot grid showing all audio features vs. selected metric, with line of best fit per subplot via #51 #54

### Changed

-   the data loading process and a get_data.py script via #44 #45
-   updated requirements.txt via #44 #52 #56
-   instructions for contributions via #57
-   From the original sketch with one scatterplot (and all features graphed on it), changed to using a scatterplot grid for Milestone 2 instead. This is due the the single-plot method not working and/or being unreadable.
-   The layout of the dashboard has changed from milestone 1 -\> 2. It has been significantly minimized due to current time constraints. More information found in the "Layout Changes" section in the Reflection below.

### Fixed

-   update app to shiny format via #40

### Known Issues

-   X-axis labels on scatter subplots can overlap at smaller window sizes
-   Value boxes may show `NaN` if artist has no data for a given metric

### Reflection

**Implementation Status**: Core filtering, summary cards, top 5 table, and scatter plot grid are all functional and deployed on Posit Cloud.

### Job Stories Status

-   **Fully Implemented**: #1, (platform and artist filter, avg. metric cards), #2 (top 5 songs table, avg. metric cards), #3 (scatter plot of audio features vs. metric)
-   **Partially/Mostly Done**: -None-
-   **Pending M3**: all -\> just for further improvements

### Layout Changes:

The following sketched visuals from Milestone 1 have not been implemented due to time constraints: - "Platform and Licensed breakdown" - "Singles %%" & "Albums %%" - "Song Duration (Avg)" - Bar chart of song features (Energy, Loudness, Speechiness etc.) - "Song Scope" and "Licensed" radio button filters - "Song Feature(s)" dropdown/Search box + Slider - "Metric of interest" dropdown/Search box.

These may or may not be incorporated in further future developments.

**Deviations from Plan**: Switched from Plotly to Matplotlib for the scatter plot due to `shinywidgets` incompatibility with the Posit Cloud Shiny version. The original plan called for a single overlaid scatter plot; this was changed to a grid of subplots per feature for clarity.

**Design Rationale**: Chartify brand colors and fonts were applied to align the dashboard with the project identity. Green outlines and dark backgrounds follow the Spotify-inspired palette from the brand guide, and the colours were taken from Spotify's 2023 Wrapped Palette.

**Visualization Best Practices**: Each audio feature is plotted independently to avoid scale distortion. A line of best fit is included per subplot to surface directional trends. X-axis is formatted in human-readable millions.

**Strengths**: Dashboard is responsive to artist and platform filters. Styling is consistent and on-brand. Scatter plot provides feature-level insight per song.

**Limitations**: Small number of data points per artist limits the interpretability of the lines of best fit. Scatter plots are static (no hover/tooltip in matplotlib).

**Future Improvements**: Add interactivity back to scatter plot (e.g. Plotly once shinywidgets compatibility is resolved). Add artist search suggestions/autocomplete. Surface tooltip with song name on hover. Additional components and visualizations such as a bar chart to display the average song feature metrics by artist searched.

# \[0.1.0\] - 2026-02-21

### Added

-   dataset selection discussion found in issue #1 closed
-   add app description to readme for issue #2 via #15
-   populate motivation & purpose in Proposal.md for issue #8 via #16
-   create section 3: usage scenarios in proposal doc for issue #10 via #17
-   expand proposal with dataset description section for issue #9 via #18
-   add section 4 for proposal.md and EDA notebook for issue #12 via #19
-   sketch and description for issue #13 via #20
-   create a skeleton app script for issue #1 & #11 via #21
-   expand install instructions + description.md for issue #2 via #22
