def main():

    result = None
    operand = None
    operator = None
    wait_for_number = True

    while True:
        if wait_for_number:

            while True:
                operand = input(">>> ")

                try:
                    operand = float(operand)
                except ValueError:

                    print(f"{operand} is not a number. Try again.")
                    continue

                else:
                    if operator == '/':

                        try:
                            result /= operand

                        except ZeroDivisionError:
                            print('Can\'t divide by Zero')
                            continue

                    elif operator == '*':
                        result *= operand

                    elif operator == '+':
                        result += operand

                    elif operator == '-':
                        result -= operand
                wait_for_number = False
                break

        elif operator == '=' and wait_for_number == False:
            print(f'Result: {result}')
            break

        elif not operator:
            result = operand
            operator = True
            continue

        elif not wait_for_number:

            while True:
                operator = input()

                if operator == '=' and result:
                    wait_for_number = False
                    break

                elif not (operator == '+' or operator == '/' or operator == '*' or operator == '-'):
                    print(
                        f"'{operator}' is not '+' or '-' or '/' or '*'. Try again.")
                    continue

                else:
                    wait_for_number = True
                    break


if __name__ == "__main__":
    main()
