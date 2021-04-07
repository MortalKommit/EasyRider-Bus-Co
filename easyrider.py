from collections import defaultdict
from itertools import combinations
import json


def count_stops(bus_stops):
    stop_by_id = defaultdict(lambda: defaultdict(list))
    start_stops, transfer_stops, finish_stops, wrong_stops = (set(), set(), set(), set())
    for bus_stop in bus_stops:
        stop_by_id[bus_stop["bus_id"]][bus_stop["stop_type"]].append(bus_stop["stop_name"])
        if len(stop_by_id[bus_stop["bus_id"]]["S"]) > 1 or \
                len(stop_by_id[bus_stop["bus_id"]]["F"]) > 1:
            print(f"There is no start or end stop for the line: {bus_stop['bus_id']}")
            break
        if bus_stop["stop_type"] == "S":
            start_stops.add(bus_stop["stop_name"])
        elif bus_stop["stop_type"] == "F":
            finish_stops.add(bus_stop["stop_name"])

    for stop in stop_by_id.keys():
        if len(stop_by_id[stop]["S"]) == 0 or len(stop_by_id[stop]["F"]) == 0:
            print(f"There is no start or end stop for the line: {stop}")
            break
    else:
        all_stops = []
        for stop in stop_by_id.keys():
            all_stops.append(set((x for a in stop_by_id[stop].values() for x in a)))

        # Take stops 2 at a time
        for stop_combination in combinations(all_stops, 2):
            # | == Union, & == intersection
            transfer_stops |= stop_combination[0] & stop_combination[1]
    for bus_stop in bus_stops:
        if bus_stop["stop_type"] == "O":
            if bus_stop["stop_name"] in start_stops | finish_stops | transfer_stops:
                wrong_stops.add(bus_stop["stop_name"])
    print("On demand stops test:")
    print(f"Wrong stop type: {sorted(wrong_stops)}" if wrong_stops else "OK")


if __name__ == "__main__":
    input_text = input()
    try:
        json_data = json.loads(input_text)
        count_stops(json_data)
    except ValueError:
        print("Decoding JSON failed; invalid JSON")
