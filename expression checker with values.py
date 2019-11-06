#!/usr/bin/python3
# Operators: (,),!,&,|,→,←,⇔
# Operators=['!','&','|','→','←','⇔']
# Example1: ((P→(!Q))&(!((P→(!Q))|(!(P⇔R))))
# Example2: (P→(Q&R))
# Example3: ((P→(!Q))&(!((P→(!Q))|(!(P⇔R)))))
import re
import sys
import itertools

atoms = set()
atoms_dict = dict()
table = dict()
list_of_interp = dict()
top = "    |"
has_top = 0


def main(argc, argv):
    global atoms, atoms_dict, table, list_of_interp
    try:
        i = input("Enter a proposition: ")
    except Exception as err:
        print("Wrong input")
        return
    if len(i) == 0:
        print("No input")
    elif len(i) == 1:
        if i.isalpha():
            print("Is a unit")
        else:
            print("Is not a unit, try a letter")
    elif i[0] != "(":
        print("The proposition is missing a parentheses at the begining")
    else:
        i = parse_nested(i)
        if i != 0:
            if recursion(i) == 1:

                # Validity check is done

                to_continue = input("\nThe proposition is valid. Would you like to create a truth table for it? Y/N? ")
                if to_continue not in ["1", "Y", "y", "yes", "Yes", "YES", "ya"]:
                    return
                all_interp = input("\nWould you like to provide an interpretation, or see all possible ones? 0/1? ")
                if all_interp != "1":
                    # Print the truth table for a given number of interpretations

                    nr = input("\nHow many interpretations would you like to provide? ")
                    list_of_interp = {x: {y: False for y in atoms} for x in range(0, int(nr) + 1)}
                    for j in range(int(nr)):
                        print("\nInterpretation " + str(j + 1) + ":")
                        get_atom_values(atoms, list_of_interp[j])
                    print("\nTruth table:")
                    for j in range(int(nr)):
                        atoms_dict = list_of_interp[j]
                        expression_truth_value(i)
                        print_truth_table(list_of_interp[j], table, j + 1)
                else:
                    # Print the truth table for all possible interpretations

                    # Generate all possible combinations of true/false
                    possible = list(itertools.product([False, True], repeat=len(atoms)))
                    x = 0
                    for var in possible:
                        list_of_interp[x] = {atom: var[count] for count, atom in enumerate(atoms)}
                        x += 1
                    print("\nTruth table:")
                    for j in range(2 ** len(atoms)):
                        atoms_dict = list_of_interp[j]
                        expression_truth_value(i)
                        print_truth_table(list_of_interp[j], table, j + 1)


# Converts the input list into nested lists based on parentheses
def parse_nested(text, left=r'[(]', right=r'[)]'):
    """ Based on https://stackoverflow.com/a/23185606 (unubtu)
    Who based his answer on https://stackoverflow.com/a/17141899/190597 (falsetru) """
    tokens = list(text)
    stack = [[]]
    for x in tokens:
        if not x: continue
        if re.match(left, x):
            stack[-1].append([])
            stack.append(stack[-1][-1])
        # Keep opening parentheses
        # stack[-1].append(x)
        elif re.match(right, x):
            # Keep closing parentheses
            # stack[-1].append(x)
            stack.pop()
            if not stack:
                print('The proposition is missing an opening parantheses')
                return 0
        else:
            stack[-1].append(x)
    if len(stack) > 1:
        print('The proposition is missing a closing parantheses')
        return 0
    return stack.pop()[0]


# Checks a basic expression (if it contains a list it considers it valid)
def check_expression(expression):
    operators = ['!', '&', '|', '→', '←', '⇔']
    global atoms
    if len(expression) != 2 and len(expression) != 3:
        print(str(expression) + " is not an expression.")
        return 0
    if len(expression) == 2:
        if expression[0] == "!":
            if type(expression[1]) == list:
                return 1
            elif expression[1].isalpha():
                atoms.add(expression[1])
                return 1
        else:
            print(str(expression) + " is not a valid expression. Is missing an operator or an atom/proposition")
            return 0
    else:
        if type(expression[0]) == list or expression[0].isalpha():
            if type(expression[0]) != list and expression[0].isalpha():
                atoms.add(expression[0])
            if (expression[1] in operators) and expression[1] != '!':
                if type(expression[2]) == list or expression[2].isalpha():
                    if type(expression[2]) != list and expression[2].isalpha():
                        atoms.add(expression[2])
                    return 1
                else:
                    print(str(expression) + " Error: the last argument of the expression is not an unit or expression")
                    return 0
            else:
                print(str(expression) + " Error: the expression is missing an operator")
                return 0
        else:
            print(str(expression) + " Error: the first argument of the expression is not an unit or expression")
            return 0


# Converts a nested list to a flat one
def flatten_nested_list(nested_list):
    flat_list = []
    # Iterate over all the elements in given list
    for elem in nested_list:
        # Check if type of element is list
        if isinstance(elem, list):
            # Extend the flat list by adding contents of this element (list)
            flat_list.append("(")
            flat_list.extend(flatten_nested_list(elem))
            flat_list.append(")")
        else:
            # Append the element to the list
            flat_list.append(elem)
    return flat_list


