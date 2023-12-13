import glob
import os
import time
import pickle

from tensorflow import keras
from mfnet.params import *
import mlflow
from mlflow.tracking import MlflowClient

def save_results(params: dict,metrics:dict ) -> None:
    if params is not None:
        mlflow.log_params(params)
    if metrics is not None:
        mlflow.log_metrics(metrics)
    print("✅ Results saved on MLflow")

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Save params locally
    if params is not None:
        params_path = os.path.join(os.getcwd(), "cached_data","params", timestamp + ".pickle")
        with open(params_path, "wb") as file:
            pickle.dump(params, file)

    # Save metrics locally
    if metrics is not None:
        metrics_path = os.path.join(os.getcwd(), "cached_data", "metrics", timestamp + ".pickle")
        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)

    print("✅ Results saved locally")

def save_model(model: keras.Model) -> None:
    """
    Saves model on hard drive and on mlflow
    """
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    model_path = os.path.join(os.getcwd(), "cached_data", "models", f"{timestamp}.h5")
    model.save(model_path)

    print("✅ Model saved locally")

    mlflow.tensorflow.log_model(
            model=model,
            artifact_path="model",
            registered_model_name="mfnet proj"
        )

    print("✅ Model saved to MLflow")

def load_model(stage="Production") -> keras.Model:

    print(f"\nLoad [{stage}] model from MLflow...")

        # Load model from MLflow
    model = None
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()

    try:
        model_versions = client.get_latest_versions(name=MLFLOW_MODEL_NAME, stages=[stage])
        model_uri = model_versions[0].source

        assert model_uri is not None
    except:
        print(f"\n❌ No model found with name {MLFLOW_MODEL_NAME} in stage {stage}")

        return None

    model = mlflow.tensorflow.load_model(model_uri=model_uri)

    print("✅ Model loaded from MLflow")
    return model

def mlflow_transition_model(current_stage: str, new_stage: str) -> None:
    """
    Transition the latest model from the `current_stage` to the
    `new_stage` and archive the existing model in `new_stage`
    """
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    client = MlflowClient()

    version = client.get_latest_versions(name=MLFLOW_MODEL_NAME, stages=[current_stage])

    if not version:
        print(f"\n❌ No model found with name {MLFLOW_MODEL_NAME} in stage {current_stage}")
        return None

    client.transition_model_version_stage(
        name=MLFLOW_MODEL_NAME,
        version=version[0].version,
        stage=new_stage,
        archive_existing_versions=True
    )

    print(f"✅ Model {MLFLOW_MODEL_NAME} (version {version[0].version}) transitioned from {current_stage} to {new_stage}")

    return None

def mlflow_run(func):
    """
    Generic function to log params and results to MLflow along with TensorFlow auto-logging

    Args:
        - func (function): Function you want to run within the MLflow run
        - params (dict, optional): Params to add to the run in MLflow. Defaults to None.
        - context (str, optional): Param describing the context of the run. Defaults to "Train".
    """
    def wrapper(*args, **kwargs):
        mlflow.end_run()
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(experiment_name=MLFLOW_EXPERIMENT)

        with mlflow.start_run():
            mlflow.tensorflow.autolog()
            results = func(*args, **kwargs)

        print("✅ mlflow_run auto-log done")

        return results
    return wrapper
