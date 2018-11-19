from . import baseoperationclass
from sklearn.cluster import KMeans
import numpy as np

CLUST_NUM = 3


class KMeansClustering(baseoperationclass.BaseOperationClass):

    _operation_name = 'K-Means Clustering'

    def __init__(self):
        self.clust_numbers = CLUST_NUM
        self.model = None
        self.results = None
        self.cent = None

    def set_parameters(self, clust_numbers):
        if clust_numbers is not None:
            self.clust_numbers = clust_numbers
        return True

    def save_parameters(self):
        return {'cluster_numbers': self.clust_numbers}

    def load_parameters(self, parameters):
        if "cluster_numbers" in parameters and parameters["cluster_numbers"] is not None:
            self.clust_numbers = parameters["cluster_numbers"]
        else:
            self.clust_numbers = CLUST_NUM
        return True

    def save_results(self):
        return {'results': self.results.tolist(), 'cent': self.cent.tolist()}

    def load_results(self, results_dict):
        if 'results' in results_dict and results_dict['results'] is not None:
            self.results = np.array(results_dict['results'])
        if 'cent' in results_dict and results_dict['cent'] is not None:
            self.cent = np.array(results_dict['cent'])
        return True

    def process_data(self, dataset):
        model = KMeans(self.clust_numbers)
        model.fit(dataset)
        self.results = model.predict(dataset)
        self.cent = model.cluster_centers_
        return self.results


try:
    baseoperationclass.register(KMeansClustering)
except ValueError as error:
    print(repr(error))
