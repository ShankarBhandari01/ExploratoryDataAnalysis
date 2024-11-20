import random
#gloabl method to be used in the game
def log_result(result):
    """print the result in a log format"""
    print(result)
    
# global method to generate random number
def roll_die()-> int:
    """Generate a random number between 1 and 6 (inclusive) to simulate a die roll."""
    return random.randint(1, 6)
# main game class 
class Game_engine:
    # Define the game's attributes
    def __init__(self):
        self.blocks = 0
        self.fouls = 0
        self.rebounds = 0

    def start_free_throw_game_engine(self):
        """
        Start free throw sequence for green, orange and purple colored dice.
        Function return with the resultes ('shooter', 'defender', or 'rebound') based on dice rolls.
        """
        log_result("\n--- Free Throw Attempt ---")
        
        # Shooter rolls the green die
        green_roll = roll_die()
        log_result(f"Shooter rolls the green die: {green_roll}")
        
        if green_roll in [1, 2]:  # Clean basket
            log_result("Clean basket! Shooter scores!")
            return "shooter"
        elif green_roll == 3:  # Miss
            log_result("Miss! Defender scores!")
            return "defender"
        else:  # Shot in progress
            log_result("Shot in progress! Defender rolls next.")
            orange_roll = roll_die()
            log_result(f"Defender rolls the orange die: {orange_roll}")
            
            if orange_roll == 1:  # Block
                self.blocks+=1
                log_result("Block! Defender scores!")
                return "defender"
            elif orange_roll == 2:  # Foul
                self.fouls+=1
                log_result("Foul! Shooter gets a free throw.")
                purple_roll = roll_die()
                return self.start_free_throw_game_engine() # Recursive call
            else:  # Pressure applied
                log_result("Pressure applied! Shooter rolls the purple die.")
                purple_roll = roll_die()
                log_result(f"Shooter rolls the purple die: {purple_roll}")
                
                if purple_roll == 1:  # Basket made
                    log_result("Shooter scores under pressure!")
                    return "shooter"
                elif purple_roll == 2:  # Out of bounds
                    log_result("Out of bounds! Defender scores!")
                    return "defender"
                else:  # Rebound fight
                    self.rebounds+=1
                    log_result("Rebound fight! The play continues.")
                    return self.start_free_throw_game_engine() # Recursive call
                
    # To start a single game , call the start_free_throw_game_engine() method
    def start_game(self, shooter_score = 0, defender_score = 0):
        """
        Start a complete game of HoopShot.
        The first player to reach 5 points wins.
        """
        log_result("Starting a new game of HoopShot!")
        
        self.blocks, self.fouls, self.rebounds = 0, 0, 0
        
        while shooter_score < 5 and defender_score < 5:
            result = self.start_free_throw_game_engine()
            
            if result == "shooter":
                shooter_score += 1
            elif result == "defender":
                defender_score += 1
            log_result(f"Current Score -> Shooter: {shooter_score}, Defender: {defender_score}")
        
        log_result("\n--- Game Over ---")
        log_result(f'{("Shooter wins" if shooter_score == 5 else "Defender wins")}, "blocks": {self.blocks}, "fouls": {self.fouls}, "rebounds": {self.rebounds}')
        return(shooter_score == 5,{"blocks": self.blocks, "fouls": self.fouls, "rebounds": self.rebounds})

    def play_multiple_games_with_stats(self, start_shooter=0, start_defender=0, num_games=100):
        try:
            """Simulates multiple games and aggregates statistics."""
            shooter_wins = 0
            total_stats = {"blocks": 0, "fouls": 0, "rebounds": 0}
            
            if num_games == 0:
                raise ValueError("Number of games can not be zero ! ")

            for _ in range(num_games):
                shooter_won, stats = self.start_game(start_shooter, start_defender)
                shooter_wins += shooter_won
                total_stats["blocks"] += stats["blocks"]
                total_stats["fouls"] += stats["fouls"]
                total_stats["rebounds"] += stats["rebounds"]

            return {
                "Win Probability (Shooter)": (shooter_wins / num_games),
                "Avg Blocks": total_stats["blocks"] / num_games,
                "Avg Fouls": total_stats["fouls"] / num_games,
                "Avg Rebounds": total_stats["rebounds"] / num_games,
            }
        except ValueError as e:
            log_result(f"Error in play_multiple_games_with_stats() method: {e}")
            return None
    
