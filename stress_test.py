from generator import Generator
from dp import min_size_vertex_cover

from branch_and_bound import bnb_main
import networkx as nx


for i in range(10000):
    G_dp, G_bnb = Generator.generate_small_dataset()
    G_dp = G_bnb.copy()

    ans1 = min_size_vertex_cover(G_dp)
    ans2 = bnb_main(G_bnb)
    if ans1 != ans2:
        print("BEDA")
        print(ans1, ans2)
        break
    print(i, ans1, ans2)
