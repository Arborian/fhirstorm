from setuptools import setup, find_packages

setup(
    name='FHIRstorm',
    # version='0.0.0',
    version='0.0.1',
    version_format='{tag}.dev{commitcount}',
    setup_requires=['setuptools-git-version'],
    description='SMART on FHIR client for Python',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Rick Copeland',
    author_email='rick@arborian.com',
    url='',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    tests_require=[],
    entry_points="""
    """)
