try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Virtuback',
    'author': 'Vilhelm von Ehrenheim',
    'url': 'https://github.com/while/virtuback',
    'author_email': 'vonehrenheim@gmail.com',
    'version': '0.2.0',
    'install_requires': ['nose', 'Flask', 'pymongo'],
    'packages': ['virtuback'],
    'scripts': [],
    'name': 'virtuback'
}

setup(**config)
