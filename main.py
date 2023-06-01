def create_augmented(matrix1, matrix2, size):
    augmented_matrix = []

    for index in range(0, size):
        augmented_matrix.append(matrix1[index])
        augmented_matrix[index].append(matrix2[index])

    return augmented_matrix


def get_pivot_position(row):
    for i in range(0, len(row)):
        if row[i] != 0:
            return True, i
    return False, -1


def is_echelon(matrix):
    pivot_position_previous_row = -1

    for row in matrix:
        exist_pivot, pivot_position = get_pivot_position(row)
        if not exist_pivot:
            pivot_position_previous_row = len(row)
        elif pivot_position <= pivot_position_previous_row:
            return False
        else:
            pivot_position_previous_row = pivot_position

    return True


def find_row_with_leftmost_pivot(matrix):
    leftmost_pivot_position = len(matrix[0])
    row_with_leftmost_pivot = 0

    for row in range(0, len(matrix)):
        exist_pivot, pivot_position = get_pivot_position(matrix[row])

        if exist_pivot and pivot_position < leftmost_pivot_position:
            leftmost_pivot_position = pivot_position
            row_with_leftmost_pivot = row

    return row_with_leftmost_pivot


def linear_combination(row1, row2, fact):
    comb = [0] * len(row1)

    for index in range(0, len(row1)):
        comb[index] = row1[index] + fact * row2[index]
        if abs(comb[index]) <= pow(10, -10):
            comb[index] = 0

    return comb


def get_echelon_form(matrix, augmented_matrix):
    if is_echelon(matrix):
        return matrix

    row_has_leftmost_pivot = find_row_with_leftmost_pivot(matrix)
    matrix[0], matrix[row_has_leftmost_pivot] = matrix[row_has_leftmost_pivot], matrix[0]

    exist_pivot, pivot_position_first_row = get_pivot_position(matrix[0])

    if not exist_pivot:
        print("Error 1 in get_echelon_form")
        exit(1)

    for row in range(1, len(matrix)):
        exist_pivot_in_row, pivot_position_in_row = get_pivot_position(matrix[row])

        if not exist_pivot_in_row:
            continue
        if pivot_position_in_row < pivot_position_first_row:
            print("Error 2 in get_echelon_form")
            exit(1)

        if pivot_position_first_row == pivot_position_in_row:
            matrix[row] = linear_combination(matrix[row], matrix[0],
                                             -1 * matrix[row][pivot_position_in_row] / matrix[0][
                                                 pivot_position_first_row])

    echelon_form = [matrix[0]]

    # for displaying step by step
    n = len(augmented_matrix) - len(matrix)
    augmented_matrix[n] = matrix[0]
    print("Step", n + 1)
    print_matrix(augmented_matrix[0:n] + matrix)

    echelon_form.extend(get_echelon_form(matrix[1:], augmented_matrix))

    return echelon_form


def get_reduced_echelon_form(matrix):
    for index in range(0, len(matrix)):
        exist_pivot, pivot_position = get_pivot_position(matrix[index])
        if not exist_pivot:
            continue

        fact = matrix[index][pivot_position]
        for column in range(0, len(matrix[index])):
            matrix[index][column] = matrix[index][column] / fact

    for row in range(len(matrix) - 1, 0, -1):
        exist_pivot, pivot_position = get_pivot_position(matrix[row])
        if not exist_pivot:
            continue

        for second_row in range(row - 1, -1, -1):
            matrix[second_row] = linear_combination(matrix[second_row], matrix[row],
                                                    -1 * matrix[second_row][pivot_position])

    return matrix


def print_answers(constants):
    for row in range(0, len(constants)):
        print('\nX' + str(row + 1) + '\t\t\t', end='')
        print('%.2f' % constants[row] + '\t\t', end='')

    print("\n\n")


def print_matrix(matrix):
    for row in matrix:
        for elem in row:
            print('%.2f\t' % elem, end='')
        print()
    print("\n")


def print_answers_parametric(constants, free_variables):
    print('\n\nfactor\t\t1\t\t', end='')
    for index in range(0, len(free_variables)):
        print('\tX' + free_variables[index][0] + '\t\t', end='')

    for row in range(0, len(constants)):
        print('\nX' + str(row + 1) + '\t\t', end='')
        print('%.2f' % constants[row] + '\t\t', end='')
        for index in range(0, len(free_variables)):
            print('%.2f' % free_variables[index][row + 1] + '\t\t', end='')

    print("\n\n")


def get_answers(matrix):
    constants = []
    for index in range(0, len(matrix)):
        constants.append(matrix[index][len(matrix[index]) - 1])

    free_variables = []

    for index in range(0, len(matrix)):
        exist_pivot, pivot_position = get_pivot_position(matrix[index])
        if not exist_pivot:
            temp = [str((index + 1))]
            for row in range(0, len(matrix)):
                temp.append(matrix[row][index] * -1)

            temp[index + 1] = 1

            free_variables.append(temp)
        else:
            if pivot_position == len(matrix) :
                print("This system of linear equations has no answer :( ")
                return

    if len(free_variables) > 0:
        print_answers_parametric(constants, free_variables)
    else:
        print_answers(constants)


def main():
    n = int(input())
    A = []
    B = []

    # get A
    for i in range(0, n):
        A.append([float(j) for j in input().split()])

    # get B
    temp = input().split()
    for i in range(0, n):
        B.append(float(temp[i]))

    augmented_matrix = create_augmented(A, B, n)

    print("\n\nAugmented matrix : \n")
    print_matrix(augmented_matrix)
    print("\n\n")

    echelon_form = get_echelon_form(augmented_matrix, augmented_matrix)

    print("Echelon form of matrix : \n")
    print_matrix(echelon_form)
    print("\n\n")

    reduced_echelon_form = get_reduced_echelon_form(echelon_form)

    print("Reduced echelon form of matrix : \n")
    print_matrix(reduced_echelon_form)
    print("\n\n")

    print("Finally :D ")
    get_answers(reduced_echelon_form)


main()
