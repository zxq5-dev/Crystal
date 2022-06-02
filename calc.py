def calculate(equation):
    # starting variables
    instruction_list_unprocessed = []
    instruction_list = []

    # user interface
    print("possible operations: +, -, *, /, //, %, **, sqrt, and single pairs of brackets")

    # inputs and initial processing

    total_length = len(equation)

    # moving each character of the equation to a separate variable in a list (instruction_list_unprocessed)
#
    for i in range(total_length):
        instruction_list_unprocessed.append(equation[i])

    instruction_list_unprocessed.append("x")
    # consolidating multi digit numbers

    for i in range(total_length):
        if str(instruction_list_unprocessed[i]).isnumeric():
            if str(instruction_list_unprocessed[i + 1]).isnumeric():
                instruction_list_unprocessed[i + 1] = instruction_list_unprocessed[i] + instruction_list_unprocessed[i + 1]
                instruction_list_unprocessed[i] = "empty"

    # consolidating muliti character operators

    for i in range(total_length):
        if str(instruction_list_unprocessed[i]).isnumeric():
            b = 0
        else:
            if instruction_list_unprocessed[i] == instruction_list_unprocessed[i + 1]:
                instruction_list_unprocessed[i + 1] = instruction_list_unprocessed[i] + instruction_list_unprocessed[i + 1]
                instruction_list_unprocessed[i] = "empty"

    # consolidating sqrt command

    for i in range(total_length):
        if str(instruction_list_unprocessed[i]).isalpha():
            if str(instruction_list_unprocessed[i]) == "s":
                instruction_list.append("sqrt")
        else: instruction_list.append(instruction_list_unprocessed[i])


    # inputs are processed here before calculation

    length = len(instruction_list)
    operation_count = 0
    print(instruction_list)
    brackets = instruction_list.count("(")
    if brackets != 0:
        print("            simplifying brackets...")

    for i in range(brackets):
        a = int(instruction_list.index("("))
        b = int(instruction_list.index(")"))
        bracket = instruction_list[a:b]

        # sqrt module

        sqrt_count_brackets = bracket.count("sqrt")

        for i in range(sqrt_count_brackets):
            x = instruction_list.index("sqrt", a, b)
            instruction_list[x] = math.sqrt(float(instruction_list[x + 1]))
            instruction_list.pop(x + 1)
            operation_count = operation_count + 1
            print(instruction_list)

        # powers module

        power_count_brackets = bracket.count("**")

        for i in range(power_count_brackets):
            x = instruction_list.index("**", a, b)
            instruction_list[x] = float(instruction_list[x - 1]) ** float(instruction_list[x + 1])
            instruction_list.pop(x + 1)
            instruction_list.pop(x - 1)
            operation_count = operation_count + 2
            print(instruction_list)

        # multiplication module

        multiplication_count_brackets = bracket.count("*")

        for i in range(multiplication_count_brackets):
            x = instruction_list.index("*", a, b)
            instruction_list[x] = float(instruction_list[x - 1]) * float(instruction_list[x + 1])
            instruction_list.pop(x + 1)
            instruction_list.pop(x - 1)
            operation_count = operation_count + 2
            print(instruction_list)

        # remainder division module

        remainder_div_count_brackets = bracket.count("%")

        for i in range(remainder_div_count_brackets):
            x = instruction_list.index("%", a, b)
            instruction_list[x] = float(instruction_list[x - 1]) % float(instruction_list[x + 1])
            instruction_list.pop(x + 1)
            instruction_list.pop(x - 1)
            operation_count = operation_count + 2
            print(instruction_list)

        # integer division module

        int_div_count_brackets = bracket.count("//")

        for i in range(int_div_count_brackets):
            x = instruction_list.index("//", a, b)
            instruction_list[x] = float(instruction_list[x - 1]) // float(instruction_list[x + 1])
            instruction_list.pop(x + 1)
            instruction_list.pop(x - 1)
            operation_count = operation_count + 2
            print(instruction_list)

        # division module

        div_count_brackets = bracket.count("/")

        for i in range(div_count_brackets):
            x = instruction_list.index("/", a, b)
            instruction_list[x] = float(instruction_list[x - 1]) / float(instruction_list[x + 1])
            instruction_list.pop(x + 1)
            instruction_list.pop(x - 1)
            operation_count = operation_count + 2
            print(instruction_list)

        # addition module

        addition_count_brackets = bracket.count("+")

        for i in range(addition_count_brackets):
            x = instruction_list.index("+", a, b)
            instruction_list[x] = float(instruction_list[x - 1]) + float(instruction_list[x + 1])
            instruction_list.pop(x + 1)
            instruction_list.pop(x - 1)
            operation_count = operation_count + 2
            print(instruction_list)

        # subtraction module

        subtraction_count_brackets = bracket.count("-")

        for i in range(subtraction_count_brackets):
            x = instruction_list.index("-", a, b)
            instruction_list[x] = float(instruction_list[x - 1]) - float(instruction_list[x + 1])
            instruction_list.pop(x + 1)
            instruction_list.pop(x - 1)
            operation_count = operation_count + 2
            print(instruction_list)

        # final processing of this bracket

        instruction_list.remove("(")
        instruction_list.remove(")")

    print(instruction_list)

    # main calculation module

    length = len(instruction_list)
    operation_count = 0
    print("            calculating answer...")

    # sqrt module

    sqrt_count = instruction_list.count("sqrt")

    for i in range(sqrt_count):
        x = instruction_list.index("sqrt")
        instruction_list[x] = math.sqrt(float(instruction_list[x + 1]))
        instruction_list.pop(x + 1)
        operation_count = operation_count + 1
        print(instruction_list)
    # indices module

    power_count = instruction_list.count("**")

    for i in range(power_count):
        x = instruction_list.index("**")
        instruction_list[x] = float(instruction_list[x - 1]) ** float(instruction_list[x + 1])
        instruction_list.pop(x + 1)
        instruction_list.pop(x - 1)
        operation_count = operation_count + 2
        print(instruction_list)
    # multiplication module

    multiplication_count = instruction_list.count("*")

    for i in range(multiplication_count):
        x = instruction_list.index("*")
        instruction_list[x] = float(instruction_list[x - 1]) * float(instruction_list[x + 1])
        instruction_list.pop(x + 1)
        instruction_list.pop(x - 1)
        operation_count = operation_count + 2
        print(instruction_list)
    # remainder division module

    remainder_div_count = instruction_list.count("%")

    for i in range(remainder_div_count):
        x = instruction_list.index("%")
        instruction_list[x] = float(instruction_list[x - 1]) % float(instruction_list[x + 1])
        instruction_list.pop(x + 1)
        instruction_list.pop(x - 1)
        operation_count = operation_count + 2
        print(instruction_list)
    # integer division module

    int_div_count = instruction_list.count("//")

    for i in range(int_div_count):
        x = instruction_list.index("//")
        instruction_list[x] = float(instruction_list[x - 1]) // float(instruction_list[x + 1])
        instruction_list.pop(x + 1)
        instruction_list.pop(x - 1)
        operation_count = operation_count + 2
        print(instruction_list)
    # division module

    division_count = instruction_list.count("/")

    for i in range(division_count):
        x = instruction_list.index("/")
        instruction_list[x] = float(instruction_list[x - 1]) / float(instruction_list[x + 1])
        instruction_list.pop(x + 1)
        instruction_list.pop(x - 1)
        operation_count = operation_count + 2
        print(instruction_list)
    # addition module

    addition_count = instruction_list.count("+")

    for i in range(addition_count):
        x = instruction_list.index("+")
        instruction_list[x] = float(instruction_list[x - 1]) + float(instruction_list[x + 1])
        instruction_list.pop(x + 1)
        instruction_list.pop(x - 1)
        operation_count = operation_count + 2
        print(instruction_list)
    # subtraction module

    subtraction_count = instruction_list.count("-")

    for i in range(subtraction_count):
        x = instruction_list.index("-")
        instruction_list[x] = float(instruction_list[x - 1]) - float(instruction_list[x + 1])
        instruction_list.pop(x + 1)
        instruction_list.pop(x - 1)
        operation_count = operation_count + 2
        print(instruction_list)


    # outputs

    answer = instruction_list
    return(answer)
