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


piece_rot = {
    'F': ['FC', 'FB', 'FE', 'FD'],
    'V': ['VC', 'VB', 'VE', 'VD'],
    'B': ['BC', 'BB', 'BE', 'BD'],
    'L': ['LV', 'LH']
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


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, board_array, dim):
        self.board_array = board_array
        self.dim = dim

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if not (0 <= row < self.dim and 0 <= col < self.dim):
            return None
        return self.board_array[row][col]


    def adjacent_positions(self, row: int, col: int):
        """Devolve os valores imediatamente acima, abaixo, à esquerda e 
        à direita respectivamente."""
        adjacents = []
        adjacents.append(self.get_value(row - 1, col))
        adjacents.append(self.get_value(row + 1, col))
        adjacents.append(self.get_value(row, col - 1))
        adjacents.append(self.get_value(row, col + 1))
        return adjacents


    def rotate_piece(self, row: int, col: int, rot: str):
        new_board = copy.deepcopy(self)

        new_board.board_array[row][col] = rot + '1'
        
        del new_board.remaining_pieces[0]

        adj_positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for pos in adj_positions:
            r, c = pos
            if(new_board.get_value(r, c) != None and new_board.get_value(r, c)[2] != '1'):
                new_rotations = new_board.calculate_possible_rotations(r, c)
                new_board.possible_rotations[r][c] = new_rotations
                if(len(new_rotations) == 1):
                    new_board.remaining_pieces.remove((r, c))
                    new_board.remaining_pieces.insert(0, (r, c))

        return new_board


    def calculate_possible_rotations(self, row: int, col: int):
        piece = self.get_value(row, col)
        possible_rotations = piece_rot[piece[0]].copy()
        adj_positions = self.adjacent_positions(row, col)


        if(adj_positions[0] in [None, 'LH1', 'VD1', 'VC1', 'BC1', 'FC1', 'FE1', 'FD1']):
            possible_rotations[0] = ''
            
            if(piece[0] == 'V'): 
                possible_rotations[3] = ''
            elif(piece[0] == 'B'): 
                possible_rotations[2] = ''
                possible_rotations[3] = ''

        elif(adj_positions[0] in ['LV1', 'VE1', 'VB1', 'BB1', 'BE1', 'BD1', 'FB1']):
            possible_rotations[1] = ''

            if(piece[0] == 'V'):
                possible_rotations[2] = ''
            elif(piece[0] == 'F'):
                possible_rotations[2] = ''
                possible_rotations[3] = ''



        if(adj_positions[1] in [None, 'LH1', 'VB1', 'VE1', 'BB1', 'FB1', 'FE1', 'FD1']):
            if (piece[0] == 'L'):
                possible_rotations[0] = ''
            else:
                possible_rotations[1] = ''
            
            if(piece[0] == 'V'):
                possible_rotations[2] = ''
            elif(piece[0] == 'B'):
                possible_rotations[2] = ''
                possible_rotations[3] = ''
        
        elif(adj_positions[1] in ['LV1', 'VD1', 'VC1', 'BC1', 'BE1', 'BD1', 'FC1']):
            if(piece[0] == 'L'):
                possible_rotations[1] = ''
            else:
                possible_rotations[0] = ''

            if(piece[0] == 'V'):
                possible_rotations[3] = ''
            elif(piece[0] == 'F'):
                possible_rotations[2] = ''
                possible_rotations[3] = ''
        

        if(adj_positions[2] in [None, 'LV1', 'VC1', 'VE1', 'BE1', 'FC1', 'FB1', 'FE1']):
            if(piece[0] == 'L'):
                possible_rotations[1] = ''
            else:
                possible_rotations[2] = ''
            
            if(piece[0] == 'V'):
                possible_rotations[0] = ''
            elif(piece[0] == 'B'):
                possible_rotations[0] = ''
                possible_rotations[1] = ''

        elif(adj_positions[2] in ['LH1', 'VD1', 'VB1', 'BC1', 'BB1', 'BD1', 'FD1']):
            if(piece[0] == 'L'):
                possible_rotations[0] = ''
            else:
                possible_rotations[3] = ''

            if(piece[0] == 'V'):
                possible_rotations[1] = ''
            elif(piece[0] == 'F'):
                possible_rotations[0] = ''
                possible_rotations[1] = ''

        if(adj_positions[3] in [None, 'LV1', 'VB1', 'VD1', 'BD1', 'FC1', 'FB1', 'FD1']):
            if(piece[0] == 'L'):
                possible_rotations[1] = ''
            else:
                possible_rotations[3] = ''
            
            if(piece[0] == 'V'):
                possible_rotations[1] = ''
            elif(piece[0] == 'B'):
                possible_rotations[0] = ''
                possible_rotations[1] = ''

        elif(adj_positions[3] in ['LH1', 'VE1', 'VC1', 'BC1', 'BB1', 'BE1', 'FE1']):
            if(piece[0] == 'L'):
                possible_rotations[0] = ''
            else:
                possible_rotations[2] = ''

            if(piece[0] == 'V'):
                possible_rotations[0] = ''
            elif(piece[0] == 'F'):
                possible_rotations[0] = ''
                possible_rotations[1] = ''

        # Verificar quando 2 finais estão ligados

        return list(filter(None, possible_rotations))
    

    def calculate_initial_state(self):
        self.possible_rotations = []
        self.remaining_pieces = []

        for row in range(self.dim):
            row_possibilities = []
            
            for col in range(self.dim):
                
                rotations = self.calculate_possible_rotations(row, col)
                row_possibilities.extend([rotations])
                
                if(len(rotations) == 1):
                    self.remaining_pieces.insert(0, (row, col))
                else:
                    self.remaining_pieces.append((row, col))

            self.possible_rotations.extend([row_possibilities])

        return self

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        line = stdin.readline().split()
        
        n = len(line)
        
        board = np.ndarray((n, n), dtype='U3')
        
        for i, elem in enumerate(line):
            board[0, i] = elem + '0'

        for i in range(1, n):
            line = stdin.readline().split()
            for j, elem in enumerate(line):
                board[i, j] = elem + '0'

        return Board(board, n).calculate_initial_state()

    def print_board(self):
        for line in self.board_array:
            modified_line = [elem[:2] for elem in line]
            print('\t'.join(map(str, modified_line)))
        print()


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(PipeManiaState(board))

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        row, col = state.board.remaining_pieces[0]
        rotations = state.board.possible_rotations[row][col]
        
        possible_actions = []
        
        for rot in rotations:
            possible_actions.extend([(row, col, rot)])
        
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
        #falta DFS
        return len(state.board.remaining_pieces) == 0

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        pass


if __name__ == "__main__":
    # Ler o ficheiro do standard input,
    board = Board.parse_instance()
    pipeMania = PipeMania(board)
    goal = depth_first_tree_search(pipeMania)
    goal.state.board.print_board()
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
