"""Set up or install package."""

from json import load
from os import getenv
from os.path import dirname, join

from setuptools import find_namespace_packages, setup


def read_pipenv_dependencies(fname):
    """Get default dependencies from Pipfile.lock."""
    filepath = join(dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = load(lockfile)
        return [dependency for dependency in lockjson.get('default')]


def read_readme(fname):
    """Get readme markdown file."""
    filepath = join(dirname(__file__), fname)
    with open(filepath, encoding='utf-8') as readme:
        readme.read()


if __name__ == '__main__':
    setup(
        name='kafka_consumer',
        version=getenv('PACKAGE_VERSION', '0.0.dev0'),
        author='Stefan Schenk',
        author_email='stefan_schenk@hotmail.com',
        long_description_content_type='text/markdown',
        long_description=read_readme('README.md'),
        description='Quickly read some kafka messages.',
        package_dir={'': 'src'},
        packages=find_namespace_packages('src', include=[
            'kafka_consumer*'
        ]),
        install_requires=read_pipenv_dependencies('Pipfile.lock'),
        entry_points={
            'console_scripts': [
                'consume=kafka_consumer.main:main'
            ]
        }
    )
