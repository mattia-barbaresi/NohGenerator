class Parameters:
    # the thresholds considered when need to add a choreography to the archive
    def __init__(self,
                 repertoire_path,
                 dissim_threshold,
                 number_of_generations,
                 evaluation_method_index,
                 random_seed,
                 fitness_threshold):
        self.full_name = ""
        self.random_seed = random_seed  # type: int
        self.evaluation_method_index = evaluation_method_index  # type: int
        self.number_of_generations = number_of_generations  # type: int
        self.fitness_threshold = fitness_threshold  # type: float
        self.dissim_threshold = dissim_threshold  # type: float
        self.repertoire_path = repertoire_path  # type: basestring
        self.archive = []

    def set_path(self, full_name):
        self.full_name = full_name  # type: basestring
