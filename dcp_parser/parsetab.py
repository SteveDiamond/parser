
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xe8C\xf4\x88\x02\xa3\xfd\x82\xf5\x83\x03`\r\x01l\xcb'
    
_lr_action_items = {'GEQ':([1,2,3,8,18,19,26,27,28,29,30,31,32,33,34,38,40,42,],[-21,11,-22,-23,11,-18,-19,None,-11,None,-10,None,-8,-9,-20,11,-15,11,]),'RPAREN':([1,3,8,18,19,26,27,28,29,30,31,32,33,34,37,38,40,42,],[-21,-22,-23,34,-18,-19,-14,-11,-12,-10,-13,-8,-9,-20,40,-16,-15,-17,]),'DIVIDE':([1,2,3,8,18,19,26,27,28,29,30,31,32,33,34,38,40,42,],[-21,12,-22,-23,12,-18,-19,12,-11,12,-10,12,12,12,-20,12,-15,12,]),'INT':([0,4,5,10,11,12,13,14,15,16,17,23,41,],[1,1,1,1,1,1,1,1,1,1,1,1,1,]),'SIGN':([7,9,],[22,25,]),'FLOAT':([0,4,5,10,11,12,13,14,15,16,17,23,41,],[3,3,3,3,3,3,3,3,3,3,3,3,3,]),'EQUALS':([1,2,3,8,18,19,26,27,28,29,30,31,32,33,34,38,40,42,],[-21,13,-22,-23,13,-18,-19,None,-11,None,-10,None,-8,-9,-20,13,-15,13,]),'ID':([0,4,5,7,9,10,11,12,13,14,15,16,17,20,21,22,23,24,25,35,36,39,41,],[8,8,8,21,21,8,8,8,8,8,8,8,8,35,-5,21,8,35,21,-6,35,35,8,]),'LEQ':([1,2,3,8,18,19,26,27,28,29,30,31,32,33,34,38,40,42,],[-21,15,-22,-23,15,-18,-19,None,-11,None,-10,None,-8,-9,-20,15,-15,15,]),'PLUS':([0,1,2,3,4,5,8,10,11,12,13,14,15,16,17,18,19,23,26,27,28,29,30,31,32,33,34,38,40,41,42,],[5,-21,16,-22,5,5,-23,5,5,5,5,5,5,5,5,16,-18,5,-19,16,-11,16,-10,16,-8,-9,-20,16,-15,5,16,]),'LPAREN':([0,4,5,8,10,11,12,13,14,15,16,17,23,41,],[4,4,4,23,4,4,4,4,4,4,4,4,4,4,]),'VARIABLE':([0,],[7,]),'COMMA':([1,3,8,19,26,27,28,29,30,31,32,33,34,37,38,40,42,],[-21,-22,-23,-18,-19,-14,-11,-12,-10,-13,-8,-9,-20,41,-16,-15,-17,]),'TIMES':([1,2,3,8,18,19,26,27,28,29,30,31,32,33,34,38,40,42,],[-21,14,-22,-23,14,-18,-19,14,-11,14,-10,14,14,14,-20,14,-15,14,]),'PARAMETER':([0,],[9,]),'MINUS':([0,1,2,3,4,5,8,10,11,12,13,14,15,16,17,18,19,23,26,27,28,29,30,31,32,33,34,38,40,41,42,],[10,-21,17,-22,10,10,-23,10,10,10,10,10,10,10,10,17,-18,10,-19,17,-11,17,-10,17,-8,-9,-20,17,-15,10,17,]),'$end':([1,2,3,6,8,19,20,21,24,26,27,28,29,30,31,32,33,34,35,36,39,40,],[-21,-7,-22,0,-23,-18,-2,-5,-4,-19,-14,-11,-12,-10,-13,-8,-9,-20,-6,-1,-3,-15,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'id_list':([7,9,22,25,],[20,24,36,39,]),'expression_list':([23,],[37,]),'expression':([0,4,5,10,11,12,13,14,15,16,17,23,41,],[2,18,19,26,27,28,29,30,31,32,33,38,42,]),'statement':([0,],[6,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> VARIABLE SIGN id_list','statement',3,'p_statement_variables','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',112),
  ('statement -> VARIABLE id_list','statement',2,'p_statement_variables','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',113),
  ('statement -> PARAMETER SIGN id_list','statement',3,'p_statement_parameters','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',126),
  ('statement -> PARAMETER id_list','statement',2,'p_statement_parameters','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',127),
  ('id_list -> ID','id_list',1,'p_id_list','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',139),
  ('id_list -> id_list ID','id_list',2,'p_id_list','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',140),
  ('statement -> expression','statement',1,'p_statement_expr','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',149),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',154),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',155),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',156),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',157),
  ('expression -> expression EQUALS expression','expression',3,'p_expression_binop','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',158),
  ('expression -> expression LEQ expression','expression',3,'p_expression_binop','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',159),
  ('expression -> expression GEQ expression','expression',3,'p_expression_binop','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',160),
  ('expression -> ID LPAREN expression_list RPAREN','expression',4,'p_expression_atom','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',171),
  ('expression_list -> expression','expression_list',1,'p_expression_list','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',180),
  ('expression_list -> expression_list COMMA expression','expression_list',3,'p_expression_list','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',181),
  ('expression -> PLUS expression','expression',2,'p_expression_uplus','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',190),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',194),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',199),
  ('expression -> INT','expression',1,'p_expression_number','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',204),
  ('expression -> FLOAT','expression',1,'p_expression_number','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',205),
  ('expression -> ID','expression',1,'p_expression_id','/Users/smd999995/PythonProjects/dcp_parser/dcp_parser/parser.py',210),
]
