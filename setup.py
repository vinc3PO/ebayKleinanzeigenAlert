from setuptools import setup, find_packages

setup(
    name='ebayAlert',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'click>=7.1',
        'requests>=2.23',
        'bs4>=0.0.1',
        'sqlalchemy>=1.4'
    ],
    entry_points={'console_scripts': 'ebAlert=ebAlert.main:cli'}
)