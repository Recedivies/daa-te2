from generator import Generator
from dp import min_size_vertex_cover
from branch_and_bound import bnb_main


if __name__ == "__main__":
    G_dp, G_bnb = Generator.generate_small_dataset()
    ans1 = min_size_vertex_cover(G_dp)
    ans2 = bnb_main(G_bnb)
    print(f"MVC DP: {ans1}, " f"MVC BnB: {ans2}")

    G_dp, G_bnb = Generator.generate_medium_dataset()
    ans1 = min_size_vertex_cover(G_dp)
    ans2 = bnb_main(G_bnb)
    print(f"MVC DP: {ans1}, " f"MVC BnB: {ans2}")

    G_dp, G_bnb = Generator.generate_large_dataset()
    ans1 = min_size_vertex_cover(G_dp)
    ans2 = bnb_main(G_bnb)
    print(f"MVC DP: {ans1}, " f"MVC BnB: {ans2}")
