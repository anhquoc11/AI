def heuristic_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def backtracking_route(start_pos, houses):
    best_route = None
    min_cost = float('inf')
    history = []

    def backtrack(current_pos, unvisited, current_route, current_cost):
        nonlocal best_route, min_cost
        history.append((current_route, "THINKING"))
        if current_cost >= min_cost:
            history.append((current_route, "PRUNED"))
            return
            
        if not unvisited:
            best_route = current_route
            min_cost = current_cost
            history.append((current_route, "RECORD"))
            return
            
        for next_house in unvisited:
            step_cost = heuristic_distance(current_pos, next_house)
            new_unvisited = [h for h in unvisited if h != next_house]
            new_route = current_route + [next_house]
            backtrack(next_house, new_unvisited, new_route, current_cost + step_cost)

    backtrack(start_pos, houses, [], 0)
    return best_route, min_cost, history