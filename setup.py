from setuptools import setup, find_packages

setup(
    name='ebayAlert',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'click>=7.1',
        'requests>=2.23',
        'bs4>=0.0.1',
        'sqlalchemy>=1.3',
        'pydantic>=1.7'
    ],
    entry_points={'console_scripts':'ebAlert=ebAlert.__main__:cli'}
)