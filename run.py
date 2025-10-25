import sys

TARGET_TYPES = ("A", "B", "C", "D")
DOOR_POSITIONS = (2, 4, 6, 8)
HALLWAY_STOPS = (0, 1, 3, 5, 7, 9, 10)
ENERGY_PER_STEP = {"A": 1, "B": 10, "C": 100, "D": 1000}

def parse_input(lines):
    hallway = tuple(lines[1][1:12])
    room_rows = []
    for row in lines[2:-1]:
        if len(row) >= 11:
            room_rows.append([row[3], row[5], row[7], row[9]])
    depth = len(room_rows)
    rooms = []
    for room_index in range(4):
        column = tuple(room_rows[level][room_index] for level in range(depth))
        rooms.append(column)
    return (hallway, tuple(rooms)), depth

def build_goal(depth):
    hallway = tuple("." for _ in range(11))
    rooms = tuple(tuple(room_type for _ in range(depth)) for room_type in TARGET_TYPES)
    return hallway, rooms

def path_is_clear(hallway, start, finish):
    step = 1 if finish > start else -1
    for position in range(start + step, finish + step, step):
        if hallway[position] != ".":
            return False
    return True


def moves_from_hallway(state, depth):
    hallway, rooms = state
    for hallway_pos, amphipod in enumerate(hallway):
        if amphipod == ".":
            continue
        room_index = TARGET_TYPES.index(amphipod)
        door = DOOR_POSITIONS[room_index]
        if not path_is_clear(hallway, hallway_pos, door):
            continue
        room = rooms[room_index]
        if any(cell not in (".", amphipod) for cell in room):
            continue
        for depth_index in range(depth - 1, -1, -1):
            if room[depth_index] == ".":
                break
        else:
            continue
        steps = abs(hallway_pos - door) + depth_index + 1
        cost = steps * ENERGY_PER_STEP[amphipod]
        new_hallway = list(hallway)
        new_hallway[hallway_pos] = "."
        new_room = list(room)
        new_room[depth_index] = amphipod
        new_rooms = list(rooms)
        new_rooms[room_index] = tuple(new_room)
        yield (tuple(new_hallway), tuple(new_rooms)), cost


def moves_from_rooms(state, depth):
    hallway, rooms = state
    for room_index, room in enumerate(rooms):
        target = TARGET_TYPES[room_index]
        if all(cell in (".", target) for cell in room):
            continue
        for depth_index, amphipod in enumerate(room):
            if amphipod != ".":
                break
        else:
            continue
        door = DOOR_POSITIONS[room_index]
        for hallway_pos in HALLWAY_STOPS:
            if hallway[hallway_pos] != ".":
                continue
            if not path_is_clear(hallway, door, hallway_pos):
                continue
            steps = depth_index + 1 + abs(hallway_pos - door)
            cost = steps * ENERGY_PER_STEP[amphipod]
            new_hallway = list(hallway)
            new_hallway[hallway_pos] = amphipod
            new_room = list(room)
            new_room[depth_index] = "."
            new_rooms = list(rooms)
            new_rooms[room_index] = tuple(new_room)
            yield (tuple(new_hallway), tuple(new_rooms)), cost


MEMO = {}

def minimal_energy(state, depth, goal):
    if state in MEMO:
        return MEMO[state]
    if state == goal:
        return 0
    best = float("inf")
    for next_state, move_cost in moves_from_hallway(state, depth):
        best = min(best, move_cost + minimal_energy(next_state, depth, goal))
    for next_state, move_cost in moves_from_rooms(state, depth):
        best = min(best, move_cost + minimal_energy(next_state, depth, goal))
    MEMO[state] = best
    return best

def solve(lines):
    state, depth = parse_input(lines)
    goal = build_goal(depth)
    MEMO.clear()
    energy = minimal_energy(state, depth, goal)
    return energy

def main():
    lines = [line.rstrip("\n") for line in sys.stdin if line.strip()]
    if not lines:
        return
    print(solve(lines))


if __name__ == "__main__":
    main()