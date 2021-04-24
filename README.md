# CYK_Parser_Visualization
The project started off owing to my liking for Automata Theory. Still working on improving the visual effects andmaking more enhancements in the project.
The project aims at visualizing how a string is parsed with respect to the Chomsky Normal Form (CNF) grammar using CYK algorithm which is widely used in the field of Automata Theory.



trial1 and trial2 are the images that show the obtained output.

Instructions
1) The grammar and the input string can be assigned in the CYK_parser.py file in the main function to variables **grammar and input_str**. 
   The grammar should be strictly in the following form:  grammar = ['S->AB',
                                                           'A->BB|a|h',
                                                           'B->AS|b|a',
                                                           'H->FG|a',
                                                          ]
The grammar should be in 'array of strings' form and **length of the grammar array should be less than 8 as the values don't fit in the blocks to make sure all the non terminals fit inside the block**.                                                         

2) Length of the input string can be anything depending on the monitor size.
3) Run the CYK_Parser.py file.
 
