from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import numpy as np
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_labels(label_file):
    """Labels created in model training"""
    label = []
    proto_as_ascii_lines = tf.io.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label


def load_graph(model_file):
    """Graph created in model training"""
    graph = tf.compat.v1.Graph()
    graph_def = tf.compat.v1.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph


def init_classification(t):
    """Compare photos to training data"""
    graph = load_graph(os.path.join(BASE_DIR, 'tmp', 'output_graph.pb'))

    input_name = "import/Placeholder"
    output_name = "import/final_result"
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.compat.v1.Session(graph=graph) as sess:
        results = sess.run(
            output_operation.outputs[0],
            {input_operation.outputs[0]: t},
        )
    results = np.squeeze(results)

    labels = load_labels(os.path.join(BASE_DIR, 'tmp', 'output_labels.txt'))
    print(labels[0], results[0])
    print(labels[1], results[1])
    if (labels[0] == 'hotdogs') and (results[0] > 0.95):
        return True
    elif results[1] > 0.95:
            return True
    return False
