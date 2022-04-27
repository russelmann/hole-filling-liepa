from setuptools import setup, find_packages

setup(
    name='hole-filling-liepa',
    version='0.0.1',
    author='Ruslan Guseinov',
    description='Hole filling algorithm by P. Liepa.',
    packages=find_packages(),
    include_package_data=True,
    package_data={'hole_filling_liepa': ['*.pyd', '*.so']},
)
