from setuptools import setup, find_packages

setup(
    name='ebayAlert',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Click',
        'requests',
        'bs4',
        'sqlalchemy'
    ],
    entry_points={'console_scripts':'ebAlert=app.ebklalert:cli'}
)