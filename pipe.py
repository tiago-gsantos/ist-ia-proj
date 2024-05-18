# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 13:
# 106059 Lara Faria
# 106329 Tiago Santos

import numpy as np
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


    def adjacent_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima, abaixo, à esquerda e 
        à direita respectivamente."""
        pass

    def rotate_piece(self, row: int, col: int, rot: str):
        pass
    
    def calculate_possible_rotations(self, row: int, col: int):
        pass

    def calculate_initial_state(self):       
        self.possible_rotations = ()
        self.remaining_pieces = []

        for row in range(self.dim):
            row_possibilities = ()
            
            for col in range(self.dim):
                rotations = self.calculate_possible_rotations(row, col)
                row_possibilities += (rotations, )
                
                if(len(rotations) == 1):
                    self.remaining_pieces.insert(0, (row, col))
                else:
                    self.remaining_pieces.append((row, col))

            self.possible_rotations += (row_possibilities, )

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
            print('\t'.join(map(str, line)))
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
            possible_actions.extend(row, col, rot)
        
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
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        pass


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
