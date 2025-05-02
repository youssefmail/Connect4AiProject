import json

history_file = "games_history.json"

# Read games history
try:
    with open(history_file, "r") as file:
        data = file.read()
        if data[0:2] == ",\n":
            data = data[2:]
        games_history = json.loads(f"[{data}]")
except Exception as e:
    print(f"Error in json file: {e}")


# Now, You can make statistics about Ai players

# ...