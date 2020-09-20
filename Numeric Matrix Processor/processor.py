from textwrap import dedent


class Matrix:
    error = "The operation cannot be performed."
    main_menu = '''
            1. Add matrices
            2. Multiply matrix by a constant
            3. Multiply matrices
            4. Transpose matrix
            5. Calculate a determinant
            6. Inverse matrix
            0. Exit
            Your choice is:
            '''

    transpose_menu = '''
            1. Main diagonal
            2. Side diagonal
            3. Vertical line
            4. Horizontal line
            Your choice is: 
            '''

    def request_matrix(self, ord=''):
        print(f"Enter size of {ord + ' ' if type(ord) == str else ''}matrix: ")
        rows, cols = [int(x) for x in input().split()]

        print(f"Enter the {ord + ' ' if type(ord) == str else ''}matrix: ")
        M = self.create_matrix(rows)
        return rows, cols, M

    def create_matrix(self, n_row: int):
        M = []
        for i in range(n_row):
            row = [float(x) if "." in x else int(x) for x in input().split()]
            M.append([])
            for j in row:
                M[i].append(j)
        return M

    def add_matrices(self, M_1, M_2):
        if len(M_1) != len(M_2) and len(M_1[0]) != len(M_2[0]):
            return None
        else:
            M = []
            for i, v in enumerate(M_1):
                M.append([])
                for j, val in enumerate(v):
                    M[i].append(val + M_2[i][j])
            return M

    def scale_matrix(self, M, scalar):
        scaled = []
        for i, row in enumerate(M):
            scaled.append([])
            for j in row:
                scaled[i].append(j * scalar)
        return scaled

    def matrix_by_matrix(self, M_1, M_2, n_col):
        M_3 = []
        for rm_1 in M_1:
            r = []
            for n in range(n_col):
                cm_2 = []
                for rm_2 in M_2:
                    cm_2.append(rm_2[n])
                s = sum(map(lambda x, y: x * y, rm_1, cm_2))
                r.append(s)
            M_3.append(r)
        return M_3

    def main_diag_transpose(self, M):
        M_t = []
        n = len(M)
        for i in range(n):
            row = []
            for r in M:
                row.append(r[i])
            M_t.append(row)
        return M_t

    def side_diag_transpose(self, M):
        M_t = []
        M.reverse()
        for i in range(len(M)):
            row = []
            for r in M:
                r.reverse()
                row.append(r[i])
            M_t.append(row)
        return M_t

    def vert_line_transpose(self, M):
        return [row[::-1] for row in M]

    def horiz_line_transpose(self, M):
        return M[::-1]

    def determinant(self, M):
        if len(M) == 1:
            return M[0][0]
        det = 0
        for i, el in enumerate(M[0]):
            sign = pow(-1, i + 2)
            if len(M) == 2 and len(M[0]) == 2:
                return M[0][0] * M[1][1] - M[0][1] * M[1][0]
            else:
                minor = self.matrix_minor(M, 0, i)
                det += el * sign * self.determinant(minor)
        return det

    def matrix_minor(self, M, i, j):
        return [row[:j] + row[j + 1:] for row in M[:i] + M[i + 1:]]

    def cofactors(self, M):
        cofactors = []
        for r in range(len(M)):
            cofactor_row = []
            for c in range(len(M)):
                minor = self.matrix_minor(M, r, c)
                cofactor_row.append(((-1) ** (r + c)) * self.determinant(minor))
            cofactors.append(cofactor_row)
        return cofactors

    def inverse_matrix(self, M):
        det = self.determinant(M)
        if det == 0:
            return "This matrix doesn't have an inverse."
        scalar = 1 / det
        cofactors_t = self.main_diag_transpose(self.cofactors(M))
        return self.scale_matrix(cofactors_t, scalar)

    def print_matrix(self, M):
        print("The result is:")
        for row in M:
            print(*row)

    def start(self):
        while True:
            print(dedent(Matrix.main_menu))
            option = input()
            if option == "0":
                break

            # Addition
            elif option == "1":
                rows_1, cols_1, M_1 = self.request_matrix("first")
                rows_1, cols_1, M_2 = self.request_matrix("second")
                addition = self.add_matrices(M_1, M_2)
                if not addition:
                    print(Matrix.error, end="\n\n")
                    continue
                else:
                    self.print_matrix(addition)
                continue

            # Scalar multiplication
            elif option == "2":
                rows, cols, M = self.request_matrix()
                print("Enter constant: ")
                constant = input()
                constant = float(constant) if "." in constant else int(constant)
                scaled = self.scale_matrix(M, constant)
                self.print_matrix(scaled)
                continue

            # Matrix multiplication
            elif option == "3":
                rows_1, cols_1, M_1 = self.request_matrix("first")
                rows_2, cols_2, M_2 = self.request_matrix("second")
                if cols_1 != rows_2:
                    print(Matrix.error, end="\n\n")
                    continue
                else:
                    self.print_matrix(self.matrix_by_matrix(M_1, M_2, cols_2))
                    continue

            elif option == "4":
                while True:
                    print(dedent(Matrix.transpose_menu))
                    option = input()

                    # Main diagonal
                    if option == "1":
                        rows, cols, M = self.request_matrix()
                        self.print_matrix(self.main_diag_transpose(M))
                        break

                    # Side diagonal
                    elif option == "2":
                        rows, cols, M = self.request_matrix()
                        self.print_matrix(self.side_diag_transpose(M))
                        break

                    # Vertical line
                    elif option == "3":
                        rows, cols, M = self.request_matrix()
                        self.print_matrix(self.vert_line_transpose(M))
                        break

                    # Horizontal line
                    elif option == "4":
                        rows, cols, M = self.request_matrix()
                        self.print_matrix(self.horiz_line_transpose(M))
                        break

                    else:
                        continue

            # Determinant
            elif option == "5":
                rows, cols, M = self.request_matrix()
                print(self.determinant(M))
                continue

            # Inverse matrix
            elif option == "6":
                rows, cols, M = self.request_matrix()
                res = self.inverse_matrix(M)
                if type(res) == str:
                    print(res)
                else:
                    self.print_matrix(res)
                continue

            else:
                continue


Matrix().start()
