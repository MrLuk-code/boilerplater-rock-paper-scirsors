#The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[]):
    # Reset history if it's a new match (prev_play is empty)
    if not prev_play:
        opponent_history.clear()
    
    opponent_history.append(prev_play)

    # Strategy configuration: We use a sequence depth of 3 moves to predict the 4th
    n = 3
    
    # Persistent dictionary to store pattern frequencies across moves in a single match
    # We use a default list wrapper or attach it to the function to persist it without changing signature
    if not hasattr(player, "model"):
        player.model = {}
        
    model = player.model
    
    # If it's a brand new match, clear out the model from previous bot matches
    if not prev_play:
        model.clear()

    # Define how to counter each move
    ideal_response = {'R': 'P', 'P': 'S', 'S': 'R'}

    # We need at least enough historical moves to form our tracking history
    if len(opponent_history) <= n:
        return "R"  # Default safe initial move

    # Update the pattern frequencies based on what the opponent actually just played
    # We look at the sequence leading up to the previous move
    last_sequence = "".join(opponent_history[-(n+1):-1])
    actual_next_play = opponent_history[-1]
    
    if last_sequence:
        if last_sequence not in model:
            model[last_sequence] = {'R': 0, 'P': 0, 'S': 0}
        model[last_sequence][actual_next_play] += 1

    # Predict what they will do NEXT based on the current sequence ending at the current moment
    current_sequence = "".join(opponent_history[-n:])
    
    prediction = "R"  # Fallback guess
    if current_sequence in model:
        # Predict the opponent's move with the highest historical frequency for this sequence
        prediction = max(model[current_sequence], key=model[current_sequence].get)
    else:
        # If sequence is unknown, guess based on their global favorite move or default
        prediction = max(set(opponent_history), key=opponent_history.count) if opponent_history else "R"

    # Play the winning counter
    return ideal_response[prediction]
