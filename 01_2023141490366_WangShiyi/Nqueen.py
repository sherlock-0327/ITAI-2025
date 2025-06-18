import time  

n = int(input("input number of queens:"))

g = [['.' for _ in range(n)] for _ in range(n)]

col = [False]*n

dg = [False]*(2*n)

udg = [False]*(2*n)

N = 0




def dfs(u):
    global N  #声明 N 为全局变量
    if u == n:
        #打印当前的解
        for row in g:
            print(''.join(row))
        print()
        N += 1  #在找到一个有效解时增加计数
        return
    for y in range(n):
        #检查是否可以放置皇后
        if not col[y] and not dg[y-u+n] and not udg[y+u]:
            col[y] = True
            dg[y-u+n] = True
            udg[y+u] = True
            
            g[u][y] = 'Q'

            dfs(u+1)
            
            #回溯，重置状态
            col[y] = False 
            dg[y-u+n] = False
            udg[y+u] = False
            
            g[u][y] = '.'


if n < 4:
    print("invalid input")
else:
    start_time = time.time()  # 开始时间
    dfs(0)
    print("Total solutions:", N)  #输出解的总数量
    end_time = time.time()    # 结束时间

    print(f"Execution time: {end_time - start_time:.6f} seconds")

