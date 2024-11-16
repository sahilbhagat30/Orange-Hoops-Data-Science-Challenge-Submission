# Orange Hoops Data Science Challenge

Welcome to the Orange Hoops Data Science Challenge! This project is part of a competition organized by the iSchool at Syracuse University, in collaboration with the SU basketball team. The goal is to generate actionable insights and predictive models using data provided by the basketball team.

## Table of Contents

- [Orange Hoops Data Science Challenge](#orange-hoops-data-science-challenge)
  - [Table of Contents](#table-of-contents)
  - [About the Competition](#about-the-competition)
  - [Project Overview](#project-overview)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Code Structure](#code-structure)
  - [Contributing](#contributing)
  - [License](#license)

## About the Competition

- **Why**: Compete for $1000 in cash prizes, gain job-relevant skills, and enhance your CV.
- **What**: A week-long contest to develop a useful predictive model.
- **Who**: Teams of 2 to 4 students from Syracuse University.
- **When**: November 7 to November 14 (registration by November 6).
- **Where**: Virtual participation.

For more details, contact ttulyagi@syr.edu.

## Project Overview

This project involves analyzing basketball data to create predictive models that can provide insights into player performance and game outcomes. The dashboard includes features for injury prediction, muscle imbalance analysis, and performance metrics.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Orange-Hoops-Data-Science-Challenge.git
   cd Orange-Hoops-Data-Science-Challenge
   ```

2. **Install the required packages**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run Injury/Dashboard/Dashboard.py
   ```

## Usage

Once the app is running, navigate through the tabs to explore different aspects of player data:

- **Injury History**: View historical injury data and trends.
- **Muscle Imbalance**: Analyze muscle balance metrics and identify high-risk players.
- **Sessions**: Examine session metrics to understand player workload and performance.
- **Performance**: Review player performance data and predictions.

You can also access the deployed app at [Orange Hoops Data Science Challenge Submission](https://orange-hoops-data-science-challenge-submissiong.streamlit.app/).

## Code Structure

- **Performance/winning_shot_player.ipynb**: Notebook for analyzing and predicting the best player for a winning shot.
  ```python:Performance/winning_shot_player.ipynb
  startLine: 30
  endLine: 555
  ```

- **Injury/Dashboard/muscle_dashboard.py**: Handles muscle imbalance analysis and visualization.
  ```python:Injury/Dashboard/muscle_dashboard.py
  startLine: 1
  endLine: 37
  ```

- **Injury/Dashboard/injury_prediction_dashboard.py**: Manages injury prediction using a machine learning model.
  ```python:Injury/Dashboard/injury_prediction_dashboard.py
  startLine: 1
  endLine: 75
  ```

- **Injury/Dashboard/muscle_dashboard.py**: Handles muscle imbalance analysis and visualization.
  ```python:Injury/Dashboard/muscle_dashboard.py
  startLine: 1
  endLine: 37
  ```

- **Injury/Dashboard/Dashboard.py**: Main entry point for the Streamlit app, setting up the dashboard layout and navigation.
  ```python:Injury/Dashboard/Dashboard.py
  startLine: 1
  endLine: 71
  ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.