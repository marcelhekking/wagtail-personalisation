import re
from setuptools import find_packages, setup


install_requires = [
    'wagtail>=1.10,<1.11',
    'user-agents>=1.0.1',
    'wagtailfontawesome>=1.0.6',
]

tests_require = [
    'factory_boy==2.8.1',
    'flake8',
    'flake8-blind-except',
    'flake8-debugger',
    'flake8-imports',
    'freezegun==0.3.8',
    'pytest-cov==2.4.0',
    'pytest-django==3.1.2',
    'pytest-sugar==0.7.1',
    'pytest==3.1.0',
    'wagtail_factories==0.3.0',
]

docs_require = [
    'sphinx>=1.4.0',
]

with open('README.rst') as fh:
    long_description = re.sub(
        '^.. start-no-pypi.*^.. end-no-pypi', '', fh.read(), flags=re.M | re.S)

setup(
    name='wagtail-personalisation',
    version='0.9.0',
    description='A Wagtail add-on for showing personalized content',
    author='Lab Digital BV',
    author_email='opensource@labdigital.nl',
    url='http://labdigital.nl',
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'docs': docs_require,
        'test': tests_require,
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    license='MIT',
    long_description=long_description,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
