from setuptools import setup

setup(
    name='converter',
    version='1.0.0',
    packages=[''],
    url='https://github.com/QuantumCalzone/unity-project-to-upm',
    license='',
    author='QuantumCalzone',
    author_email='QuantumCalzone@gmail.com',
    description='An automation tool to converter your unity project into a package hosted with git.',
    install_requires=[
        'cached-property==1.5.1',
        'cffi==1.14.0',
        'pycparser==2.20',
        'pygit2==1.2.1',
        'pyperclip==1.8.0',
    ],
)
