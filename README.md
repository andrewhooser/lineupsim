# lineupsim
lineupsim test for streamlit
# ⚾ Baseball Lineup Simulator

This is a Streamlit web app that simulates baseball game outcomes based on uploaded player statistics. It's designed to help coaches, players, and data enthusiasts analyze different lineups using season averages.

---

## 🚀 Features

- Upload Excel files with player batting stats
- Simulate thousands of games
- See average runs per inning
- View game-by-game results and at-bat logs
- Download full results (CSV and Excel)

---

## 📊 Input Format

Upload an Excel file (`.xlsx`) with a sheet named **"Input"**. The required columns are:

- `Player Name`
- `Order` (batting order)
- `AB` (at-bats)
- `K` (strikeouts)
- `1B`, `2B`, `3B`, `HR` (hit types)

Example available in: `Input File.xlsx`

---

## 🧠 Simulation Logic

The simulation blends real player stats with a baseline probability model. Each game consists of 5 innings, and up to 10,000 games can be simulated in a session.

---

## 📦 Installation (for local development)

```bash
git clone https://github.com/YOUR_USERNAME/baseball-lineup-sim.git
cd baseball-lineup-sim
pip install -r requirements.txt
streamlit run lineupsim_app.py
