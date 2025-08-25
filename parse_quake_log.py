import re
import json

def parse_log(log_path):
    players = set()
    kills = {}

    with open(log_path) as f:
        for line in f:
            match = re.match(r'.*Kill:.*: (.*) killed (.*) by (.*)', line)
            if match:
                killer, victim, means = match.groups()
                if killer != '<world>':
                    players.add(killer)
                    kills[killer] = kills.get(killer, 0) + 1
                else:
                    # <world> kills: decrease victim's kill count
                    kills[victim] = kills.get(victim, 0) - 1
                if victim != '<world>':
                    players.add(victim)

    return {
        "players": list(players),
        "kills": {player: kills.get(player, 0) for player in players}
    }

if __name__ == "__main__":
    result = parse_log("qgames.log")
    print(json.dumps(result, indent=2))