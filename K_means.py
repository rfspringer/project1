import random
import math


def get_random_color():
    """Returns a list of the rgb values for a random color"""
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


def assign_initial_random_means(k):
    """Returns list of k random colors to use as the initial means values"""
    means_list = []
    for color in range(k):
        means_list.append(get_random_color())
    return means_list


def compute_distance(pixel_color, mean_color):
    """Computes and returns linear distance between two colors
    Args:
        pixel_color-- rgb list from pixel in original image
        mean_color-- rgb list of one color from the means list
    """
    return math.sqrt((pixel_color[0] - mean_color[0])**2 +
                     (pixel_color[1] - mean_color[1])**2 + (pixel_color[2] - mean_color[2])**2)


def initialize_mean_assignment():
    """initialize mean assignment and distance to two impossible values"""
    return 500, -100


def update_mean_assignment(distance, color_index, least_distance_so_far, least_distance_index):
    """return least distance and index of best mean of all means checked so far"""
    if distance < least_distance_so_far:
        return distance, color_index
    else:
        return least_distance_so_far, least_distance_index


def get_assignment(pixel, means_list):
    """Finds and returns mean assignment for a given pixel"""
    least_distance_so_far, current_assignment = initialize_mean_assignment()
    for color_index in range(len(means_list)):
        distance = compute_distance(pixel, means_list[color_index])
        least_distance_so_far, current_assignment = \
            update_mean_assignment(distance, color_index, least_distance_so_far, current_assignment)
    return current_assignment


def update_assignments(assignments_list, image, means_list):
    """Gets mean assignment for each pixel in image"""
    for x in range(len(image)):
        for y in range(len(image[0])):
            assignments_list[x][y] = get_assignment(image[x][y], means_list)

    return assignments_list


def initialize_empty_array(image):
    """Returns empty array with the same dimensions as 2d image"""
    return [[0] * len(image[0])] * len(image)


def initialize_assignments(image, means_list):
    """Returns first assignments list"""
    empty_array = initialize_empty_array(image)
    return update_assignments(empty_array, image, means_list)


def update_mean_grouped_list(mean_grouped_list, assignment, image_pixel):
    """Adds pixel to sublist of pixels with same mean"""
    mean_grouped_list[assignment].append(image_pixel)


def group_pixels_by_mean(image, assignments_list, k):
    """Returns list that groups all pixels assigned to the same mean into k sublists"""
    mean_grouped_list = [[] for i in range(k)]
    for x in range(len(assignments_list)):
        for y in range(len(assignments_list[0])):
            update_mean_grouped_list(mean_grouped_list, assignments_list[x][y], image[x][y])
    return mean_grouped_list


def get_averaged_mean(summed_values, num_pixels):
    """Gets new mean by dividing sum of r g b values from each pixel in that mean by total number of pixels in mean
    Args:
        summed_values-- list that contains the sum of r g and b values respectively for all colors assigned to previous mean
        num_pixels-- number of pixels assigned to previous mean
    """
    mean = []
    for summed_color_value in summed_values:
        if summed_color_value:
            mean.append(summed_color_value // num_pixels)
        else:
            mean.append(0)
    return mean


def get_sum_of_pixels(pixels_list):
    """Returns list of length three containing the summed r g and b values of all pixels in a list"""
    temp_sum = [0, 0, 0]
    for individual_color in pixels_list:
        for index in range(3):
            temp_sum[index] += individual_color[index]
    return temp_sum


def add_new_mean(means_list, summed_pixels, colors_in_mean):
    """Adds new mean to means list
    Args:
        means_list-- list to add new mean to
        summed_pixels-- list containing summed r g and b values of all pixels from a previous mean
        colors_in_mean-- list of pixels from previous mean
    """
    mean = get_averaged_mean(summed_pixels, len(colors_in_mean))
    means_list.append(mean)


def get_means_list(grouped_pixel_list):
    """Returns new means list
    Args:
        grouped_pixel_list-- list of pixels grouped into sublist based on what mean they were last assigned to
    """
    new_means_list = []
    for colors_in_mean in grouped_pixel_list:
        summed_pixels = get_sum_of_pixels(colors_in_mean)
        add_new_mean(new_means_list, summed_pixels, colors_in_mean)
    return new_means_list


def update_means_list(image, assignments_list, k):
    """Returns new means list"""
    grouped_pixel_list = group_pixels_by_mean(image, assignments_list, k)
    return get_means_list(grouped_pixel_list)


def optimize_lists(means_list, assignments_list, image, k):
    last_means_list = []
    while last_means_list != means_list:
        last_means_list = means_list[:]
        means_list = update_means_list(image, assignments_list, k)
        assignments_list = update_assignments(assignments_list, image, means_list)
        print(means_list)
        print(assignments_list)
    return means_list, assignments_list


def run_k_means(image, k):
    means_list = assign_initial_random_means(k)
    assignments = initialize_assignments(image, means_list)
    return optimize_lists(means_list, assignments, image, k)


def create_image_from_k_means(means_list, assignments_list):
    new_image = initialize_empty_array(assignments_list)
    for i in range(len(new_image)):
        for j in range(len(new_image[0])):
            x = assignments_list[i][j]
            new_image[i][j] = means_list[x]
    return new_image


def get_image(image, k):
    m, a = run_k_means(image, k)
    return create_image_from_k_means(m, a)
