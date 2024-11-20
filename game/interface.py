from game import Game_engine,log_result;
import pandas as pd
import matplotlib.pyplot as plt
game = Game_engine()

# Test the simulation with two full games
#log_result("\n--- Game 1: Balanced Outcomes ---")
#game.start_game()

log_result("\n--- Game 2: Shooter Dominates ---")
#game.start_game()

# Run in different scenarios
num_games = 100
results_0_0 = game.play_multiple_games_with_stats(0, 0,num_games)
results_3_1_shooter = game.play_multiple_games_with_stats(3, 1,num_games)
results_3_1_defender = game.play_multiple_games_with_stats(1, 3,num_games)

#two visualise the outcome of probabilites results 
if results_0_0 is not None and results_3_1_shooter is not None and results_3_1_defender is not None:
    # generating table 
    df = pd.DataFrame([results_0_0,results_3_1_defender,results_3_1_shooter],
                    columns=['Win Probability (Shooter)'	,'Avg Blocks',	'Avg Fouls',	'Avg Rebounds'],
                    index=['Start 0-0', '3-1 Defender', '3-1 Shooter'])

    df.index.name= 'Scenario'
    log_result(df)
    df.plot(title='Wining probability and stats',ylabel='probability')
    plt.show()