from distutils.core import setup

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(
    name='reservation',
    version='1.0.0',
    description='Room reservation module for portal',
    long_description=long_description,
    author='Vlad Bezpalko',
    author_email='vl.bezpalko@gmail.com',
    packages=[],
    install_requires=[
        'celery>=4',
        'dj-database-url',
        'Django>=1.10',
        'django-filter>=1.0.1',
        'django-getenv',
        'djangorestframework>=3.5',
        'psycopg2',
        'redis>=2',
    ],
    tests_require=[
        'pytest',
        'pytest-django',
        'freezegun',
    ],
    dependency_links=[],
    license='MIT',
    include_package_data=True,
)
