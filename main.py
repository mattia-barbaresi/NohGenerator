from datetime import datetime

from genetic_algorithm.genetic_init import init

if __name__ == "__main__":
    now = datetime.now()
    time_now = now.strftime("%Y%m%d-%H.%M")
    for random_seed in [100]:  # for random_seed in [100, 330, 42]:
        for generations in [10]:  # for generations in [1000,2000]:
            for evaluation_method in [0,1,2]:  # 0-fitness, 1- novelty, 2-fitness and novelty
                for repertoire_index in [3]:  # for repertoireIndex in [0..7]:
                    for dissim_thresh in [0.55, 0.62]:
                        for fitness_thresh in [0.5, 0.6]:
                            init(number_of_generations=generations,  # generations,
                                 repertoire_index=repertoire_index,  # repertoire_index,
                                 evaluation_method_index=evaluation_method,
                                 random_seed=random_seed,
                                 dissim_threshold=dissim_thresh,
                                 fitness_threshold=fitness_thresh)
