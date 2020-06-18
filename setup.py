from setuptools import setup, find_packages
import os


def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()


setup(
    name='pog',
    version='1.0.0',
    packages=find_packages(),
    author='Steven Liu',
    author_email='steven.liu@hivery.com',
    install_requires=read('requirements.txt').splitlines(),
    description='command for extract main inf from psa file.',
    license='Proprietary',
    long_description=read('README.md'),
    entry_points='''
    [console_scripts]
    pog=src.run:extract
    '''
)
