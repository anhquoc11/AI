import copy 

def knapsack_forward_checking(items, max_weight):

    best_value = 0
    best_orders = []
    history = []
    n = len(items)
    domains = []
    for i  in range(n):
        if items[i]['w'] <= max_weight: domains.append([0, 1])
        else: domains.append([0])
    def forward(index, current_weight, current_value, selected_orders):
        nonlocal best_value, best_orders, history, domains
        history.append((selected_orders.copy(), current_weight, current_value, "THINKING"))
        if current_value > best_value:
            best_value = current_value
            best_orders = selected_orders.copy()
            history.append((selected_orders.copy(), current_weight, current_value, "RECORD"))
        if index == n:
            return
        forward(index + 1, current_weight, current_value, selected_orders)
        w = items[index]['w']
        v = items[index]['v']
        if len(domains[index]) == 2:
            saved_domains = copy.deepcopy(domains)
            selected_orders.append(items[index])
            for j in range(index + 1, n):
                if 1 in domains[j]:
                    if current_weight + w + items[j]['w'] > max_weight:
                        domains[j] = [0]
            forward(index + 1, current_weight + w, current_value + v, selected_orders)
            selected_orders.pop()
            domains = saved_domains
    forward(0, 0, 0, [])
    return best_orders, history