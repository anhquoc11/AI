def heuristic_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def forward_checking_route(start_pos, houses, max_fuel):
    best_route = None
    min_cost = float('inf')
    history = [] 

    def fc_search(current_pos, unvisited, current_route, current_cost):
        nonlocal best_route, min_cost
        
        history.append((current_route, "THINKING"))

        if not unvisited:
            if current_cost < min_cost:
                best_route = current_route
                min_cost = current_cost
                history.append((current_route, "RECORD"))
            return
            
        for next_house in unvisited:
            step_cost = heuristic_distance(current_pos, next_house)
            new_cost = current_cost + step_cost
            
            new_unvisited = [h for h in unvisited if h != next_house]
            is_valid = True
            
            for future_house in new_unvisited:
                if new_cost + heuristic_distance(next_house, future_house) > max_fuel:
                    is_valid = False
                    break
            
            new_route = current_route + [next_house]
            if not is_valid:
                history.append((new_route, "PRUNED"))
            elif new_cost >= min_cost:
                history.append((new_route, "PRUNED"))
            else:
                fc_search(next_house, new_unvisited, new_route, new_cost)

    fc_search(start_pos, houses, [], 0)
    return best_route, min_cost, history