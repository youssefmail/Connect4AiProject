import json

# Read games history
try:
    with open("games_history.json", "r") as file:
        games_history = json.loads(f"[{file.read()}]")
except Exception as e:
    print(f"Error in json file: {e}")


# Now, You can make statistics about Ai players

# ...