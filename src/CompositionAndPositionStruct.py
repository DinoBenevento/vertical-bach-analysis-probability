class CompositionPosition:


    def __init__(self):
        #notes
        self.composition = []
        #positions in witch the composition is repeated
        self.positions = []
        #number of occurences
        self.reps = 0

    def add_composition(self, composition):
        self.composition.append(composition)

    def add_position(self, positions):
        self.positions = positions

    def set_reps(self, reps):
        self.reps = reps
