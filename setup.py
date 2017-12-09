from setuptools import setup, find_packages

setup(
    name='FHIRstorm',
    # version='0.0.0',
    version='0.0.1',
    version_format='{tag}.dev{commitcount}',
    setup_requires=['setuptools-git-version'],
    description='SMART on FHIR client for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
    ],
    author='Rick Copeland',
    author_email='rick@arborian.com',
    url='https://github.com/Arborian/fhirstorm',
    keywords='',
    license="Apache License Version 2.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests_oauthlib',
        'PyJWT',
    ],
    tests_require=[],
    entry_points="""
    """)
