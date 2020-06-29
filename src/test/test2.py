
# lis = ["RIGHT",  "BOTH", 'LEFT', 'RIGHT', 'NO', 'RIGHT', 'NO',  'LEFT', 'RIGHT']
# lis = ['NO', 'BOTH','LEFT', 'NO', 'NO', 'NO', 'BOTH',  'RIGHT',  'LEFT', 'NO', 'BOTH', 'BOTH', 'LEFT', 'NO','BOTH']
from dataclasses import dataclass

@dataclass
class Direction:
    combine_direction: str
    name: int


lis = [Direction("RIGHT",1), Direction("BOTH",2),Direction("LEFT",3),Direction("RIGHT",4),Direction("RIGHT",5), Direction("RIGHT",6), Direction("BOTH",7),Direction("LEFT",8)]
comb = []
# lis = [['NO'], ["RIGHT", 'BOTH'], ['RIGHT'], ['NO'], ['LEFT'], 'RIGHT', 'RIGHT']
while lis[0].combine_direction in ["NO", "LEFT"]:
    comb.append([lis[0]])
    lis.pop(0)
if len(lis) == 1:
    comb.append([lis[0]])
dp = [0] * len(lis)
dp[0] = [lis[0]]
prune = [1] * len(lis)

for i in range(1, len(lis)):
    # print(dp)
    if lis[i].combine_direction == "NO":
        if prune[i-1]:
            comb.append(dp[i-1])
            prune[i-1] = 0
        if dp[i-1].combine_direction != ['NO']:
            prune[i] = 0
            comb.append([lis[i]])
        dp[i] = [lis[i]]
        if prune[i]:
            comb.append(dp[i])
            prune[i] = 0
    if dp[i-1][-1].combine_direction in ["RIGHT", "BOTH"] and lis[i].combine_direction == 'BOTH':
        dp[i] = dp[i-1] + [lis[i]]
        if i == len(lis) - 1:
            comb.append(dp[i])
    if dp[i-1][-1].combine_direction in ["RIGHT", "BOTH"] and lis[i].combine_direction == 'LEFT':
        dp[i] = dp[i-1] + [lis[i]]
        if prune[i]:
            comb.append(dp[i])
            prune[i] = 0
    if dp[i - 1][-1].combine_direction in ['LEFT', 'NO']:
        dp[i] = [lis[i]]
        if i == len(lis) - 1 and prune[i]:
            comb.append(dp[i])
            prune[i] = 0
    if dp[i-1][-1].combine_direction in ['LEFT', 'NO'] and lis[i].combine_direction == 'LEFT':
        if prune[i]:
            comb.append([lis[i]])
            prune[i] = 0
    if dp[i-1][-1].combine_direction in ["RIGHT", "BOTH"] and lis[i].combine_direction == 'RIGHT':
        dp[i] = [lis[i]]
        if prune[i-1]:
            comb.append(dp[i-1])
            prune[i-1] = 0
    if i == len(lis) - 1 and lis[i].combine_direction == 'RIGHT' and prune[i]:
        comb.append([lis[i]])


print(comb)