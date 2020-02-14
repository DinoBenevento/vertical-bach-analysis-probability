class CompositionPosition:


    def __init__(self):
        self.composition = []
        self.positions = []
        self.reps = 0

    def add_composition(self, composition):
        self.composition.append(composition)

    def add_position(self, positions):
        self.positions = positions

    def set_reps(self, reps):
        self.reps = reps
