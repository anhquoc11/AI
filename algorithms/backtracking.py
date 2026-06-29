def knapsack_backtracking(items, max_weight):
    best_value = 0
    best_orders = []
    history = [] 
    
    def backtrack(index, current_weight, current_value, selected_orders):
        nonlocal best_value, best_orders
        
        history.append((selected_orders.copy(), current_weight, current_value, "THINKING"))
        
        if current_weight > max_weight:
            history.append((selected_orders.copy(), current_weight, current_value, "PRUNED_OVERWEIGHT"))
            return
            
        if index == len(items):
            if current_value > best_value:
                best_value = current_value
                best_orders = selected_orders.copy()
                history.append((selected_orders.copy(), current_weight, current_value, "RECORD"))
            return
        
        backtrack(index + 1, current_weight, current_value, selected_orders)
        
        selected_orders.append(items[index])
        backtrack(index + 1, current_weight + items[index]['w'], current_value + items[index]['v'], selected_orders)
        selected_orders.pop() 
        
    backtrack(0, 0, 0, [])
    return best_orders, history