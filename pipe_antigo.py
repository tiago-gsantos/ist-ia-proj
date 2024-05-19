# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 13:
# 106059 Lara Faria
# 106329 Tiago Santos

import numpy as np
import copy
from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

adjacent_directions = {
    'FC': [(-1, 0)],
    'FB': [(1, 0)],
    'FD': [(0, 1)],
    'FE': [(0, -1)],
    'VC': [(-1, 0), (0, -1)],
    'VB': [(1, 0), (0, 1)],
    'VD': [(0, 1), (-1, 0)],
    'VE': [(0, -1), (1, 0)],
    'BC': [(-1, 0), (0, -1), (0, 1)],
    'BB': [(1, 0), (0, 1), (0, -1)],
    'BD': [(0, 1), (-1, 0), (1, 0)],
    'BE': [(0, -1), (1, 0), (-1, 0)],
    'LH': [(0, 1), (0, -1)],    
    'LV': [(1, 0), (-1, 0)],    
}

num_connections = {
    'F': 1,
    'V': 2,
    'B': 3,
    'L': 2
}

piece_rot = {
    'F': ['FC', 'FD', 'FB', 'FE'],
    'V': ['VC', 'VD', 'VB', 'VE'],
    'B': ['BC', 'BD', 'BB', 'BE'],
    'L': ['LV', 'LH', 'LV']
}

directions_rot = {
    'C': 0, 'D': 1, 'B': 2, 'E': 3, 
    'V': 0, 'H': 1
}

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    """Utilizado em caso de empate na gestão da lista de abertos nas procuras informadas."""
    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, board_array, dim):
        self.board_array = board_array
        self.dim = dim

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if not (0 <= row < self.dim and 0 <= col < self.dim):
            return None
        return self.board_array[row][col][:2]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row-1, col), self.get_value(row+1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col-1), self.get_value(row, col+1))
    
    def adjacent_positions(self, row: int, col: int):
        directions = adjacent_directions[self.get_value(row, col)]
        positions = []
        for i in directions:
            p = (row + i[0], col + i[1])
            if (self.get_value(p[0], p[1]) != None):
                positions.append(p)
        return positions

    def num_piece_connections(self, row: int, col: int):
        num_connections = 0
        adjacent = self.adjacent_positions(row, col)

        for position in adjacent:
            adjacent_adjacent = self.adjacent_positions(position[0], position[1])
            if((row, col) in adjacent_adjacent):
                num_connections += 1
        return num_connections

    def count_board_connections(self):
        self.total_connections = 0
        self.current_connections = 0
        
        for row in range(self.dim):
            for col in range(self.dim):
                self.total_connections += num_connections[self.board_array[row][col][0]]
                self.current_connections += self.num_piece_connections(row, col)

        return self


    def rotate_piece(self, row: int, col: int, rot: int):
        new_board = copy.deepcopy(self)

        piece = new_board.get_value(row, col)
        rotated_piece = piece_rot[piece[0]][(directions_rot[piece[1]] + rot)%4]
        new_board.board_array[row][col] = rotated_piece + '1' + piece[3]
        
        self.change_adjacents(row, col)

        connections = self.num_piece_connections(row, col)
        new_connections = new_board.num_piece_connections(row, col)

        new_board.current_connections += 2*(new_connections - connections)

        return new_board
    
    def change_adjacents(self, row: int, col: int):
        pieces = self.adjacent_positions(row, col)
        
        for piece in pieces:
            piece[3] = chr(ord(piece[3]) + 1)
        return

    def solve_initial_pieces(self):
        dim = self.dim - 1
        if(self.board_array[0][0][0] == 'V'):
            self.board_array[0][0] = 'VB1' + self.board_array[0][0][3]
            self.change_adjacents(0, 0)

        if(self.board_array[0][dim][0] == 'V'):
            self.board_array[0][dim] = 'VE1' + self.board_array[0][dim][3]
            self.change_adjacents(0, dim)

        if(self.board_array[dim][0][0] == 'V'):
            self.board_array[dim][0] = 'VD1' + self.board_array[dim][0][3]
            self.change_adjacents(dim, 0)

        if(self.board_array[dim][dim][0] == 'V'):
            self.board_array[dim][dim] = 'VC1' + self.board_array[dim][dim][3]
            self.change_adjacents(dim, dim)
        
        for i in range(1, dim):
            if(self.board_array[0][i][0] == 'L'):
                self.board_array[0][i] = 'LH1' + self.board_array[0][i][3]
                self.change_adjacents(0, i)

            elif(self.board_array[0][i][0] == 'B'):
                self.board_array[0][i] = 'BB1' + self.board_array[0][i][3]
                self.change_adjacents(0, i)

            
            if(self.board_array[dim][i][0] == 'L'):
                self.board_array[dim][i] = 'LH1' + self.board_array[dim][i][3]
                self.change_adjacents(dim, i)

            elif(self.board_array[dim][i][0] == 'B'):
                self.board_array[dim][i] = 'BC1' + self.board_array[dim][i][3]
                self.change_adjacents(dim, i)


            if(self.board_array[i][0][0] == 'L'):
                self.board_array[i][0] = 'LV1' + self.board_array[i][0][3]
                self.change_adjacents(i, 0)

            elif(self.board_array[i][0][0] == 'B'):
                self.board_array[i][0] = 'BD1' + self.board_array[i][0][3]
                self.change_adjacents(i, 0)

            
            if(self.board_array[i][dim][0] == 'L'):
                self.board_array[i][dim] = 'LV1' + self.board_array[i][dim][3]
                self.change_adjacents(i, dim)

            elif(self.board_array[i][dim][0] == 'B'):
                self.board_array[i][dim] = 'BE1' + self.board_array[i][dim][3]
                self.change_adjacents(i, dim)

        return self

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        
        line = stdin.readline().split()
        
        n = len(line)
        
        board = np.ndarray((n, n), dtype='U4')
        
        for i, elem in enumerate(line):
            board[0, i] = elem + '00'

        for i in range(1, n):
            line = stdin.readline().split()
            for j, elem in enumerate(line):
                board[i, j] = elem + '00'
        
        return Board(board, n).solve_initial_pieces().count_board_connections()
    
    def print_board(self):
        for line in self.board_array:
            modified_line = [elem[:2] for elem in line]
            print('\t'.join(map(str, modified_line)))
        print()

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(PipeManiaState(board))

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        """
        1 - 90º sentido horário
        2 - 180º
        -1 - 90º sentido anti-horário
        """
        possible_actions = []

        for row in range(state.board.dim):
            for col in range(state.board.dim):
                if(state.board.board_array[row][col][2] == '0'):
                    if(state.board.board_array[row][col][0] == 'L'):
                        possible_actions.extend([(row, col, 1)])
                    else:
                        possible_actions.extend([(row, col, 1), (row, col, 2), (row, col, -1)])

        return possible_actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        (row, col, rot) = action
        
        return PipeManiaState(state.board.rotate_piece(row, col, rot))

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if (state.board.current_connections == state.board.total_connections):
            return True
        return False

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return node.state.board.total_connections - node.state.board.current_connections

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler o ficheiro do standard input,
    board = Board.parse_instance()
    pipeMania = PipeMania(board)
    goal = greedy_search(pipeMania)
    goal.state.board.print_board()

    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
