from __future__ import division


def spread_calculator(obtained_front, extreme_point1, extreme_point2):
    """Given a Pareto front `first_front` and the two extreme points of the
    optimal Pareto front, this function returns a metric of the diversity
    of the front as explained in the original NSGA-II article by K. Deb.
    The smaller the value is, the better the front is.
    """

    def euclidean_distance(list1, list2):
        assert(len(list1) == len(list2)), "The points don't have the same dimension"
        distance = sum([(i - j) ** 2 for i, j in zip(list1, list2)]) ** 0.5
        assert(distance >= 0), "Distance can't be less than 0"
        return distance

    def closest(obtained_front, point, distance=euclidean_distance):
        """Returns the point from obtained_front which is closed to point"""
        from sys import maxint
        closest_point = None
        min_distance = maxint
        for opoint in obtained_front:
            temp_distance = distance(opoint, point)
            if temp_distance < min_distance:
                min_distance = temp_distance
                closest_point = opoint
        assert(closest_point is not None), "closest_point cannot be None"
        return closest_point, min_distance

    _, df = closest(obtained_front, extreme_point1)
    _, dl = closest(obtained_front, extreme_point2)

    distances = [euclidean_distance(obtained_front[i], obtained_front[i+1]) for i in xrange(len(obtained_front) -1)]
    distances_mean = sum(distances)/len(distances)
    d_variance = sum([abs(di - distances_mean) for di in distances])
    N = len(obtained_front)

    return (df + dl + d_variance)/(df + dl + (N -1) * distances_mean)


def file_reader(filepath, separator=" "):
    from os.path import isfile
    assert(isfile(filepath) == True), "file doesn't exist"
    content = []
    for line in open(filepath, "r"):
        content.append([float(element) for element in line.split(separator) if element != "\n"])
    return content


def sort_list_of_list(list_of_list):
    """ This function is to extract the extreme points"""
    def sorting_def(list):
        number_of_objectives = len(list)
        weights = reversed([10 ** i for i in xrange(number_of_objectives)])
        return sum([element * weight for element, weight in zip(list, weights)])
    return sorted(list_of_list, key=sorting_def)


def spread_calculator_wrapper():
    true_pf_folder = "./True_PF/"
    obtained_pf_folder = "./Obtained_PF/"

    # Fetching the files from the folders True_PF and Obtained_PF
    from os import listdir
    true_pf_files = [true_pf_folder + name for name in listdir(true_pf_folder)]
    obtained_pf_files = [obtained_pf_folder + name for name in listdir(obtained_pf_folder)]

    algorithm_names = [name.split("_")[0] for name in listdir(obtained_pf_folder)]
    model_name = [name.split("_")[1] for name in listdir(obtained_pf_folder)]

    assert(len(model_name) > 0), "Please check the folder ./Obtained_PF/"
    assert(len(set(model_name)) == 1), "The utility cannot handle more than one model at a time"

    model_name = model_name[-1]

    temp_obtained_pf_files = [name for name in listdir(true_pf_folder)]
    true_frontier_exists = False

    # Checking if the True frontier is available for the tool
    for true_pf_file in temp_obtained_pf_files:
        if model_name == true_pf_file.split("_")[0]:
            true_frontier_exists = True
            true_frontier_file = true_pf_folder + true_pf_file

    # Finding contents of the obtained PF files
    contents = []
    for obtained_pf_file in obtained_pf_files: contents.append(file_reader(obtained_pf_file))

    if true_frontier_exists is True:
        true_pf_content = file_reader(true_frontier_file)
        sorted_true_pf_content = sort_list_of_list(true_pf_content)
        # If frontier exists then uses the extreme points from the True frontier
        first_extreme_solution = sorted_true_pf_content[0]
        second_extreme_solution = sorted_true_pf_content[-1]
    else:
        flatten_content = [e1 for item in contents for e1 in item]
        sorted_obtained_pf_content = sort_list_of_list(flatten_content)
        # If frontier doesn't exist calculate the extreme points from the available obtained PF
        first_extreme_solution = sorted_obtained_pf_content[0]
        second_extreme_solution = sorted_obtained_pf_content[-1]

    for algorithm_name, content in zip(algorithm_names, contents):
        spread = spread_calculator(sort_list_of_list(content), first_extreme_solution, second_extreme_solution)
        print "Name: ", algorithm_name, " Spread: ", round(spread, 3)

spread_calculator_wrapper()
