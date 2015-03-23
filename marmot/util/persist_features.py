# persist features to file
# feature output formats are different depending upon the datatype
# if it's an ndarray, write to .csv
# if it's an list of lists, write to crf++ format, with a separate file containing the feature names
# if it's a dict, write to .json or pickle the object(?), write the feature names to a separate file
import os, errno
import pandas as pd
import numpy as np
import logging

from marmot.experiment.import_utils import list_of_lists

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger('experiment_logger')


# TODO: make sure to check the type of the features
def persist_features(dataset_name, features, persist_dir, tags=None, feature_names=None):
    '''
    persist the features to persist_dir -- use dataset_name as the prefix for the persisted files
    :param dataset_name:
    :param features:
    :param persist_dir:
    :param feature_names:
    :return:
    '''
    try:
        os.makedirs(persist_dir)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(persist_dir):
            pass
        else:
            raise

#    print "FEATURES", features[0][0]
#    print "NAMES", feature_names
    # for the 'plain' datatype
    if type(features) == np.ndarray and features.shape[1] == len(feature_names):
        output_df = pd.DataFrame(data=features, columns=feature_names)
        output_path = os.path.join(persist_dir, dataset_name + '.csv')
        output_df.to_csv(output_path, index=False)
        logger.info('saved features in: {} to file: {}'.format(dataset_name, output_path))

    # for the 'sequential' datatype
    elif list_of_lists(features):
        output = open(dataset_name + '.crf', 'w')
        if tags is not None:
            assert(len(features) == len(tags)), "Different numbers of tag and feature sequences"
            for s_idx, (seq, tag_seq) in enumerate(zip(features, tags)):
                assert(len(seq) == len(tag_seq)), "Lengths of tag and feature sequences don't match in sequence %d" % s_idx
                for w_idx, (feature_list, tag) in enumerate(zip(seq, tag_seq)):
                    assert(len(feature_list) == len(feature_names)), "Wrong number of features in sequence %d, word %d" % (s_idx, w_idx)
                    tag = str(tag)
                    feature_str = []
                    for f in feature_list:
                        if type(f) == unicode:
                            feature_str.append(f.encode('utf-8'))
                        else:
                            feature_str.append(str(f))
                    feature_str = '\t'.join(feature_str)
                    output.write('%s\t%s\n' % (feature_str, tag))
                output.write("\n")
        else:
            for s_idx, seq in enumerate(features):
                for w_idx, feature_list in enumerate(seq):
                    assert(len(seq) == len(feature_names)), "Wrong number of features in sequence %d, word %d" % (s_idx, w_idx)
                    feature_str = []
                    for f in feature_list:
                        if type(f) == unicode:
                            feature_str.append(f.encode('utf-8'))
                        else:
                            feature_str.append(str(f))
                    feature_str = '\t'.join(feature_str)
                    output.write('%s\n' % feature_str.encode('utf-8'))
                output.write("\n")
        output_features = open(dataset_name + '.features', 'w')
        for f_name in feature_names:
            output_features.write("%s\n" % f_name.encode('utf-8'))
        output.close()
        output_features.close()
