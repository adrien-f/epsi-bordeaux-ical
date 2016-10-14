from setuptools import setup, find_packages

setup(
    name='ical-dumper',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'arrow',
        'beautifulsoup4',
        'icalendar',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        icaldump=icaldump.main:cli
    ''',
)