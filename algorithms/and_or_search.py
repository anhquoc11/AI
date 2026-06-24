WIN_FUEL = 30
DRAW_FUEL = 0
LOSE_FUEL = -10

DELIVERY_COST = 5

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
        or_node(
            fuel - DELIVERY_COST + WIN_FUEL,
            houses_left - 1
        ),

        or_node(
            fuel - DELIVERY_COST + DRAW_FUEL,
            houses_left - 1
        ),

        or_node(
            fuel - DELIVERY_COST + LOSE_FUEL,
            houses_left - 1
        )
    ]

    memo[key] = all(results)
    return memo[key]


def and_or_search(current_fuel, route_cost, house_count):
    """
    current_fuel : nhiên liệu hiện có

    route_cost : chi phí đường bay dự kiến
                 từ thuật toán tìm đường

    house_count : số nhà cần giao

    True  -> an toàn trong mọi trường hợp

    False -> tồn tại ít nhất 1 nhánh
             khiến drone hết nhiên liệu
    """

    memo.clear()

    fuel_after_route = current_fuel - route_cost

    return or_node(
        fuel_after_route,
        house_count
    )