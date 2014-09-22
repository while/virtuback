try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Vilhelm von Ehrenheim',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'vonehrenheim@gmail.com',
    'version': '0.1.0',
    'install_requires': ['nose'],
    'packages': ['virtuback'],
    'scripts': [],
    'name': 'virtuback'
}

setup(**config)

