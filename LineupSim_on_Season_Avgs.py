import pandas as pd
import random

def run_simulation_from_df(df_input, num_games=1000):
    df_input["Player Name"] = df_input["Player Name"].str.strip().str.upper()
    df_input = df_input.sort_values("Order")

    baseline_probs = {
        "Single": 0.65,
        "Double": 0.08,
        "Triple": 0.01,
        "Home Run": 0.01
    }

    def clear_scored_runners_from_bases(bases, runners_scored):
        return [None if runner in runners_scored else runner for runner in bases]

    batting_order = []
    for _, row in df_input.iterrows():
        ab = row["AB"]
        k = row["K"]
        singles = row["1B"]
        doubles = row["2B"]
        triples = row["3B"]
        hr = row["HR"]
        hits = singles + doubles + triples + hr
        batting_avg = hits / ab if ab > 0 else 0
        strikeout_rate = k / ab if ab > 0 else 0
        soft_out_rate = max(0.0, 1.0 - batting_avg - strikeout_rate)
        actual_probs = {
            "Single": singles / hits if hits > 0 else baseline_probs["Single"],
            "Double": doubles / hits if hits > 0 else baseline_probs["Double"],
            "Triple": triples / hits if hits > 0 else baseline_probs["Triple"],
            "Home Run": hr / hits if hits > 0 else baseline_probs["Home Run"]
        }
        weight = min(ab / 30, 1.0)
        blended_probs = {
            hit: weight * actual_probs.get(hit, 0) + (1 - weight) * baseline_probs[hit]
            for hit in baseline_probs
        }
        batting_order.append({
            "Player Name": row["Player Name"],
            "Batting Average": batting_avg,
            "Strikeout Rate": strikeout_rate,
            "Soft Out Rate": soft_out_rate,
            "Hit Probabilities": blended_probs
        })

    def simulate_at_bat(player):
        roll = random.random()
        if roll < player["Strikeout Rate"]:
            return "Strikeout"
        elif roll < player["Strikeout Rate"] + player["Soft Out Rate"]:
            return "Out"
        roll = random.random()
        cumulative = 0
        for hit, prob in player["Hit Probabilities"].items():
            cumulative += prob
            if roll < cumulative:
                return hit
        return "Single"

    def simulate_simple_game(batting_order):
        batter_index = 0
        inning = 1
        log = []
        inning_scores = []

        while inning <= 5:
            outs = 0
            bases = [None, None, None]
            runs = 0
            max_runs = 5 if inning <= 3 else 10

            while outs < 3:
                player = batting_order[batter_index]
                name = player["Player Name"]
                result = simulate_at_bat(player)
                runners_scored = []

                if result in ["Out", "Strikeout"]:
                    outs += 1
                elif result == "Single":
                    if bases[2]: runners_scored.append(bases[2])
                    if bases[1]:
                        if random.random() < 0.7:
                            runners_scored.append(bases[1])
                            bases[1] = None
                        else:
                            bases[2] = bases[1]
                            bases[1] = None
                    if bases[0]: bases[1] = bases[0]
                    bases[0] = name
                elif result == "Double":
                    if bases[2]: runners_scored.append(bases[2])
                    if bases[1]: runners_scored.append(bases[1])
                    if bases[0]:
                        if random.random() < 0.5:
                            runners_scored.append(bases[0])
                        else:
                            bases[2] = bases[0]
                    bases[0], bases[1] = None, None
                    bases[2] = name
                elif result == "Triple":
                    for runner in bases:
                        if runner: runners_scored.append(runner)
                    bases = [None, None, name]
                elif result == "Home Run":
                    for runner in bases:
                        if runner: runners_scored.append(runner)
                    runners_scored.append(name)
                    bases = [None, None, None]

                bases = clear_scored_runners_from_bases(bases, runners_scored)
                projected_total = runs + len(runners_scored)

                if projected_total >= max_runs:
                    allowed = max_runs - runs
                    runners_scored = runners_scored[:allowed]
                    runs = max_runs
                    log.append({
                        "Inning": inning,
                        "Batter": name,
                        "Result": result + " (capped)",
                        "Runners Scored": ", ".join(runners_scored),
                        "Outs After At-Bat": outs,
                        "Total Runs This Inning": runs
                    })
                    outs = 3
                    break
                else:
                    runs = projected_total
                    log.append({
                        "Inning": inning,
                        "Batter": name,
                        "Result": result,
                        "Runners Scored": ", ".join(runners_scored),
                        "Outs After At-Bat": outs,
                        "Total Runs This Inning": runs
                    })

                batter_index = (batter_index + 1) % len(batting_order)

            inning_scores.append(runs)
            inning += 1

        return inning_scores, pd.DataFrame(log)

    def simulate_multiple_games(batting_order, num_games=1000):
        all_logs = []
        all_game_results = []

        for game_num in range(1, num_games + 1):
            inning_scores, game_log = simulate_simple_game(batting_order)
            total = sum(inning_scores)
            all_game_results.append([game_num] + inning_scores + [total])
            game_log["Game"] = game_num
            all_logs.append(game_log)

        df_log = pd.concat(all_logs, ignore_index=True)
        columns = ["Game"] + [f"Inning {i+1}" for i in range(5)] + ["Total Runs"]
        df_results = pd.DataFrame(all_game_results, columns=columns)
        df_averages = df_results.iloc[:, 1:6].mean().reset_index()
        df_averages.columns = ["Inning", "Average Runs"]

        return df_results, df_averages, df_log

    return simulate_multiple_games(batting_order, num_games)
