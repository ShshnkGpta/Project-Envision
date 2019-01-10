def count_total_calls(n_dict):
    l = 0
    for k, v in n_dict.items():
        l = l + len(v)
    return l
    
def count_daily_calls(n_dict):
    dic = {}
    for k, v in n_dict.items():
        dic[k] = len(v)
    return dic

def pos_calls(n_dict):
    total_pos = 0
    daily_pos_calls = {}
    for date, num in n_dict.items():
        new_pos = 0
        old_pos = total_pos
        for num, key in num.items():
            if key["response"] == "positive":
                total_pos = total_pos + 1
        new_pos = total_pos - old_pos
        daily_pos_calls[date] = new_pos
    
    return total_pos, daily_pos_calls
    
def neg_calls(d1, d2):
    d3 = {}
    for k, v in d1.items():
        d3[k] = [(v - d2.get(k, 0)), d2.get(k,0)]   #returns value if k exists in d2, otherwise 0
    return d3
