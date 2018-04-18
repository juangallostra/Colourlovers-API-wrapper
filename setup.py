from setuptools import setup

setup(
    name='colourlovers',
    packages=['colourlovers'], # this must be the same as the name above
    version='0.1.2',
    description='A python wrapper for ColourLovers API',
    long_description='\n\n'.join([
        open('README.rst').read(), open('CHANGES.rst').read()]),
    author='Juan Gallostra',
    author_email='juangallostra@gmail.com',
    license='MIT',
    url='https://github.com/juangallostra/Colourlovers-API-wrapper', # use the URL to the github repo
    download_url='https://github.com/juangallostra/Colourlovers-API-wrapper/archive/0.1.2.tar.gz', # I'll explain this in a second
    keywords=['color', 'colour', 'palette', 'api', 'colourlovers', 'wrapper'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'Pillow',
    ],
)