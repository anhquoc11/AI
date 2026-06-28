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


WIN_FUEL = 30
DRAW_FUEL = 0
LOSE_FUEL = -10


memo = {}
def or_node(fuel, houses_left):
    key = ("OR", fuel, houses_left)
    if key in memo:
        return memo[key]
    if fuel < 0:
        memo[key] = False
        return False
    if houses_left == 0:
        memo[key] = True
        return True
    memo[key] = and_node(fuel, houses_left)
    return memo[key]

def and_node(fuel, houses_left):
    key = ("AND", fuel, houses_left)
    if key in memo:
        return memo[key]
    if houses_left == 0:
        memo[key] = fuel >= 0
        return memo[key]

    results = [
        or_node(fuel + WIN_FUEL,houses_left - 1),
        or_node(fuel + DRAW_FUEL,houses_left - 1),
        or_node(fuel + LOSE_FUEL,houses_left - 1)
    ]
    memo[key] = all(results)
    return memo[key]
def and_or_search(current_fuel, route_cost, house_count):
    memo.clear()
    fuel_after_route = current_fuel - route_cost
    return or_node(fuel_after_route,house_count)