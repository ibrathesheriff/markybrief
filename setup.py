import setuptools

setuptools.setup(
    include_package_data=True,
    name='markybrief',
    version='0.0.1',
    description='A ool for generating concise summaries of HTML and markdown files.',
    url='https://github.com/ibrathesheriff/markybrief',
    author='ibrathesheriff',
    author_email='thesheriff@ibrathesheriff.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['bert-extractive-summarizer', 'beautifulsoup4', 'torch', 'Markdown', 'html5lib'
    ],
    long_description='A lightweight Python tool for generating concise summaries of HTML and markdown files. Perfect for developers and teams to quickly grasp the essence of documentation.',
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.12',
         "Operating System :: OS Independent",
    ],
)