
# lis = ["RIGHT",  "BOTH", 'LEFT', 'RIGHT', 'NO', 'RIGHT', 'NO',  'LEFT', 'RIGHT']
lis = ['LEFT', 'RIGHT', 'BOTH', 'BOTH', 'LEFT', 'NO', 'NO']
# lis = ["RIGHT",'BOTH',"LEFT","RIGHT","BOTH", 'BOTH','LEFT','NO','BOTH','BOTH']
comb = []
# lis = [['NO'], ["RIGHT", 'BOTH'], ['RIGHT'], ['NO'], ['LEFT'], 'RIGHT', 'RIGHT']
while lis[0] in ["NO", "LEFT"]:
    comb.append([lis[0]])
    lis.pop(0)
if len(lis) == 1:
    comb.append([lis[0]]) 
dp = [0] * len(lis)
dp[0] = [lis[0]]
prune = [1] * len(lis)

for i in range(1, len(lis)):
    if lis[i] == "NO":
        if prune[i-1]:
            comb.append(dp[i-1])
            prune[i-1] = 0
        if dp[i-1] != ['NO']:
            prune[i] = 0
            comb.append([lis[i]])
        dp[i] = [lis[i]]
        if prune[i]:
            comb.append(dp[i])
            prune[i] = 0
    if dp[i-1][-1] in ["RIGHT", "BOTH"] and lis[i] == 'BOTH':
        dp[i] = dp[i-1] + [lis[i]]
        if i == len(lis) - 1:
            comb.append(dp[i])
    if dp[i-1][-1] in ["RIGHT", "BOTH"] and lis[i] == 'LEFT':
        dp[i] = dp[i-1] + [lis[i]]
        if prune[i]:
            comb.append(dp[i])
            prune[i] = 0
    if dp[i - 1][-1] in ['LEFT', 'NO']:
        dp[i] = [lis[i]]
        if i == len(lis) - 1 and prune[i]:
            comb.append(dp[i])
            prune[i] = 0
    if dp[i-1][-1] in ['LEFT', 'NO'] and lis[i] == 'LEFT':
        if prune[i]:
            comb.append([lis[i]])
            prune[i] = 0
    if dp[i-1][-1] in ["RIGHT", "BOTH"] and lis[i] == 'RIGHT':
        dp[i] = [lis[i]]
        if prune[i-1]:
            comb.append(dp[i-1])
            prune[i-1] = 0
    if i == len(lis) - 1 and lis[i] == 'RIGHT' and prune[i]:
        comb.append([lis[i]])


print(comb)