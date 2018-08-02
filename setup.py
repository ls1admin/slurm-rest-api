from setuptools import setup

setup(
    name='slurm-rest-api',
    packages=['slurm-rest-api'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-cors',
        'flask-restful',
        'Flask-SQLAlchemy',
        'mysql-python',
        'pyslurm',
        'pyyaml',
        'tinydb',
        'ujson',
        'uwsgi',
    ],
)
