import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load datasets
df = pd.read_csv("deliveries.csv")
df2 = pd.read_csv("matches.csv")

# Data cleaning
df.drop_duplicates(inplace=True)

# Aggregations
top_batsman = df.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False)
top_bowler = df.groupby('bowler')['is_wicket'].sum().sort_values(ascending=False)
best = df2.groupby('winner').size().sort_values(ascending=False)
avg = df2.groupby('id')['season'].first()  # 'match_id' ko 'id' se replace kiya

# Merging for avg score of batsman per season
df = df[['match_id', 'batter', 'batsman_runs']]
df2 = df2.merge(df, left_on='id', right_on='match_id', how="left")  # Merge ko bhi update kiya

# Season-based runs
season_run = df2.groupby(["season", "batter"])['batsman_runs'].sum()

# Season-based avg run
season_avg = season_run.groupby(['season', 'batter']).mean().reset_index()

# Har season ke top batsmen


#provided option to see analytics
print("Choose one option: " \
"(1) Top 10 Batsman" \
"(2) Top 10 Bowlers" \
"(3) Who Wins Most Matches" \
"(4) Top 5 Batsmen's Average High Score All Season")
#take input from user 
user = input("Enter your option: ")
if user == "1" :
    print("Top 10 Batsmen by Total Runs:")
    print(top_batsman.head(10))
    plt.figure(figsize=(12, 6))
    tb = top_batsman.head(10).plot(kind='bar', color='purple')
    plt.title('Top 10 Batsmen by total run')
    plt.xlabel('Batsman')
    plt.ylabel('Number of total Scores')
    plt.xticks(rotation=90)
    for i,v in enumerate(top_batsman.head(10)):
        tb.text(i,v+0.5, str(v), ha='center', va='bottom',fontsize=10, color='red' )
    plt.show()
elif user == "2":
    print("Top 10 bowler by total wickets")
    print(top_bowler.head(10))
    plt.figure(figsize=(10, 6))
    ax = top_bowler.head(10).plot(kind='bar', color='purple')
    plt.title('Top 10 Bowler by wickets')
    plt.xlabel('Bowlers')
    plt.ylabel('Number of total wickets')
    plt.xticks(rotation=90)
    for i, v in enumerate(top_bowler.head(10)):
        ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=10, color='red')
    plt.tight_layout()
    plt.show()
elif user == "3":
    print("Top 5 Teams Who wins most matches")
    print(best.head(5))
    plt.figure(figsize=(10,6))
    bt = best.head(5).plot(kind='bar', color="blue")
    plt.title("5 best team")
    plt.xlabel("Teams")
    plt.ylabel("No. Of Matches")
    plt.xticks(rotation =90)
    for i,v in enumerate(best.head(5)):
        bt.text(i,v+0.5,str(v),ha='center',va="bottom", fontsize=10,color="black")
    plt.tight_layout()
    plt.show()
elif user == "4":
    import math

    # Latest 5 seasons
    latest_seasons = sorted(season_avg['season'].unique())[-5:]

    print("Top 5 Batsmen by Average Score in the Last 5 Seasons:")

    ncols = 2
    nrows = math.ceil(len(latest_seasons) / ncols)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, nrows * 4))
    axes = axes.flatten()

    for idx, season in enumerate(latest_seasons):
        top_batsmen = season_avg[season_avg['season'] == season].sort_values(by='batsman_runs', ascending=False).head(5)
        print(f"\nSeason {season}:\n", top_batsmen)

        ax = axes[idx]
        top_batsmen.plot(kind='bar', x='batter', y='batsman_runs', color='purple', ax=ax, width=0.6)
        ax.set_title(f"Season {season}", fontsize=12)
        ax.set_xlabel("Batsman", fontsize=10)
        ax.set_ylabel("Avg Score", fontsize=10)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=9)

        for i, v in enumerate(top_batsmen['batsman_runs']):
            ax.text(i, v + 3, f"{v:.0f}", ha='center', va='bottom', fontsize=9, color='red')

    # Remove empty subplots (if any)
    for j in range(idx + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
else:
    print("Plese Choose only from option")

