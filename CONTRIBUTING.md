# Contributing to Chartify

Thank you for your interest in Chartify! Please read below to learn how to contribute to the project.

## Development Installation

To install the required packages and run the app locally, copy and paste the following code into your terminal.

``` bash
# After opening a terminal:
git clone https://github.com/UBC-MDS/DSCI-532_2026_Group_31_Chartify.git
cd DSCI-532_2026_Group_31_Chartify/

# Optional (but suggested): make a fresh environment
conda env create -f environment.yml
# Activate environment
conda activate chartify

# Optional for Assistant Chat (LLM) tab:
# Copy `.env.example` and remove ".example" to be just `.env`.
# Add the  API key for one of the providers, save and continue the rest of the steps

# Run draft application locally  
shiny run --reload --launch-browser src/app.py # → http://127.0.0.1:8050

# Optional (but suggested): deactivate environment when done
conda deactivate
```

## Getting Started

Once you have the repository running on your local: 1. Create a feature branch: `git checkout -b feature/your-feature` 2. Add your feature as needed. 3. See instruction below for instructions for submitting your changes.

## Guidelines

-   Follow [PEP 8](https://pep8.org/) for Python code
-   Write clear commit messages
-   Add tests for new features
-   Update documentation as needed

## Submitting Changes

1.  Push to your branch: `git push origin feature/your-feature`
2.  Create a Pull Request with a clear description
3.  Link any related issues

## Code Review

-   A maintainer will review your PR
-   Address feedback promptly
-   Approved PRs will be merged

## Questions?

Open an issue or contact the maintainers.

Thank you for contributing!

## Milestone 3 Retrospective

### What went well

-   Consistent progress: We stayed on schedule and successfully shipped all the core features planned for M3
-   Feature Integration: We successfully connected the backend logic to the UI, ensuring dashboard updates correctly when users interact with it
-   Technical Ownership: Each team member took clear responsibility for their own sections (eg querychat, scatterplots, etc) to get them finished

### What can be improved

-   Review History: Some PRs were merged without recorded approvals
-   PR Size Management: While there were some large lines of code (LoC) that were necessary to initialize new features from scratch (eg querychat), we worked on breaking down follow-up updates into smaller pieces
-   Documentation: Some code updates were pushed without corresponding changes to the design specifications docs during M3

### Milestone 4 Collaboration Norms

-   Visible Approvals: At least one team member will review the PR before performing merger. Ideally with a quick comment if possible
-   Balanced Reviewing: We will rotate the PR reviews so that the review workload is shared equally
-   Smaller Updates: After feature initialized, we will try to keep updates small so they are easier for team members to read and check
-   Update Docs: If PR changes how the app works, person making the change will also update the project notes in same PR