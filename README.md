# Group 31

## Chartify: Spotify Dashboard Analytics


## Users

Chartify is a data analytics dashboard that leverages Spotify's song features dataset to uncover patterns and characteristics of successful songs. Below is a small preview of it's features and how to interact with it: 
![](img/demo.gif)

Built for music producers and A&R professionals, it provides actionable insights on tempo, energy, danceability, and other key metrics that correlate with chart performance and cross-platform popularity. The main goal of this to to help   stakeholders make data-driven decisions in hit song production.

The main and stable deployment of this dashboard can be found here: https://019c9724-a466-7485-646d-fe85536777ee.share.connect.posit.cloud/ 

## Contributing

As the developments are being made to the dashboard, a preview can be found here: 
https://019c9725-ef1f-1b27-7dae-b8159ce8ad33.share.connect.posit.cloud/

If you are interested in contributing to this dashboard, please review the [CONTRIBUTING.md](CONTRIBUTING.md) document for more information on:
- Development environment installation
- How to submit changes or feature additions
- Development guidelines

By contributing to the project you accept and agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

### Quick-Start Setup Instructions:

To install the required packages and run the app locally, copy and paste the following code into your terminal.

```bash
# After opening a terminal:
git clone https://github.com/UBC-MDS/DSCI-532_2026_Group_31_Chartify.git
cd DSCI-532_2026_Group_31_Chartify/

# Optional (but suggested): make a fresh environment
conda env create -f environment.yml
# Activate environment
conda activate chartify

# Run draft application locally  
python src/app.py # → http://127.0.0.1:8050

# Optional (but suggested): deactivate environment when done
conda deactivate
```

