from setuptools import setup


setup(
    name='mkdocs-title-plugin',
    version='0.1',
    description='',
    author='Ryan Conway',
    author_email='',
    license='MIT',
    packages=['mkdocs_title_plugin'],
    install_requires=[
        "mkdocs>=1"
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-title-plugin = mkdocs_title_plugin:MkDocsTitlePlugin'
        ]
    }
)
