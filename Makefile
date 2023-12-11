create_local_env_as: create_local_env install_apple_silicon

create_local_env:
	pyenv virtualenv 3.10.6 mfnet-env
	pyenv local mfnet-env

delete_local_env:
	rm .python-version
	pyenv virtualenv-delete mfnet-env

install_apple_silicon:
	pip install --upgrade pip
	pip install -r requirements_apple_silicon.txt
