from .training import init_h2o, get_data
from .training import get_trained_model, write_outputs


def train_both_models(model_type):
    """
    Train both Bad Loan and Interest Rate Models
    :param model_type: model_type (currently one of:
    random_forest, gradient_boosting or logistic regression)
    :return:
    """

    init_h2o()

    train, valid = get_data()

    if model_type == "logistic_regression":
        # Logistic regression requires 0 or 1 integer
        # rather than categorical (enum)
        target_variable = "bad_loan"
    else:
        target_variable = "bad_loan_categorical"

    model_name = "BadLoanModel"
    bad_loan_model = get_trained_model(train, valid, model_name,
                                       target_variable, model_type)

    write_outputs(bad_loan_model, model_name, model_type)

    target_variable = "int_rate"
    model_name = "InterestRateModel"
    interest_rate_model = get_trained_model(train, valid, model_name,
                                            target_variable, model_type)

    write_outputs(interest_rate_model, model_name, model_type)
