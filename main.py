from datetime import datetime
from genetic_algorithm.genetic_init import init

if __name__ == "__main__":
    now = datetime.now()
    time_now = now.strftime("%Y%m%d-%H.%M")
    for repertoire_index in [0,1,2,3,4,5,6,7]:  # for repertoireIndex in [0..7]:
        for generations in [50]:
            for random_seed in [7, 46, 101, 171]:
                for fitness_thresh in [0.5, 0.53, 0.57]:
                    for dissim_thresh in [0.45, 0.5, 0.53, 0.55]:
                        for evaluation_method in [0, 1, 2]:  # 0-fitness, 1- novelty, 2-fitness and novelty
                            init(number_of_generations=generations,
                                 repertoire_index=repertoire_index,
                                 evaluation_method_index=evaluation_method,
                                 random_seed=random_seed,
                                 dissim_threshold=dissim_thresh,
                                 fitness_threshold=fitness_thresh)


