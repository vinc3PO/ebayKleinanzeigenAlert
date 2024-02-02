from setuptools import setup, find_packages

setup(
    name='ebayAlert',
    version='1.5',
    packages=find_packages(),
    install_requires=[
        'click>=7.1',
        'requests>=2.31',
        'bs4>=0.0.1',
        'sqlalchemy>=1.4',
        'urllib3>=2.2.0'
    ],
    entry_points={'console_scripts': 'ebAlert=ebAlert.main:cli'}
)
