from setuptools import setup


def readme():
    with open('README.md') as file:
        return file.read()


setup(
    name='airdrive',
    version='0.1.5',
    description='Unlimited cloud storage for your files',
    long_description=readme(),
    long_description_content_type="text/markdown",
    package_dir={'airdrive': 'src'},
    packages=['airdrive'],
    install_requires=['deta'],
    url='https://github.com/jnsougata/airdrive',
    project_urls={
        "Bug Tracker": "https://github.com/jnsougata/airdrive/issues"
    },
    author='Sougata Jana',
    author_email='jnsougata@gmail.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
