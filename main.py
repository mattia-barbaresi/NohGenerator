from datetime import datetime
from genetic_algorithm.genetic_init import init


if __name__ == "__main__":
    now = datetime.now()
    time_now = now.strftime("%Y%m%d-%H.%M")
    for repertoire_index in [0]:  # range(8):
        for generations in [20, 50]:
            for random_seed in [7,135]:
                for fitness_thresh in [0.2, 0.5, 0.8]:
                    for dissim_thresh in [0.2, 0.5, 0.8]:
                        for evaluation_method in [0,1,2]:  # 0-fitness, 1- novelty, 2-fitness and novelty
                            init(number_of_generations=generations,
                                 repertoire_index=repertoire_index,
                                 evaluation_method_index=evaluation_method,
                                 random_seed=random_seed,
                                 dissim_threshold=dissim_thresh,
                                 fitness_threshold=fitness_thresh)
