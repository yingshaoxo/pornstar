from setuptools import setup, find_packages
from os.path import dirname, join, abspath

file_path = join(abspath(dirname(__file__)), "README.md")
with open(file_path) as f:
    long_description = f.read()

setup(
    name='pornstar',
    version='0.1',
    description='Make you become the next porn star!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='pornstar',
    url='https://github.com/yingshaoxo/pornstar',
    author='yingshaoxo',
    author_email='yingshaoxo@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'setuptools',
        'auto_everything',
        'numpy',
        'matplotlib',
        'pillow',
        'moviepy',
    ]
)
