To interact with the parser, first write a file containing expressions of the following form:
  variable x y z ...
  parameter (SIGN) a b c ...
  Any objective (i.e. '-log(x) + max(square(y),a) + b*z')

The currently implemented atoms are square, max, log_sum_exp, and log.
See sample.txt for an example.

Run dcp_parser/demo.py and follow the instructions. You will then be able to browse the parse trees for the objectives in the file.