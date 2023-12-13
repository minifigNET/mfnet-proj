create_local_env_as: create_local_env install_apple_silicon
create_local_env_mi: create_local_env install_mac_intel

create_local_env:
	pyenv virtualenv 3.10.6 mfnet-env
	pyenv local mfnet-env

delete_local_env: disable_local_env
	pyenv virtualenv-delete mfnet-env

disable_local_env:
	rm .python-version

enable_local_env:
	pyenv local mfnet-env


install_apple_silicon:
	pip install --upgrade pip
	pip install -r requirements_apple_silicon.txt

install_mac_intel:
	pip install --upgrade pip
	pip install -r requirements_mac_intel.txt

reinstall_package:
	@pip uninstall -y mfnet || :
	@pip install -e .

run_preprocess:
	python -c 'from mfnet.interface.main import preprocess; preprocess()'

run_train:
	python -c 'from mfnet.interface.main import train; train()'

run_pred:
	python -c 'from mfnet.interface.main import pred; pred()'

run_evaluate:
	python -c 'from mfnet.interface.main import evaluate; evaluate()'

run_all: run_preprocess run_train run_pred run_evaluate

run_workflow:
	PREFECT__LOGGING__LEVEL=${PREFECT_LOG_LEVEL} python -m mfnet.interface.workflow

run_api:
	uvicorn mfnet.api.fast:app --reload
