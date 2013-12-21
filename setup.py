from distutils.core import setup

setup(
    name='dcp_parser',
    version='1.0',
    author='Steven Diamond',
    author_email='stevend2@stanford.edu',
    packages=[  'dcp_parser',
                'dcp_parser.atomic',
                'dcp_parser.error_messages',
                'dcp_parser.expression',
                'dcp_parser.json',
             ],
    package_dir={'dcp_parser': 'dcp_parser'},
        url='https://github.com/SteveDiamond/parser/',
    license='...',
    description='A parser for mathematical expressions that does Disciplined Convex Programming analysis.',
    long_description=open('README.txt').read(),
    requires = ["ply(>= 3.4)"]
)