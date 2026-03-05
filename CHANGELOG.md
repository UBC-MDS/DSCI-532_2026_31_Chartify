# [0.2.0] - 2026-02-28
### Added

- App specification `m2_spec.md` file #42 #43 
- Within `m2_spec.md`  added component inventory (#48) and mermaid chart #49
- created `.gitignore` file for extra files created by kagglehub data loaded #44
- Metrics cards displaying average KPI counts #46 #49
- Added 2 Posit Connect Cloud links to readme #57
- Created Chartify brand styling: Spotify green (`#1DB954`) card outlines, table headers, and sidebar border #45
- Circular Std / Helvetica font applied across the dashboard #45
- Dark sidebar background (`#111111`) with green border separator #45
- reactive.cal #44
- Created dropdown menus to select a metric of interest and an artist #44
- Clickable choice box to select platform(s) of interest #47
- Top 5 songs table for artist of choice #55
- Scatter plot grid showing all audio features vs. selected metric, with line of best fit per subplot #51 #54

### Changed
- the data loading process and a get_data.py script #44 #45
- updated requirements.txt #44 #52 #56
- instructions for contributions #57
- From the original sketch with one scatterplot (and all features graphed on it), changed to using a scatterplot grid for Milestone 2 instead. This is due the the single-plot method not working and/or being unreadable.
- The layout of the dashboard has changed from milestone 1 -> 2. It has been significantly minimized due to current time constraints. More information found in the "Layout Changes" section in the Reflection below.
### Fixed
- update app to shiny format #40
### Known Issues
- X-axis labels on scatter subplots can overlap at smaller window sizes
- Value boxes may show `NaN` if artist has no data for a given metric

## Reflection

**Implementation Status**: Core filtering, summary cards, top 5 table, and scatter plot grid are all functional and deployed on Posit Cloud.

### Job Stories Status

- **Fully Implemented**: #1, (platform and artist filter, avg. metric cards), #2 (top 5 songs table, avg. metric cards), #3 (scatter plot of audio features vs. metric)
- **Partially/Mostly Done**: -None-
- **Pending M3**: all -> just for further improvements

### Layout Changes:

The following sketched visuals from Milestone 1 have not been implemented due to time constraints:
 - "Platform and Licensed breakdown"
 - "Singles %%" & "Albums %%"
 - "Song Duration (Avg)"
 - Bar chart of song features (Energy, Loudness, Speechiness etc.)
 - "Song Scope" and "Licensed" radio button filters
 - "Song Feature(s)" dropdown/Search box + Slider
 - "Metric of interest" dropdown/Search box.

These may or may not be incorporated in further future developments.

**Deviations from Plan**: Switched from Plotly to Matplotlib for the scatter plot due to `shinywidgets` incompatibility with the Posit Cloud Shiny version. The original plan called for a single overlaid scatter plot; this was changed to a grid of subplots per feature for clarity.

**Design Rationale**: Chartify brand colors and fonts were applied to align the dashboard with the project identity. Green outlines and dark backgrounds follow the Spotify-inspired palette from the brand guide, and the colours were taken from Spotify's 2023 Wrapped Palette.

**Visualization Best Practices**: Each audio feature is plotted independently to avoid scale distortion. A line of best fit is included per subplot to surface directional trends. X-axis is formatted in human-readable millions.

**Strengths**: Dashboard is responsive to artist and platform filters. Styling is consistent and on-brand. Scatter plot provides feature-level insight per song.

**Limitations**: Small number of data points per artist limits the interpretability of the lines of best fit. Scatter plots are static (no hover/tooltip in matplotlib).

**Future Improvements**: Add interactivity back to scatter plot (e.g. Plotly once shinywidgets compatibility is resolved). Add artist search suggestions/autocomplete. Surface tooltip with song name on hover. Additional components and visualizations such as a bar chart to display the average song feature metrics by artist searched.

# [0.2.0] - 2026-02-21
### Added

- dataset selection discussion found in  issue #1 closed 
- add app description to readme #15 for issue #2
- populate motivation & purpose in Proposal.md #16 for issue #8 
- create section 3: usage scenarios in proposal doc #17 for issue #10
- expand proposal with dataset description section #18 for issue #9 
- add section 4 for proposal.md and EDA notebook #19 for issue #12
- sketch and description #20 for issue #13
- create a skeleton app script #21 for issue #1 & #11 
- expand install instructions + description.md #22 for issue #2 

