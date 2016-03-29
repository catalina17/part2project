import ast
import numpy


if __name__ == '__main__':

    num_genres = 6
    num_test_examples = 60
    num_runs = 21
    num_genres_str = 'six'

    average_confusion_matrix = numpy.zeros((num_genres, num_genres))
    mean_error = 0.0
    z_value = 1.96

    for i in range(num_runs):
        # Read the results for the i-th run
        f = open('eval_runs/' + str(num_genres) + 'genres/' + num_genres_str +
                 '_class_run' + str(i + 1) + '.txt')
        text_data = f.read()
        f.close()

        # Parse the test error
        test_data = text_data[text_data.find('\'test\''): text_data.find(',')]
        error = float(test_data[test_data.find(' ') + 1:])
        mean_error += error

        # Parse the confusion matrix
        text_confusion_matrix = text_data[text_data.find('array(') + 6:
                                          text_data.find('), \'train_loss\'')]
        confusion_matrix = numpy.array(ast.literal_eval(text_confusion_matrix))
        average_confusion_matrix += confusion_matrix

    # Compute overall statistics
    average_confusion_matrix /= num_runs
    mean_error /= num_runs
    half_range = z_value * numpy.sqrt(mean_error * (1.0 - mean_error) / num_test_examples)

    # Confidence interval for the classification error
    print str(mean_error) + " +- " + str(half_range)
    # Averaged confusion matrix between genres
    print average_confusion_matrix * 10.0
