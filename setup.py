from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='mkdocs-nav-enhancements',
    version='0.9.1',
    author='Ryan Conway',
    author_email='ryan@rjc.cc',
    description='This is a small plugin for the excellent MkDocs project which makes some enhancements to the navigation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rylon/mkdocs-nav-enhancements',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-nav-enhancements = mkdocs_nav_enhancements:MkDocsNavEnhancements'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Documentation'
    ],
)
