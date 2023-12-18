import os
import requests
from prefect import task, flow

from mfnet.ml_logic.registry import mlflow_transition_model

from mfnet.interface.main import evaluate, preprocess, train
from mfnet.ml_logic.registry import mlflow_transition_model
from mfnet.params import *

@task
def preprocess_new_data():
    return preprocess()

@task
def evaluate_production_model():
    return evaluate()

@task
def re_train():
    return train()

@task
def transition_model(current_stage: str, new_stage: str):
    return mlflow_transition_model(current_stage=current_stage, new_stage=new_stage)

@flow(name=PREFECT_FLOW_NAME)
def train_flow():
    """
    - Import new data
    - compute `old_accuracy` by evaluating the current production model
    - compute `new_accuracy` by re-training, then evaluating the current production
    - if the new one is better than the old one, replace the current production model with the new one
    """

    preprocessed = preprocess_new_data.submit()

    old_accuracy = evaluate_production_model.submit(wait_for=[preprocessed])
    new_accuracy = re_train.submit(wait_for=[preprocessed])

    old_accuracy = old_accuracy.result()
    new_accuracy = new_accuracy.result()

    if old_accuracy < new_accuracy:
        print(f"🚀 New model replacing old in production with accuracy: {new_accuracy} the Old accuracy was: {old_accuracy}")
        transition_model.submit(current_stage="Staging", new_stage="Production")
        return f"🚀 New model replacing old in production with accuracy: {new_accuracy} the Old accuracy was: {old_accuracy}"
    else:
        print(f"🚀 Old model kept in place with accuracy: {old_accuracy}. The new accuracy was: {new_accuracy}")
        return f"🚀 Old model kept in place with accuracy: {old_accuracy}. The new accuracy was: {new_accuracy}"

if __name__ == "__main__":
    train_flow()
