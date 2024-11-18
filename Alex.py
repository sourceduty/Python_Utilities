nodes = ['Alex ', "didn't ", 'study ', 'Python', '.']
expression = ''.join(nodes)

valid = False
invalid = True

valid_expression = "Alex learned Python."
invalid_expression = "Alex didn't study Python."

if invalid:
 print(valid_expression)

elif valid: 
 print(invalid_expression)
 
else:
    print("Alex studies theoretical programming.")
