import setuptools
from setuptools import setup


setup(
    name='CSPInstWithPref',
    version='1.0',
    description='A scientific simple package for solving constraint satisfaction problems with conditional preferences',
    author='Mohsen Zahraei',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Topic :: Software Development :: AI TOOLS',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.11',
    ],
    keywords="Constraint Satisfaction Problem, CSP, RB model,"
             " Random CSP, AI tools, AI, Conditional preferences,"
             " CP-net, CSP solver, CP tables, dependencies, parents,"
             " full look ahead, back tracking, forward checking,"
             " outcomes, K-pareto outcomes, Random binary CSP",
    author_email='mzx776@uregina.ca',
    url='https://github.com/AmirrezaZahraei1387/CSP_RB_EXAMPLE_preferences',
    packages=setuptools.find_packages(),
)

