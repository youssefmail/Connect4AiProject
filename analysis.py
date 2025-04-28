import json

history_file = "games_history.json"

# Read games history
try:
    with open(history_file, "r") as file:
        games_history = json.loads(f"[{file.read()}]")
except Exception as e:
    print(f"Error in json file: {e}")


# Now, You can make statistics about Ai players

# ...