WIN_FUEL = 30
DRAW_FUEL = 0
LOSE_FUEL = -10

def or_node(fuel, houses_left,path):
    key = (fuel, houses_left)
    if key in path:
        return False
    if fuel < 0:
        return False
    if houses_left == 0:
        return True
    result = and_node(fuel, houses_left,path | {key})
    return result

def and_node(fuel, houses_left,path):
    return (
        or_node(fuel + WIN_FUEL, houses_left - 1,path)
        and or_node(fuel + DRAW_FUEL, houses_left - 1,path)
        and or_node(fuel + LOSE_FUEL, houses_left - 1,path)
    )
def and_or_search(current_fuel, route_cost, house_count):
    fuel_after_route = current_fuel - route_cost
    path = set()
    return or_node(fuel_after_route,house_count,path)
