def knapsack_forward_checking(items, max_weight):
    best_val = 0
    best_subset = []
    history = []
    
    def fc_search(curr_w, curr_v, curr_sub, remaining_items):
        nonlocal best_val, best_subset
        
        history.append((curr_sub.copy(), curr_w, curr_v, "THINKING"))
        
        if curr_v > best_val:
            best_val = curr_v
            best_subset = curr_sub.copy()
            history.append((curr_sub.copy(), curr_w, curr_v, "RECORD"))
            
        valid_next_items = [item for item in remaining_items if curr_w + item['w'] <= max_weight]
        
        for i, item in enumerate(valid_next_items):
            curr_sub.append(item)
            next_remaining = valid_next_items[i + 1:] 
            fc_search(curr_w + item['w'], curr_v + item['v'], curr_sub, next_remaining)
            curr_sub.pop()
            
    fc_search(0, 0, [], items)
    return best_subset, history