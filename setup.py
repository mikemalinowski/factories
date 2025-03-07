import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='factories',
    version='1.4.0',
    author='Mike Malinowski',
    author_email='mike.malinowski@outlook.com',
    description='A python package exposing the factory/plugin design pattern',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>3.1.1',
    url='https://github.com/mikemalinowski/factories',
    packages=setuptools.find_packages(),
    install_requires=[
        "signalling",
    ],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
