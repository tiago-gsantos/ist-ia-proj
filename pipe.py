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
        self.is_valid = True

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if not (0 <= row < self.dim and 0 <= col < self.dim):
            return None
        return self.board_array[row][col]

    def adjacent_positions(self, row: int, col: int):
        """Devolve os valores imediatamente acima, abaixo, à esquerda e 
        à direita respectivamente."""
        return [self.get_value(row - 1, col), self.get_value(row + 1, col),
                self.get_value(row, col - 1), self.get_value(row, col + 1)]

    def adjacent_connections(self, row: int, col: int):
        directions = adjacent_directions[self.get_value(row, col)[:2]]
        positions = []
        for dir in directions:
            pos = (row + dir[0], col + dir[1])
            if (self.get_value(pos[0], pos[1]) != None):
                positions.append(pos)
        return positions
        
    def update_adjacent(self, adj_positions):
        for pos in adj_positions:
            r, c = pos
            if(self.get_value(r, c) != None and self.get_value(r, c)[2] != '1'):
                old_possibilities = len(self.possible_rotations[r][c])

                new_rotations = self.calculate_possible_rotations(r, c)

                new_possibilities = len(new_rotations)
                
                if(new_possibilities == 0):
                    self.is_valid = False
                    return
                
                if(new_possibilities == 1 and old_possibilities != 1):
                    self.remaining_pieces.remove((r, c))
                    self.remaining_pieces.insert(0, (r, c))
                
                self.possible_rotations[r][c] = new_rotations
                self.total_possibilities += (new_possibilities - old_possibilities)

    def rotate_piece(self, row: int, col: int, rot: str):
        new_board = copy.deepcopy(self)

        new_board.board_array[row][col] = rot + '1'
        
        del new_board.remaining_pieces[0]

        adj_positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        new_board.update_adjacent(adj_positions)
        
        return new_board


    def calculate_possible_rotations(self, row: int, col: int):
        piece = self.get_value(row, col)
        possible_rotations = piece_rot[piece[0]].copy()
        adj_positions = self.adjacent_positions(row, col)


        if(adj_positions[0] in {None, 'LH1', 'VD1', 'VC1', 'BC1', 'FC1', 'FE1', 'FD1'}):
            possible_rotations[0] = ''
            
            if(piece[0] == 'V'): 
                possible_rotations[3] = ''
            elif(piece[0] == 'B'): 
                possible_rotations[2] = ''
                possible_rotations[3] = ''

        elif(adj_positions[0] in {'LV1', 'VE1', 'VB1', 'BB1', 'BE1', 'BD1', 'FB1'}):
            possible_rotations[1] = ''

            if(piece[0] == 'V'):
                possible_rotations[2] = ''
            elif(piece[0] == 'F'):
                possible_rotations[2] = ''
                possible_rotations[3] = ''


        if(adj_positions[1] in {None, 'LH1', 'VB1', 'VE1', 'BB1', 'FB1', 'FE1', 'FD1'}):
            if (piece[0] == 'L'):
                possible_rotations[0] = ''
            else:
                possible_rotations[1] = ''
            
            if(piece[0] == 'V'):
                possible_rotations[2] = ''
            elif(piece[0] == 'B'):
                possible_rotations[2] = ''
                possible_rotations[3] = ''
        
        elif(adj_positions[1] in {'LV1', 'VD1', 'VC1', 'BC1', 'BE1', 'BD1', 'FC1'}):
            if(piece[0] == 'L'):
                possible_rotations[1] = ''
            else:
                possible_rotations[0] = ''

            if(piece[0] == 'V'):
                possible_rotations[3] = ''
            elif(piece[0] == 'F'):
                possible_rotations[2] = ''
                possible_rotations[3] = ''
        

        if(adj_positions[2] in {None, 'LV1', 'VC1', 'VE1', 'BE1', 'FC1', 'FB1', 'FE1'}):
            if(piece[0] == 'L'):
                possible_rotations[1] = ''
            else:
                possible_rotations[2] = ''
            
            if(piece[0] == 'V'):
                possible_rotations[0] = ''
            elif(piece[0] == 'B'):
                possible_rotations[0] = ''
                possible_rotations[1] = ''

        elif(adj_positions[2] in {'LH1', 'VD1', 'VB1', 'BC1', 'BB1', 'BD1', 'FD1'}):
            if(piece[0] == 'L'):
                possible_rotations[0] = ''
            else:
                possible_rotations[3] = ''

            if(piece[0] == 'V'):
                possible_rotations[1] = ''
            elif(piece[0] == 'F'):
                possible_rotations[0] = ''
                possible_rotations[1] = ''

        if(adj_positions[3] in {None, 'LV1', 'VB1', 'VD1', 'BD1', 'FC1', 'FB1', 'FD1'}):
            if(piece[0] == 'L'):
                possible_rotations[1] = ''
            else:
                possible_rotations[3] = ''
            
            if(piece[0] == 'V'):
                possible_rotations[1] = ''
            elif(piece[0] == 'B'):
                possible_rotations[0] = ''
                possible_rotations[1] = ''

        elif(adj_positions[3] in {'LH1', 'VE1', 'VC1', 'BC1', 'BB1', 'BE1', 'FE1'}):
            if(piece[0] == 'L'):
                possible_rotations[0] = ''
            else:
                possible_rotations[2] = ''

            if(piece[0] == 'V'):
                possible_rotations[0] = ''
            elif(piece[0] == 'F'):
                possible_rotations[0] = ''
                possible_rotations[1] = ''

        if(piece[0] == 'F'):
            if(adj_positions[0] != None and adj_positions[0][0] == 'F'):
                possible_rotations[0] = ''
            if(adj_positions[1] != None and adj_positions[1][0] == 'F'):
                possible_rotations[1] = ''
            if(adj_positions[2] != None and adj_positions[2][0] == 'F'):
                possible_rotations[2] = ''
            if(adj_positions[3] != None and adj_positions[3][0] == 'F'):
                possible_rotations[3] = ''

        return list(filter(None, possible_rotations))

    def solve_iteratively(self, pieces):
        while pieces:
            row, col = pieces.pop()
        
            rotations = self.calculate_possible_rotations(row, col)
            num_possibilities = len(rotations)

            if(num_possibilities == 0):
                self.is_valid = False
                return
            
            elif(num_possibilities == 1):
                self.board_array[row][col] = rotations[0] + '1'
                
                try:
                    self.remaining_pieces.remove((row, col))
                except ValueError:
                    pass

                adj_positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                for adj in adj_positions:
                    r, c = adj
                    if(self.get_value(r, c) != None and self.get_value(r, c)[2] != '1'):
                        pieces.append(adj)
        return


    def calculate_initial_state(self):
        self.possible_rotations = []
        self.remaining_pieces = []
        self.total_possibilities = 0

        for row in range(self.dim):
            self.possible_rotations.append([])
            
            for col in range(self.dim):

                if(self.board_array[row][col][2] == '0'):    
                    rotations = self.calculate_possible_rotations(row, col)
                    num_possibilities = len(rotations)

                    if(num_possibilities == 0):
                        self.is_valid = False
                        return self
                    
                    elif(num_possibilities == 1):
                        self.board_array[row][col] = rotations[0] + '1'
                        adj_positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                        adj_pieces = []
                        for adj in adj_positions:
                            r, c = adj
                            if(self.get_value(r, c) != None and self.get_value(r, c)[2] != '1'):
                                adj_pieces.append(adj)
                        self.solve_iteratively(adj_pieces)
                        
                    else:
                        self.remaining_pieces.append((row, col))

                    self.total_possibilities += num_possibilities
                    self.possible_rotations[row].append(rotations)
                else:
                    self.total_possibilities += 1
                    self.possible_rotations[row].append(self.get_value(row, col)[:2])
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

    def dfs(self):
        stack = [(0,0)]
        visited = set()

        while stack:
            piece = stack.pop()
            if piece in visited: continue
            visited.add(piece)
            for adj in self.adjacent_connections(piece[0], piece[1]):
                if(piece in self.adjacent_connections(adj[0], adj[1])):
                    stack.append(adj)
        
        return len(visited)


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(PipeManiaState(board))

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        possible_actions = []

        if(state.board.is_valid == False or len(state.board.remaining_pieces) == 0):
            return possible_actions
        
        row, col = state.board.remaining_pieces[0]
        rotations = state.board.possible_rotations[row][col]
        
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
        
        if(len(state.board.remaining_pieces) != 0):
            return False

        return state.board.dfs() == (state.board.dim * state.board.dim)
    
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return node.state.board.total_possibilities


if __name__ == "__main__":
    board = Board.parse_instance()
    pipeMania = PipeMania(board)
    goal = greedy_search(pipeMania)
    if(goal):
        goal.state.board.print_board()
    else:
        print('Error')
