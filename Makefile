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
