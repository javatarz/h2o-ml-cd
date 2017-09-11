import json
import os
from h2o.estimators import H2ORandomForestEstimator
from h2o.estimators import H2OGeneralizedLinearEstimator
from h2o.estimators import H2OGradientBoostingEstimator


def get_params(name_tag):
    """
    Return the parameters corresponding to the model name tag
    :param name_tag: name tag
    :return:
    """
    this_dir = os.path.dirname(os.path.abspath(__file__))
    directory = "%s/model_parameters" % this_dir
    file_name = "%s/%s_params.json" % (directory, name_tag)
    return json.load(open(file_name, 'r'))


def random_forest_model(name):
    """
    Get the (untrained) Random Forest Model
    :param name: model name, will determine filename
    :return: model
    """
    params = get_params("random_forest")
    return H2ORandomForestEstimator(model_id=name, **params)


def logistic_regression(name):
    """
    Get the Logistic Rregression Model
    :param name: model name, will determine filename
    :return: model
    """
    params = get_params("logistic_regression")
    return H2OGeneralizedLinearEstimator(model_id=name, **params)


def gradient_boosting(name):
    """
    Get the Gradient Boosting Model
    :param name: model name, will determine filename
    :return:
    """
    params = get_params("gradient_boosting")
    return H2OGradientBoostingEstimator(model_id=name, **params)