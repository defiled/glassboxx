from setuptools import setup, find_packages

setup(
    name='glassboxx',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['build/*', 'build/static/*/*'],
    },)
