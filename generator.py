import random
import networkx as nx

SMALL_SIZE_DP = 10_000
MEDIUM_SIZE_DP = 100_000
LARGE_SIZE_DP = 1_000_000

SMALL_SIZE_BNB = 75
MEDIUM_SIZE_BNB = 100
LARGE_SIZE_BNB = 125


class Generator:
    @classmethod
    def _renumber(cls, n, u, v):
        permutation = list(range(1, n + 1))
        random.shuffle(permutation)
        for i in range(len(u)):
            u[i] = permutation[u[i] - 1]
            v[i] = permutation[v[i] - 1]

    @classmethod
    def _linear_tree(cls, n):
        u = []
        v = []
        for i in range(2, n + 1):
            u.append(i)
            v.append(i - 1)
        cls._renumber(n, u, v)
        return u, v

    @classmethod
    def generate_small_dataset(cls):
        return cls._generate_random_tree(
            "./input/dataset-kecil", SMALL_SIZE_DP, SMALL_SIZE_BNB
        )

    @classmethod
    def generate_medium_dataset(cls):
        return cls._generate_random_tree(
            "./input/dataset-medium", MEDIUM_SIZE_DP, MEDIUM_SIZE_BNB
        )

    @classmethod
    def generate_large_dataset(cls):
        return cls._generate_random_tree(
            "./input/dataset-large", LARGE_SIZE_DP, LARGE_SIZE_BNB
        )

    @classmethod
    def _generate_random_tree(cls, name_file, N_DP, N_BNB):
        with open(name_file + "-dp.txt", "w") as f1, open(
            name_file + "-bnb.txt", "w"
        ) as f2:
            G_dp = nx.Graph()
            G_bnb = nx.Graph()

            G_dp.add_nodes_from(range(1, N_DP + 1))
            G_bnb.add_nodes_from(range(1, N_BNB + 1))

            vertices = list(range(2, N_DP + 1))

            random.shuffle(vertices)

            for v in vertices:
                parent = random.randint(1, v)
                G_dp.add_edge(parent, v)
                if parent <= N_BNB and v <= N_BNB:
                    G_bnb.add_edge(parent, v)

            for i in range(1, N_DP + 1):
                f1.write(str(i))
                for ne in G_dp.neighbors(i):
                    f1.write(" " + str(ne))
                f1.write("\n")

            for i in range(1, N_BNB + 1):
                f2.write(str(i))
                for ne in G_bnb.neighbors(i):
                    f2.write(" " + str(ne))
                f2.write("\n")

            return G_dp, G_bnb
