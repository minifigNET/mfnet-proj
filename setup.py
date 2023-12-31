from setuptools import find_packages
from setuptools import setup

with open("requirements_package.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='mfnet',
      version="0.4",
      description="Lego figure recognition",
      author="minifigNET",
      install_requires=requirements,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
