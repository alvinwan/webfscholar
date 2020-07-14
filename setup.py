import setuptools

VERSION = '0.0.3'

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="webfscholar",
    version=VERSION,
    author="Alvin Wan",
    author_email="hi@alvinwan.com",
    description="Generate publications webpages from Google Scholar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alvinwan/webfscholar",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    download_url='https://github.com/alvinwan/webfscholar/archive/%s.zip' % VERSION,
    scripts=['webfscholar/bin/webfscholar'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    include_package_data=True
)
