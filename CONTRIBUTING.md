# Contributing to Chartify

Thank you for your interest in Chartify! Please read below to learn how to contribute to the project. 

## Development Installation

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
shiny run --reload --launch-browser src/app.py # → http://127.0.0.1:8050

# Optional (but suggested): deactivate environment when done
conda deactivate
```

## Getting Started

Once you have the repository running on your local:
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Add your feature as needed. 
3. See instruction below for instructions for submitting your changes. 


## Guidelines

- Follow [PEP 8](https://pep8.org/) for Python code
- Write clear commit messages
- Add tests for new features
- Update documentation as needed

## Submitting Changes

1. Push to your branch: `git push origin feature/your-feature`
2. Create a Pull Request with a clear description
3. Link any related issues

## Code Review

- A maintainer will review your PR
- Address feedback promptly
- Approved PRs will be merged

## Questions?

Open an issue or contact the maintainers.

Thank you for contributing!
