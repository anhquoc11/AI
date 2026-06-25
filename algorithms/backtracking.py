def knapsack_backtracking(items, max_weight):
    best_val = 0
    best_subset = []
    history = [] 
    
    def backtrack(index, curr_w, curr_v, curr_sub):
        nonlocal best_val, best_subset
        
        history.append((curr_sub.copy(), curr_w, curr_v, "THINKING"))
        
        if curr_w > max_weight:
            history.append((curr_sub.copy(), curr_w, curr_v, "PRUNED_OVERWEIGHT"))
            return
            
        if index == len(items):
            if curr_v > best_val:
                best_val = curr_v
                best_subset = curr_sub.copy()
                history.append((curr_sub.copy(), curr_w, curr_v, "RECORD"))
            return
        
        backtrack(index + 1, curr_w, curr_v, curr_sub)
        
        curr_sub.append(items[index])
        backtrack(index + 1, curr_w + items[index]['w'], curr_v + items[index]['v'], curr_sub)
        curr_sub.pop() 
        
    backtrack(0, 0, 0, [])
    return best_subset, history