from distutils.core import setup

setup(
    name='dcp_parser',
    version='0.1',
    author='Steven Diamond, Eric Chu, Stephen Boyd',
    author_email='stevend2@stanford.edu, echu508@stanford.edu, boyd@stanford.edu',
    packages=[  'dcp_parser',
                'dcp_parser.atomic',
                'dcp_parser.error_messages',
                'dcp_parser.json',
             ],
    package_dir={'dcp_parser': 'dcp_parser'},
        url='https://github.com/SteveDiamond/parser/',
    license='...',
    description='A parser for mathematical expressions that does Disciplined Convex Programming analysis.',
    requires = ["ply(>= 3.4)"]
)