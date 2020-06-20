

lis = ["RIGHT",  "BOTH", 'LEFT', 'RIGHT', 'NO', 'RIGHT', 'NO',  'LEFT', 'RIGHT']
comb = []
stack = []
dp = [0] * len(lis)
if lis[0] == 'NO':
    comb.append([lis[0]])
    lis.pop(0)
dp[0] = [lis[0]]
for i in range(1, len(lis)):
    print(i)
    print(dp)
    print(comb)
    if i == len(lis) - 1 and lis[i] == 'RIGHT':
        comb.append([lis[i]])
        break
    if lis[i] == "NO":
        if dp[i-1][-1] != 'LEFT' or dp[i-1][-1] == 'LEFT' and len(dp[i-1]) == 1:
            comb.append(dp[i-1])
        comb.append([lis[i]])
        dp[i] = [lis[i]]
        if lis[i+1] == 'LEFT':
            comb.append([lis[i+1]])
        if i+1 < len(lis):
            dp[i+1] = [lis[i+1]]
        continue
    if dp[i-1][-1] in ["RIGHT", "BOTH"] and lis[i] == 'LEFT':
        dp[i] = dp[i-1] + [lis[i]]
        comb.append(dp[i])
    if dp[i-1][-1] in ["LEFT", "BOTH", 'RIGHT'] and lis[i] == 'RIGHT':
        dp[i] = [lis[i]]
        comb.append(dp[i-1])
        continue
    if dp[i-1][-1] in ["RIGHT", "BOTH"]:
        dp[i] = dp[i-1] + [lis[i]]

print(comb)

lis = []
for coordinate_y in key_set:
    combine = []
    for shelf in sorted(planogram.mini_planogram_set, key=lambda x: x.coordinate_x):
        if shelf.coordinate_y == coordinate_y:
            combine.append(shelf)
    lis.append(combine)
            # if shelf.combine_direction == "NO":
            #     p_dict[shelf.name] = [shelf]
            #     continue
            # if shelf.combine_direction in ["RIGHT", "BOTH"]:
            #     combine.append(shelf)
            # if shelf.combine_direction == "LEFT":
            #     combine.append(shelf)
            #     # number = ','.join(
            #     #     [shelf.name.split('-', 1)[1].strip() if '-' in shelf.name else shelf.name.split(' ')[-1].strip() for shel in combine])
            #     # key = "".join([shelf.name.split('-', 1)
            #     #                [0], "- ", "[", number, "]"])
            #     key = " - ".join([shel.name for shel in combine])
            #     p_dict[key] = combine
            #     # print(p_dict)
            #     combine = []