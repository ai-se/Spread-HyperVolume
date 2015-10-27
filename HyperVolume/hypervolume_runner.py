from hypervolume import InnerHyperVolume

class HyperVolumeContainer():
    def __init__(self, filename, results):
        self.name = filename
        self.dimension = len(results[0])
        self.results = results  # list of list
        self.reference_point = None
        self.hypervolume = None

    def get_reference_point(self):
        if self.reference_point is None:
            dimension = len(self.results[0])
            self.reference_point = [max([result[i] for result in self.results]) for i in xrange(dimension)]
        return self.reference_point

    def set_reference_point(self, reference_point):
        assert(len(reference_point) == self.dimension), \
            "Length of the reference point should be equal to dimension of the problem"
        self.reference_point = reference_point

    def set_hypervolume(self, hypervolume):
        if self.hypervolume is None: self.hypervolume = hypervolume
        else: print "HyperVolume has already been set"

    def get_hypervolume(self):
        return self.hypervolume

    def __str__(self):
        return "Name: " + self.name + " HyperVolume: " + str(self.hypervolume)


def file_reader(filepath, separator=" "):
    from os.path import isfile
    assert(isfile(filepath) == True), "file doesn't exist"
    content = []
    for line in open(filepath, "r"):
        content.append([float(element) for element in line.split(separator) if element != "\n"])
    return content


def HyperVolume(list_result_object):
    """Receives list of  HyperVolumeContainer"""
    # Calculate the reference points: This is for minimization problems only
    dimension = list_result_object[0].dimension
    # find the maximum point of each coordinate and increase it to 150%
    reference_point = [1.5 * max([one.get_reference_point()[i] for one in list_result_object]) for i in xrange(dimension)]

    HV = InnerHyperVolume(reference_point)
    for result_object in list_result_object:
        result_object.hypervolume = HV.compute(result_object.results)
        print result_object


def HyperVolume_wrapper():
    folder_path = "./Pareto_Fronts/"
    from os import listdir
    filenames = [folder_path + file for file in listdir(folder_path)]
    fronts = [HyperVolumeContainer(filename.split("/")[-1], file_reader(filename)) for filename in filenames]
    HyperVolume(fronts)


HyperVolume_wrapper()