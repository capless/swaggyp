from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


version = '0.1.0'

setup(
    name='swaggyp',
    version=version,
    description="Python library for generating Swagger templates based on valley ",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only"
    ],
    keywords='swagger, valley, api',
    author='Brian Jinwright',
    author_email='opensource@ipoots.com',
    maintainer='Brian Jinwright',
    packages=find_packages(),
    url='https://github.com/capless/swaggyp',
    license='GNU General Public License v3.0',
    install_requires=parse_requirements('requirements.txt'),
    include_package_data=True,
    zip_safe=False,
)
