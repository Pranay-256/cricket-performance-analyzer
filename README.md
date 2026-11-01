# 🏏 T20 Cricket Team Performance Analyzer

A complete cricket analytics dashboard built with **Python, Pandas, NumPy, Matplotlib, Seaborn and Streamlit**. Upload your match data and get batting, bowling, player-level and team-level insights in seconds, with no expensive software and no analytics background needed.

🔗 **Live Demo:** [t20-team-performance-analyzer.streamlit.app](https://t20-team-performance-analyzer.streamlit.app/)

📄 A detailed write-up is available in [`Cricket_Performance_Analyzer_Documentation.pdf`](Cricket_Performance_Analyzer_Documentation.pdf).

---

## ❗ Problem Statement

Cricket is played at every level, but advanced performance analytics is available only at the top of the game. Professional teams use expensive analytical tools and dedicated analysts. The vast majority of players do not have access to anything like this, including:

- **Gully cricket** and friendly matches
- **Turf tournaments** and local leagues
- **Inter-school** and **inter-college** tournaments
- **Small tournaments**, including district-level and state-level competitions

In these settings, players, coaches and associations usually have no access to advanced, costly cricket analytics tools. Performance is judged by memory, personal observation and a quick look at the scorecard. This creates several problems:

- **Subjective evaluation:** a player's contribution is decided by opinion rather than numbers.
- **Unfair awards:** Best Batsman, Best Bowler and Player of the Tournament can be influenced by bias, favouritism or even cheating, because there is no transparent data behind the decision.
- **Incomplete bowling evaluation:** bowlers are judged only by wickets, ignoring how many runs they conceded (economy rate).
- **No consistency tracking:** it is hard to tell who performs well regularly and who has just one good match.
- **Weak strategy planning:** coaches cannot easily see where the team loses wickets, which batting position scores the most, or which role contributes the most, so improving for future matches becomes guesswork.
- **No structured records:** match-to-match comparison is almost impossible without a proper data system.

### 🎯 Aim of the Project

The aim of this project is to provide a **simple, free and easy-to-use analytical tool** that gives these players, coaches and organizers the kind of team analysis that was earlier available only through advanced and expensive tools.

Using this tool:

- **Players and coaches** can analyze their team performance effectively, find strengths and weaknesses, and build better strategies to perform well in future matches.
- **Organizers and associations** can give awards **accurately and fairly**, backed by data, without bias or cheating against any player or in favour of another.
- **Anyone** can get started by filling in a simple template (`.csv` or `.xlsx`) and uploading it, with no coding required.

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Screenshots](#-screenshots)
3. [Features](#-features)
4. [Tech Stack](#-tech-stack)
5. [Dataset Structure](#-dataset-structure)
6. [Data Pipeline](#-data-pipeline)
7. [Analytical Modules](#-analytical-modules)
8. [Repository Structure](#-repository-structure)
9. [How to Run Locally](#-how-to-run-locally)
10. [Version History](#-version-history)
11. [Known Limitations](#-known-limitations)
12. [Future Scope](#-future-scope)
13. [Author](#-author)

---

## 📌 Project Overview

The project began as a Jupyter notebook, where the data validation rules, cleaning, feature engineering and analysis logic were built and tested first. That logic was then converted into a fully interactive Streamlit web application with:

- CSV and Excel upload (single or multiple files)
- Automated data validation with descriptive error messages
- Automated cleaning and feature engineering
- Batting, Bowling, Player and Summary analytics
- Interactive player selection and charts

### 🤖 How It Was Built

- **Notebook (`T20_Cricket_Team_Performance_Analysis.ipynb`):** the raw, unformatted version of the analysis, run on `match_data.csv`. It holds the validation rules, the cleaning steps, the feature engineering (strike rate, economy rate with overs converted to balls, consistency score, batting order and match phase) and every analysis and chart, so the logic can be tested and cross-checked before it goes into the app. It is kept in sync with `app.py`.
- **Dashboard UI (`app.py`):** the Streamlit dashboard UI, including the tabs, KPI cards, charts layout and styling, was created with the help of **Claude AI**. The analytical logic behind it comes from the notebook, and the AI-generated code and outputs were reviewed and validated against it for accuracy.

Each row of the dataset is one player's performance in one match. A ready-made example dataset ([`match_data.csv`](match_data.csv)) and a blank [`template.csv`](template.csv) are included in the repository and can also be downloaded from inside the app.

---

## 📸 Screenshots

### 📊 Dataset Tab

Download the template or example dataset, upload one or more files, and read the validation rules for every column.

![Dataset Tab](images/dataset%20tab.png)

### 🏏 Batting Analytics

Individual runs, runs contribution, runs per match, role-wise runs, strike-rate comparison, batting consistency, total and average runs by batting order, and phase-wise wickets lost.

![Batting Analytics Tab](images/batting%20analytics%20tab.png)

### ⚾ Bowling Analytics

Individual wickets, wickets contribution, wickets per match, role-wise wickets, average wickets by role, economy-rate comparison and bowling consistency.

![Bowling Analytics Tab](images/bowling%20analytics%20tab.png)

### 🎯 Player Analytics

Select any player to see their batting and bowling breakdown match by match, with KPI cards and contribution charts against the team.

![Player Analytics Tab](images/player%20analytics%20tab.png)

### 📋 Summary

Runs and wickets per match, top-performer KPI cards and automated narrative insights for the whole team.

![Summary Tab](images/summary%20tab.png)

### ℹ️ About Section

Project background, objective, tech stack, analytical approach and recent updates.

![About Section](images/about%20section.png)

---

## ✨ Features

### 🏏 Batting Analytics
- Individual runs scored by every player
- Total runs contribution (top 5 batters vs others)
- Player's total runs in each match (select a player)
- Runs contribution by role
- Strike-rate comparison between batsmen and all-rounders (minimum 10 balls faced)
- Batting consistency score
- Total runs and average runs by batting order (top, middle, lower)
- Phase-wise wickets lost (powerplay, middle overs, death overs)

### ⚾ Bowling Analytics
- Individual wickets taken by every bowler
- Total wickets contribution (top 5 bowlers vs others)
- Player's total wickets in each match (select a player)
- Wickets contribution by role
- Average wickets by role
- Economy-rate comparison between bowlers and all-rounders (minimum 2 overs bowled)
- Bowling consistency score

### 🎯 Player Analytics
- Player information: role, matches played and usual batting order
- Batting KPIs: total runs, balls played, strike rate and batting consistency
- Runs and strike rate in each match
- Player's runs contribution in a chosen match
- Player's run contribution against the whole team
- Bowling KPIs: total wickets, overs bowled, economy rate and bowling consistency
- Wickets and economy rate in each match
- Player's wickets contribution in a chosen match and against the whole team

### 📋 Team Summary
- Team runs and wickets in every match
- KPI cards for top run scorer, top wicket taker, best strike rate and best economy rate
- Automated narrative insights for the whole team

### ⚙️ System Features
- `.csv` and `.xlsx` upload support
- Multi-file upload with automatic merging
- Strict validation with clear error messages
- Automated data cleaning and feature engineering
- Cached processing for fast reloads
- Download buttons for the template and example datasets

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **Pandas** | Data cleaning, manipulation and aggregation |
| **NumPy** | Numerical operations |
| **Matplotlib** | Charts and plots |
| **Seaborn** | Statistical and aesthetic visualizations |
| **Streamlit** | Interactive web dashboard |
| **Jupyter Notebook** | Building and validating the analysis logic |
| **Claude AI** | Creating the Streamlit dashboard UI |

---

## 📂 Dataset Structure

Each row represents **one player's performance in one match**.

| Column | Description |
|---|---|
| `Match_No` | Match number (1, 2, 3...). Required. |
| `Player_Name` | Player's name, spelled the same way in every match. Required. |
| `Role` | `batsman`, `bowler`, `all-rounder` or `wicketkeeper` (case does not matter). Blank is filled with the most common role. A wicketkeeper is treated as a batsman. |
| `Batting_Position` | Position from 1 (opener) to 11. Required. |
| `Batting_Start_Over` | Over in which the player came in to bat. Blank only if the player did not bat. |
| `Out_Over` | Over in which the player got out. Blank or `not-out` for a not-out batter. Cannot exceed 20. |
| `Balls_Played` | Balls faced. Blank only if the player did not bat. |
| `Runs_Scored` | Runs scored. Blank only if the player did not bat. |
| `Overs_Bowled` | Overs bowled in `O.B` format (3.4 = 3 overs and 4 balls). Blank or 0 if the player did not bowl. |
| `Runs_Given` | Runs conceded. Must be filled if `Overs_Bowled` is filled. |
| `Wickets_Taken` | Wickets taken. Must be filled if `Overs_Bowled` is filled. |

**Supported formats:** `.csv` and `.xlsx`

---

## 🔄 Data Pipeline

### 1️⃣ Data Loading
Upload one or more `.csv` / `.xlsx` files. Multiple files are merged automatically.

### 2️⃣ Data Validation
The dataset is rejected with a descriptive message if any of these rules is broken:
- `Out_Over` is greater than 20 (T20 only)
- A match has more than 11 players, or the dataset has more than 22 unique players
- Total wickets taken in a single match are more than 10
- `Match_No` or `Batting_Position` is missing
- A row has data but no `Player_Name`
- Batting columns are inconsistent: stats without a start over, a start over without balls or runs, or a start over later than the out over
- Bowling columns are inconsistent: stats without overs, or overs without runs given or wickets

### 3️⃣ Data Cleaning
- `Role` is stripped, lowercased, blanks are filled with the most common role, and `wicketkeeper` becomes `batsman`
- `Out_Over` is converted to numeric (`not-out` becomes blank)
- Blank batting and bowling values are filled with 0

### 4️⃣ Feature Engineering
- **Batted** and **Was_Out** flags
- **Strike Rate** = runs / balls x 100
- **Balls Bowled** (overs in `O.B` format are converted to balls first, so 3.4 overs is not treated as a decimal)
- **Economy Rate** = runs given / overs bowled
- **Batting Order** group: top (positions 1-3), middle (4-7), lower (8-11)
- **Consistency Score** = average / (standard deviation + 1), calculated across matches
- **Match phase** of each wicket: powerplay (up to over 6), middle overs (up to 15), death overs (after 15)

---

## 📊 Analytical Modules

| Module | What it answers |
|---|---|
| **Batting** | Who scores the most? Who scores fastest? Who is consistent? Which batting order scores the most? In which phase does the team lose wickets? |
| **Bowling** | Who takes the most wickets? Who is the most economical? Which role takes the most wickets? Who is consistent? |
| **Player** | How did one particular player perform in every match, and how much did they contribute to the team? |
| **Summary** | What are the key takeaways for the whole team? |

---

## 📁 Repository Structure

```text
cricket-performance-anlayzer/
│
├── .devcontainer/                                   # Dev container configuration
│
├── images/                                          # Screenshots used in this README
│   ├── about section.png
│   ├── batting analytics tab.png
│   ├── bowling analytics tab.png
│   ├── dataset tab.png
│   ├── player analytics tab.png
│   └── summary tab.png
│
├── t20-cricket-team-performance-analysis/
│   ├── app.py                                       # Streamlit application
│   ├── requirements.txt                             # Python dependencies
│   └── T20_Cricket_Team_Performance_Analysis.ipynb  # Raw notebook: validation, cleaning, analysis
│
├── Cricket_Performance_Analyzer_Documentation.pdf   # Detailed project documentation
├── match_data.csv                                   # Example dataset
├── template.csv                                     # Blank template dataset
└── README.md
```

---

## 🚀 How to Run Locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/Pranay-256/cricket-performance-anlayzer.git
   cd cricket-performance-anlayzer
   ```

2. **Install the dependencies**

   ```bash
   pip install -r t20-cricket-team-performance-analysis/requirements.txt
   ```

3. **Run the app from the repository root** (the app reads `template.csv` and `match_data.csv` from there)

   ```bash
   streamlit run t20-cricket-team-performance-analysis/app.py
   ```

4. **Upload your data** in the Dataset tab, press **Confirm Upload**, and explore the other tabs. You can use `match_data.csv` to try it out.

> **Notebook:** `T20_Cricket_Team_Performance_Analysis.ipynb` reads `match_data.csv` from its working directory. Run it from the repository root, or change the path to `../match_data.csv`.

---

## 📌 Version History

### Version 2.1 · 16th September 2026
- Improved data validation rules
- Added the Player Analytics section
- Split batting order runs into Total and Average sections, and added Average Wickets by Role

### Version 2.01 · 18th April 2026
- Improved overall tool user interface
- Improved data validation and cleaning
- Added drop-down expanders for the dataset columns overview and About section
- Improved visualization clarity and chart styling
- Added KPI cards for key performance indicators in the Summary tab
- Improved logic for line charts and runs/wickets contributions
- Organized insights into clear analytical sections
- Fixed bugs and issues

### Version 2.0 · 16th March 2026
- Improved overall tool user interface
- Added support for `.xlsx` dataset uploads
- Enhanced data validation and cleaning
- Added more detailed batting and bowling analytics
- Improved visualization clarity
- Added interactive player performance analysis

### Version 1.0 · 27th February 2026
- Initial release

---

## ⚠️ Known Limitations

- Supports only the T20 format currently
- Maximum 11 players per match and 22 unique players per dataset (upload 2 matches at a time)
- Maximum 10 wickets per match
- No fielding statistics
- No extras tracking

---

## 🔮 Future Scope

- ODI and Test match support
- Opposition team analysis
- Career player profiles
- PDF report export
- Match result correlation analysis

---

## 👨‍💻 Author

**Pranay Jha**, B.Tech in Computer Science and Engineering, learning and exploring Data Science, Data Analytics and Data Visualization.

- 🐙 GitHub: [Pranay-256](https://github.com/Pranay-256)
- 💼 LinkedIn: [Pranay Jha](https://www.linkedin.com/in/pranay-jha-6582a937b/)
