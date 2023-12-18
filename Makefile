default:
	nohup uvicorn mfnet.api.api:api --reload --port $(API_PORT) &

create_local_env_with_as_deps: create_local_env install_apple_silicon_deps
create_local_env_with_mi_deps: create_local_env install_mac_intel_deps
create_local_env_with_linux_deps: create_local_env install_linux_deps

create_env:
	pyenv virtualenv 3.10.6 mfnet-env

delete_env:
	pyenv virtualenv-delete mfnet-env

create_local_env: create_env enable_local_env

delete_local_env: disable_local_env delete_env

disable_local_env:
	rm .python-version

enable_local_env:
	pyenv local mfnet-env

install_apple_silicon_deps:
	pip install --upgrade pip
	pip install -r requirements_apple_silicon.txt

install_mac_intel_deps:
	pip install --upgrade pip
	pip install -r requirements_mac_intel.txt

install_linux_deps:
	pip install --upgrade pip
	pip install -r requirements_linux.txt

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

start_web_app:
	streamlit run website/app.py

start_api:
	uvicorn mfnet.api.api:api --reload --port $(API_PORT)
