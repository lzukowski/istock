import os

from setuptools import find_packages
from setuptools import setup


def path_in_project(*path):
    return os.path.join(os.path.dirname(__file__), *path)


def read_file(filename):
    with open(path_in_project(filename)) as f:
        return f.read()


def read_requirements(filename):
    contents = read_file(filename).strip('\n')
    return contents.split('\n') if contents else []


def get_version():
    return read_file('VERSION').strip()


setup(
    name='istock',
    version=get_version(),
    packages=find_packages(
        include=path_in_project('istock*'),
        exclude=['tests*'],
    ),
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('requirements_dev.txt'),
)
