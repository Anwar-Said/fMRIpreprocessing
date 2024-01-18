from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()
setup(
    name='fMRIpreprocessing',
    version='0.1.0',
    long_description='A Python Package for preprocessing fMRI',
    long_description_content_type='text/markdown',
    author='Anwar Said',
    author_email='anwar.said@vanderbilt.edu',
    packages=find_packages(),
    install_requires=[
        # List any dependencies your package requires
        'numpy',
        'nilearn',
        'sphinx_rtd_theme'
    ],
    keywords=['python', 'neuroimaging'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
)