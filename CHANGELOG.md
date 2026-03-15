## \[0.4.0\] - 2026-03-17

### Added

-   <!-- New features, components, tests - one line each. Reference PRs where relevant (e.g. #12). -->

### Changed

-   <!-- Spec or design deviations, and motivation. -->

-   <!-- Feedback items you addressed: "Addressed: <item description> (#<prioritization issue>) via #<PR>" -->

-   Addressed: Documentation and Local Setup - resolved environment naming inconsistency and Windows UnicodeDecodeError (ref #80, source #90) via \#<PR>

### Fixed

-   <!-- Bugs resolved since M3. -->

-   **Feedback prioritization issue link:** #80
- Resolved UnicodeDecodeError on Windows by reactivate `pandas_kwargs` in `get_data.py` with latin-1 encoding and zip compression (ref #80, source #90)
- Fixed environment name mismatch in `environment.yml` to use `chartify` (ref #80, source #90)

### Known Issues

-   <!-- Anything incomplete or broken TAs should be aware of (so it isn't mistaken for unfinished work). -->

### Release Highlight: \[Name of your advanced feature\]

<!-- One short paragraph describing what you built and what it does for the user. -->

-   **Option chosen:** A / B / C / D
-   **PR:** #...
-   **Why this option over the others:** <!-- 1–2 sentences; link to your feature prioritization issue -->
-   **Feature prioritization issue link:** #...

### Collaboration

<!-- Summary of workflow or collaboration improvements made since M3. -->

-   **CONTRIBUTING.md:** <!-- Link to the PR that updated it with your M3 retrospective and M4 norms. -->
-   **M3 retrospective:** <!-- What changed in your workflow after M3 collaboration feedback. -->
-   **M4:** <!-- What you tried or improved this milestone. -->

### Reflection

```{=html}
<!-- Standard (see General Guidelines): what the dashboard does well, current limitations,
     any intentional deviations from DSCI 531 visualization best practices. -->
```

<!-- Trade-offs: one sentence on feedback prioritization - full rationale is in #<issue> and ### Changed above. -->

```{=html}
<!-- Most useful: which lecture, material, or feedback shaped your work most this milestone,
     and anything you wish had been covered. -->
```

# \[0.3.0\] - 2026-03-08

### Added

-   setup chatbot and new dashboard tab for natural and interactable querying #66 for #62
-   table display for chatbot filtered dataset and a download to csv button #68 for #62
-   bar chart of songs by platform type via filtered chatbot dataset #73 for #62
-   "musical feature distribution" (box plot) via filtered chatbot dataset of average song features #74 for #62
-   collapsible feature/toggle for sidebar in both dashboard and AI assistant tabs #65
-   thematic color styling to the "AI Assistant" tab visuals #75

### Changed

-   some UI design choices according to feedback: further mentioned in `fixed` below
-   migrated required packages from `‎environment.yml` into `requirements.txt` with a referance to requirements file #71 for #64 

### Fixed

-   UI table hover, navbar styling, metric card theming #69 for #65
-   modified artist input selection to now be a dropdown #67 for #65

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

-   App specification `m2_spec.md` file #42 #43
-   Within `m2_spec.md` added component inventory (#48) and mermaid chart #49
-   created `.gitignore` file for extra files created by kagglehub data loaded #44
-   Metrics cards displaying average KPI counts #46 #49
-   Added 2 Posit Connect Cloud links to readme #57
-   Created Chartify brand styling: Spotify green (`#1DB954`) card outlines, table headers, and sidebar border #45
-   Circular Std / Helvetica font applied across the dashboard #45
-   Dark sidebar background (`#111111`) with green border separator #45
-   reactive.cal #44
-   Created dropdown menus to select a metric of interest and an artist #44
-   Clickable choice box to select platform(s) of interest #47
-   Top 5 songs table for artist of choice #55
-   Scatter plot grid showing all audio features vs. selected metric, with line of best fit per subplot #51 #54

### Changed

-   the data loading process and a get_data.py script #44 #45
-   updated requirements.txt #44 #52 #56
-   instructions for contributions #57
-   From the original sketch with one scatterplot (and all features graphed on it), changed to using a scatterplot grid for Milestone 2 instead. This is due the the single-plot method not working and/or being unreadable.
-   The layout of the dashboard has changed from milestone 1 -\> 2. It has been significantly minimized due to current time constraints. More information found in the "Layout Changes" section in the Reflection below. 

### Fixed

-   update app to shiny format #40 

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
-   add app description to readme #15 for issue #2
-   populate motivation & purpose in Proposal.md #16 for issue #8
-   create section 3: usage scenarios in proposal doc #17 for issue #10
-   expand proposal with dataset description section #18 for issue #9
-   add section 4 for proposal.md and EDA notebook #19 for issue #12
-   sketch and description #20 for issue #13
-   create a skeleton app script #21 for issue #1 & #11
-   expand install instructions + description.md #22 for issue #2