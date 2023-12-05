from generator import Generator
import psutil
import datetime
import networkx as nx


def dfs(G_dp, dp, src, par):
    dp[src][0] = 0
    dp[src][1] = 1

    for child in G_dp.neighbors(src):
        if child == par:
            continue

        dfs(G_dp, dp, child, src)

        dp[src][0] += dp[child][1]
        dp[src][1] += min(dp[child][1], dp[child][0])


def min_size_vertex_cover(G_dp):
    N = G_dp.number_of_nodes() + 1
    dp = [[0 for j in range(2)] for i in range(N)]

    process = psutil.Process()
    start_time = datetime.datetime.now()

    dfs(G_dp, dp, 1, -1)

    end_time = datetime.datetime.now()
    time_diff = end_time - start_time
    execution_time = time_diff.total_seconds() * 1000
    print(
        f"[DP]: "
        f"Execution time: {execution_time:.1f} ms, "
        f"Memory Usage: {process.memory_info().rss // 1_000_000} MB"  # in MB
    )

    # return minimum size vertex cover
    return min(dp[1][0], dp[1][1])