# Checks if an expression doesnt contain lists (it' minimal)
def minimal(expression):
    for each in expression:
        if type(each) == list:
            return 0
    return 1


# Iterates through the expression and checks from the innermost ones
def recursion(expression):
    global table
    if minimal(expression):
        table["".join(flatten_nested_list(expression))] = False
        return check_expression(expression)
    else:
        for each in expression:
            if type(each) == list:
                # print("Verifying this smaller proposition: "+str(each))
                if recursion(each) == 0:
                    return 0
        val = check_expression(expression)
        table["".join(flatten_nested_list(expression))] = False
        return val


# Iterates through
def get_atom_values(atom_set, atom_dict):
    for each in atom_set:
        i = input("Value of " + str(each) + " = ")
        if i in ["True", "true", "TRUE", "1", "t", "T"]:
            atom_dict[each] = True
        elif i in ["False", "false", "FALSE", "0", "f", "F"]:
            atom_dict[each] = False
        else:
            print("Wrong input value for " + str(each))


# Logical operation not
def op_not(par1):
    return not par1


# Logical operation and
def op_and(par1, par2):
    return par1 and par2


# Logical operation or
def op_or(par1, par2):
    return par1 or par2


# Logical operation implication
def op_impl(par1, par2):
    return (not par1) or par2


# Logical operation equivalence
def op_eq(par1, par2):
    return par1 == par2


# Returns the truth value of the expression based on atoms_dict,
# and stores in table the truth values of each smaller expression
def expression_truth_value(expression):
    operators = ['&', '|', '→', '⇔']
    global atoms_dict, table
    expression_string = "".join(flatten_nested_list(expression))
    value = 0
    if len(expression) == 2:
        if expression[0] == "!":
            if type(expression[1]) == list:
                value = op_not(expression_truth_value(expression[1]))
            elif expression[1].isalpha():
                value = op_not(atoms_dict[expression[1]])
    else:
        if expression[1] == "&":
            if type(expression[0]) == list and type(expression[2]) == list:
                value = op_and(expression_truth_value(expression[0]), expression_truth_value(expression[2]))
            elif type(expression[0]) == list:
                value = op_and(expression_truth_value(expression[0]), atoms_dict[expression[2]])
            elif type(expression[2]) == list:
                value = op_and(atoms_dict[expression[0]], expression_truth_value(expression[2]))
            else:
                value = op_and(atoms_dict[expression[0]], atoms_dict[expression[2]])
        elif expression[1] == "|":
            if type(expression[0]) == list and type(expression[2]) == list:
                value = op_or(expression_truth_value(expression[0]), expression_truth_value(expression[2]))
            elif type(expression[0]) == list:
                value = op_or(expression_truth_value(expression[0]), atoms_dict[expression[2]])
            elif type(expression[2]) == list:
                value = op_or(atoms_dict[expression[0]], expression_truth_value(expression[2]))
            else:
                value = op_or(atoms_dict[expression[0]], atoms_dict[expression[2]])
        elif expression[1] == "→":
            if type(expression[0]) == list and type(expression[2]) == list:
                value = op_impl(expression_truth_value(expression[0]), expression_truth_value(expression[2]))
            elif type(expression[0]) == list:
                value = op_impl(expression_truth_value(expression[0]), atoms_dict[expression[2]])
            elif type(expression[2]) == list:
                value = op_impl(atoms_dict[expression[0]], expression_truth_value(expression[2]))
            else:
                value = op_impl(atoms_dict[expression[0]], atoms_dict[expression[2]])
        elif expression[1] == "⇔":
            if type(expression[0]) == list and type(expression[2]) == list:
                value = op_eq(expression_truth_value(expression[0]), expression_truth_value(expression[2]))
            elif type(expression[0]) == list:
                value = op_eq(expression_truth_value(expression[0]), atoms_dict[expression[2]])
            elif type(expression[2]) == list:
                value = op_eq(atoms_dict[expression[0]], expression_truth_value(expression[2]))
            else:
                value = op_eq(atoms_dict[expression[0]], atoms_dict[expression[2]])
    table[expression_string] = value
    return value


# Pretty prints the truth table
def print_truth_table(atoms_table, exp_table, interpretation_nr):
    global has_top, top
    # Add atoms at the begining of the table
    table = {**atoms_table, **exp_table}

    # Create table top
    if has_top == 0:
        for i, each in enumerate(table):
            top += each.ljust(len(each) + 2, " ").rjust(len(each) + 4, " ")
            top += "|"

    # Create separation line
    line = ""
    sw = 0
    for each in top:
        if each == "|" and sw == 1:
            line += "|"
        else:
            line += "-"
        if each != " ":
            sw = 0
        else:
            sw = 1

    # Create interpretation row
    row = "I" + str(interpretation_nr) + "  |"
    for i, each in enumerate(table):
        row += str(table[each]).ljust(len(each) + 4, " ")
        row += "|"
    if has_top == 0:
        for each in top:
            print("-", end="")
        print("")
        print(top)
        has_top = 1

    print(line)
    print(row)


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)

# GOOD to skip () for a linear iteration of the expression
# for i,c in enumerate(expression):
# 	if c in ['(',')']:
# 		sw*=-1
# 		last=')'
# 		pass
# 	if sw==1:
# 		pass
# 	last=c
