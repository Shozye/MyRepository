budgets = []
answer = []
n = int(input())
c = int(input())
for i in range(n):
    b = int(input())
    budgets.append(b)
budgets.sort()
while len(budgets)!=0:
    mean_price = c/len(budgets)
    if budgets[0] >= mean_price:
        answer.append(round(mean_price))
        c -= round(mean_price)
        del budgets[0]
    else:
        answer.append(budgets[0])
        c -= budgets[0]
        del budgets[0]
if c>0:
    print("IMPOSSIBLE")
else:
    answer.sort()
    for i in answer:
        print(i)
