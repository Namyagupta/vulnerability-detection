import numpy as np


def get_pattern_feature(name):
    test_total_name_path = 'name.txt'
    pattern_feature_path = "feature_zeropadding/"

    final_pattern_feature_test = []  # pattern feature test
    pattern_feature_test_label_path = "label_by_extractor/"+name

    f_test = open(test_total_name_path, 'r')
    lines = f_test.readlines()
    for line in lines:
        line = line.strip('\n').split('.')[0]
        tmp_feature = np.loadtxt(pattern_feature_path + line + '.txt')
        final_pattern_feature_test.append(tmp_feature)

    for i in range(len(final_pattern_feature_test)):
        final_pattern_feature_test[i] = final_pattern_feature_test[i].tolist()

    return final_pattern_feature_test
