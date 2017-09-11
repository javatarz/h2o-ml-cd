import h2o
import os
import sys
from h2o.estimators import H2ORandomForestEstimator


def init_h2o():
    """
    Start up H2o
    """
    h2o.init(nthreads=-1)


def get_data():
    """
    Get the training and validation data
    :return:
    """
    loan_csv = "{}/data/loan.csv".format("" if len(sys.argv) == 0 else sys.argv[1])
    loans = h2o.import_file(loan_csv)

    print("Import approved and rejected loan requests...")

    loans["bad_loan"] = loans["bad_loan"].asfactor()

    train, valid, test = loans.split_frame([0.79, 0.2], seed=1234)
    return train, valid


def train_bad_loan_model(train, valid):
    """
    Train the Bad Loan model
    :param train: training frame
    :param valid: validation frame
    :return:
    """

    # Prepare predictors and response columns
    target_variable = "bad_loan"

    input_variables = ["loan_amnt", "longest_credit_length", "revol_util",
                       "emp_length", "home_ownership", "annual_inc",
                       "purpose", "addr_state", "dti", "delinq_2yrs",
                       "total_acc", "verification_status", "term"]

    model = H2ORandomForestEstimator(
        ntrees=100,
        max_depth=5,
        stopping_tolerance=0.01,  # 10-fold increase in threshold as defined in rf_v1
        stopping_rounds=2,
        score_each_iteration=True,
        model_id="BadLoanModel",
        seed=2000000
    )
    model.train(input_variables, target_variable,
                training_frame=train, validation_frame=valid)

    print(model)
    gini = model.gini(valid=True)
    print("Bad loan Gini coefficient: %s" % gini)
    write_model_pojo(model)
    return model


def train_interest_rate_model(train, valid):
    """
    Train the Interest Rate model
    :param train: training frame
    :param valid: validation frame
    :return:
    """

    # Interest rate model
    target_variable = "int_rate"

    input_variables = ["loan_amnt", "longest_credit_length",
                       "revol_util", "emp_length", "home_ownership",
                       "annual_inc", "purpose", "addr_state", "dti",
                       "delinq_2yrs", "total_acc", "verification_status",
                       "term"]

    model = H2ORandomForestEstimator(
        ntrees=100,
        max_depth=5,
        stopping_tolerance=0.01,  # 10-fold increase in threshold as defined in rf_v1
        stopping_rounds=2,
        score_each_iteration=True,
        model_id="InterestRateModel",
        seed=2000000
    )
    model.train(input_variables, target_variable,
                training_frame=train, validation_frame=valid)

    print(model)
    write_model_pojo(model)
    return model


def write_model_pojo(model):
    """
    Write the model as POJO
    :param model: trained model
    :return: None
    """

    # Relative path from code dir
    output_directory = "build"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    h2o.download_pojo(model, path=output_directory)


def train_models():
    """
    Train both models
    :return: None
    """
    init_h2o()
    train, valid = get_data()
    train_bad_loan_model(train, valid)
    train_interest_rate_model(train, valid)


if __name__ == "__main__":
    train_models()

