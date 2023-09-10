from Board import BoardUtility
import random
import copy


class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=2):
        super().__init__(player_piece)
        self.depth = depth

    def utility_func(self, board):
        val = 0
        for row in range(6):
            for col in range(4):
                if board[row][col] == 1 and board[row][col + 1] == 1 and board[row][col + 2] == 1:
                    val += 100
                if board[row][col] == 2 and board[row][col + 1] == 2 and board[row][col + 2] == 2:
                    val -= 100 / 2
            
            for col in range(3):
                if board[row][col] == 1 and board[row][col + 1] == 1 and board[row][col + 2] == 1 and board[row][col + 3] == 1:
                    val += 400
                if board[row][col] == 2 and board[row][col + 1] == 2 and board[row][col + 2] == 2 and board[row][col + 3] == 2:
                    val -= 400 / 2


        for col in range(6):
            for row in range(4):
                if board[row][col] == 1 and board[row + 1][col] == 1 and board[row + 2][col] == 1:
                    val += 100
                if board[row][col] == 2 and board[row + 1][col] == 2 and board[row + 2][col] == 2:
                    val -= 100 / 2
            
            for row in range(3):
                if board[row][col] == 1 and board[row + 1][col] == 1 and board[row + 2][col] == 1 and board[row + 3][col] == 1:
                    val += 400
                if board[row][col] == 2 and board[row + 1][col] == 2 and board[row + 2][col] == 2 and board[row + 3][col] == 2:
                    val -= 400 / 2
        
        # big movarab 1
        for row in range(4):
            if board[row][row] == 1 and board[row + 1][row + 1] == 1 and board[row + 2][row + 2] == 1:
                    val += 50
            if board[row][row] == 2 and board[row + 1][row + 1] == 2 and board[row + 2][row + 2] == 2:
                val -= 50 / 2

        for row in range(3):
            if board[row][row] == 1 and board[row + 1][row + 1] == 1 and board[row + 2][row + 2] == 1 and board[row + 3][row + 3] == 1:
                    val += 200
            if board[row][row] == 2 and board[row + 1][row + 1] == 2 and board[row + 2][row + 2] == 2 and board[row + 3][row + 3] == 2:
                val -= 200 / 2

        # big movarab 2
        for row in range(4):
            if board[row][5 - row] == 1 and board[row + 1][4 - row] == 1 and board[row + 2][3 - row] == 1:
                    val += 50
            if board[row][5 - row] == 2 and board[row + 1][4 - row] == 2 and board[row + 2][3 - row] == 2:
                val -= 50 / 2

        for row in range(3):
            if board[row][5 - row] == 1 and board[row + 1][4 - row] == 1 and board[row + 2][3 - row] == 1 and board[row + 3][2 - row] == 1:
                    val += 200
            if board[row][5 - row] == 2 and board[row + 1][4 - row] == 2 and board[row + 2][3 - row] == 2 and board[row + 3][2 - row] == 2:
                val -= 200 / 2
        
        # small movarab 1
        for row in range(3):
            if board[row][row + 1] == 1 and board[row + 1][row + 2] == 1 and board[row + 2][row + 3] == 1:
                val += 50
            if board[row][row + 1] == 2 and board[row + 1][row + 2] == 2 and board[row + 2][row + 3] == 2:
                val -= 50 / 2

        for row in range(2):
            if board[row][row + 1] == 1 and board[row + 1][row + 2] == 1 and board[row + 2][row + 3] == 1 and board[row + 3][row + 4] == 1:
                val += 200
            if board[row][row + 1] == 2 and board[row + 1][row + 2] == 2 and board[row + 2][row + 3] == 2 and board[row + 3][row + 4] == 2:
                val -= 200 / 2

        # small movarab 2
        for row in range(3):
            if board[row + 1][row] == 1 and board[row + 2][row + 1] == 1 and board[row + 3][row + 2] == 1:
                val += 50
            if board[row + 1][row] == 2 and board[row + 2][row + 1] == 2 and board[row + 3][row + 2] == 2:
                val -= 50 / 2

        for row in range(2):
            if board[row + 1][row] == 1 and board[row + 2][row + 1] == 1 and board[row + 3][row + 2] == 1 and board[row + 4][row + 3] == 1:
                val += 200
            if board[row + 1][row] == 2 and board[row + 2][row + 1] == 2 and board[row + 3][row + 2] == 2 and board[row + 4][row + 3] == 2:
                val -= 200 / 2


        # small movarab 3
        for row in range(3):
            if board[row][4 - row] == 1 and board[row + 1][3 - row] == 1 and board[row + 2][2 - row] == 1:
                val += 50
            if board[row][4 - row] == 2 and board[row + 1][3 - row] == 2 and board[row + 2][2 - row] == 2:
                val -= 50 / 2

        for row in range(2):
            if board[row][4 - row] == 1 and board[row + 1][3 - row] == 1 and board[row + 2][2 - row] == 1 and board[row + 3][1- row] == 1:
                val += 200
            if board[row][4 - row] == 2 and board[row + 1][3 - row] == 2 and board[row + 2][2 - row] == 2 and board[row + 3][1 - row] == 2:
                val -= 200 / 2

         # small movarab 4
        for row in range(3):
            if board[row + 1][5 - row] == 1 and board[row + 2][4 - row] == 1 and board[row + 3][3 - row] == 1:
                val += 50
            if board[row + 1][5 - row] == 2 and board[row + 2][4 - row] == 2 and board[row + 3][3 - row] == 2:
                val -= 50 / 2

        for row in range(2):
            if board[row + 1][5 - row] == 1 and board[row + 2][4 - row] == 1 and board[row + 3][3 - row] == 1 and board[row + 4][2 - row] == 1:
                val += 200
            if board[row + 1][5 - row] == 2 and board[row + 2][4 - row] == 2 and board[row + 3][3 - row] == 2 and board[row + 4][2 - row] == 2:
                val -= 200 / 2

        return val

    def dfs(self,remained_depth, board, player_number, alpha, beta):
        
        ret = []
        inf = 100000
        infm = -200000
        tmp_board = copy.deepcopy(board)
        finished = BoardUtility.is_terminal_state(tmp_board)
        if finished:
            if BoardUtility.is_draw(tmp_board):
                return ret, 0
            elif BoardUtility.has_player_won(tmp_board, 1):
                return ret, inf
            else: 
                return ret, infm
        
        if remained_depth == 0:
            # TODO
            #print ("salam111 " + str(remained_depth))
            uf = self.utility_func(board)
            #uf = 10
            return ret, uf

        
        valid_locations = BoardUtility.get_valid_locations(tmp_board)


        final_move = []
        if player_number == 1:
            v = infm
            bbb = True
            for loc in valid_locations:
                #print ("salam " + str(remained_depth) + ' ' + str(loc))
                if bbb == False:
                    break
                for i in range(4):
                    rg = i + 1
                    # skip rotation
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "skip", 1)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "skip"]
                    if v <= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    alpha = max(alpha, v)
                    if alpha >= beta:
                        bbb = False
                        break
                    # clockwise
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "clockwise", 1)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "clockwise"]
                    if v <= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    alpha = max(alpha, v)
                    if alpha >= beta:
                        bbb = False
                        break
                    # anticlockwise
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "anticlockwise", 1)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "anticlockwise"]
                    if v <= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    alpha = max(alpha, v)
                    if alpha >= beta:
                        bbb = False
                        break
            return final_move, v
        
        else:
            v = inf
            bbb = True
            for loc in valid_locations:
                #print ("salam " + str(remained_depth) + ' ' + str(loc))
                if bbb == False:
                    break
                for i in range(4):
                    rg = i + 1
                    # skip rotation
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "skip", 2)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "skip"]
                    if v >= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    beta = min(beta, v)
                    if alpha >= beta:
                        bbb = False
                        break
                    # clockwise
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "clockwise", 2)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "clockwise"]
                    if v >= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    beta = min(beta, v)
                    if alpha >= beta:
                        bbb = False
                        break
                    # anticlockwise
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "anticlockwise", 2)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "anticlockwise"]
                    if v >= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    beta = min(beta, v)
                    if alpha >= beta:
                        bbb = False
                        break
            return final_move, v
            
        

    
    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        inf = 100000
        infm = -200000
        alpha = copy.copy(infm)
        beta = copy.copy(inf)
        move, g = self.dfs(self.depth, board, 1, alpha, beta)
        

        row = move[0]
        col = move[1]
        rg = move[2]
        rotation = move[3]
        region = copy.copy(rg)

        print (g)
        return [[row, col], region, rotation]


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=2, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def utility_func(self, board):
        val = 0
        for row in range(6):
            for col in range(4):
                if board[row][col] == 1 and board[row][col + 1] == 1 and board[row][col + 2] == 1:
                    val += 100
                if board[row][col] == 2 and board[row][col + 1] == 2 and board[row][col + 2] == 2:
                    val -= 100 / 2
            
            for col in range(3):
                if board[row][col] == 1 and board[row][col + 1] == 1 and board[row][col + 2] == 1 and board[row][col + 3] == 1:
                    val += 400
                if board[row][col] == 2 and board[row][col + 1] == 2 and board[row][col + 2] == 2 and board[row][col + 3] == 2:
                    val -= 400 / 2


        for col in range(6):
            for row in range(4):
                if board[row][col] == 1 and board[row + 1][col] == 1 and board[row + 2][col] == 1:
                    val += 100
                if board[row][col] == 2 and board[row + 1][col] == 2 and board[row + 2][col] == 2:
                    val -= 100 / 2
            
            for row in range(3):
                if board[row][col] == 1 and board[row + 1][col] == 1 and board[row + 2][col] == 1 and board[row + 3][col] == 1:
                    val += 400
                if board[row][col] == 2 and board[row + 1][col] == 2 and board[row + 2][col] == 2 and board[row + 3][col] == 2:
                    val -= 400 / 2
        
        # big movarab 1
        for row in range(4):
            if board[row][row] == 1 and board[row + 1][row + 1] == 1 and board[row + 2][row + 2] == 1:
                    val += 50
            if board[row][row] == 2 and board[row + 1][row + 1] == 2 and board[row + 2][row + 2] == 2:
                val -= 50 / 2

        for row in range(3):
            if board[row][row] == 1 and board[row + 1][row + 1] == 1 and board[row + 2][row + 2] == 1 and board[row + 3][row + 3] == 1:
                    val += 200
            if board[row][row] == 2 and board[row + 1][row + 1] == 2 and board[row + 2][row + 2] == 2 and board[row + 3][row + 3] == 2:
                val -= 200 / 2

        # big movarab 2
        for row in range(4):
            if board[row][5 - row] == 1 and board[row + 1][4 - row] == 1 and board[row + 2][3 - row] == 1:
                    val += 50
            if board[row][5 - row] == 2 and board[row + 1][4 - row] == 2 and board[row + 2][3 - row] == 2:
                val -= 50 / 2

        for row in range(3):
            if board[row][5 - row] == 1 and board[row + 1][4 - row] == 1 and board[row + 2][3 - row] == 1 and board[row + 3][2 - row] == 1:
                    val += 200
            if board[row][5 - row] == 2 and board[row + 1][4 - row] == 2 and board[row + 2][3 - row] == 2 and board[row + 3][2 - row] == 2:
                val -= 200 / 2
        
        # small movarab 1
        for row in range(3):
            if board[row][row + 1] == 1 and board[row + 1][row + 2] == 1 and board[row + 2][row + 3] == 1:
                val += 50
            if board[row][row + 1] == 2 and board[row + 1][row + 2] == 2 and board[row + 2][row + 3] == 2:
                val -= 50 / 2

        for row in range(2):
            if board[row][row + 1] == 1 and board[row + 1][row + 2] == 1 and board[row + 2][row + 3] == 1 and board[row + 3][row + 4] == 1:
                val += 200
            if board[row][row + 1] == 2 and board[row + 1][row + 2] == 2 and board[row + 2][row + 3] == 2 and board[row + 3][row + 4] == 2:
                val -= 200 / 2

        # small movarab 2
        for row in range(3):
            if board[row + 1][row] == 1 and board[row + 2][row + 1] == 1 and board[row + 3][row + 2] == 1:
                val += 50
            if board[row + 1][row] == 2 and board[row + 2][row + 1] == 2 and board[row + 3][row + 2] == 2:
                val -= 50 / 2

        for row in range(2):
            if board[row + 1][row] == 1 and board[row + 2][row + 1] == 1 and board[row + 3][row + 2] == 1 and board[row + 4][row + 3] == 1:
                val += 200
            if board[row + 1][row] == 2 and board[row + 2][row + 1] == 2 and board[row + 3][row + 2] == 2 and board[row + 4][row + 3] == 2:
                val -= 200 / 2


        # small movarab 3
        for row in range(3):
            if board[row][4 - row] == 1 and board[row + 1][3 - row] == 1 and board[row + 2][2 - row] == 1:
                val += 50
            if board[row][4 - row] == 2 and board[row + 1][3 - row] == 2 and board[row + 2][2 - row] == 2:
                val -= 50 / 2

        for row in range(2):
            if board[row][4 - row] == 1 and board[row + 1][3 - row] == 1 and board[row + 2][2 - row] == 1 and board[row + 3][1- row] == 1:
                val += 200
            if board[row][4 - row] == 2 and board[row + 1][3 - row] == 2 and board[row + 2][2 - row] == 2 and board[row + 3][1 - row] == 2:
                val -= 200 / 2

         # small movarab 4
        for row in range(3):
            if board[row + 1][5 - row] == 1 and board[row + 2][4 - row] == 1 and board[row + 3][3 - row] == 1:
                val += 50
            if board[row + 1][5 - row] == 2 and board[row + 2][4 - row] == 2 and board[row + 3][3 - row] == 2:
                val -= 50 / 2

        for row in range(2):
            if board[row + 1][5 - row] == 1 and board[row + 2][4 - row] == 1 and board[row + 3][3 - row] == 1 and board[row + 4][2 - row] == 1:
                val += 200
            if board[row + 1][5 - row] == 2 and board[row + 2][4 - row] == 2 and board[row + 3][3 - row] == 2 and board[row + 4][2 - row] == 2:
                val -= 200 / 2

        return val

    def dfs(self,remained_depth, board, player_number, alpha, beta):
        
        ret = []
        inf = 100000
        infm = -200000
        tmp_board = copy.deepcopy(board)
        finished = BoardUtility.is_terminal_state(tmp_board)
        if finished:
            if BoardUtility.is_draw(tmp_board):
                return ret, 0
            elif BoardUtility.has_player_won(tmp_board, 1):
                return ret, inf
            else: 
                return ret, infm
        
        if remained_depth == 0:
            # TODO
            #print ("salam111 " + str(remained_depth))
            uf = self.utility_func(board)
            #uf = 10
            return ret, uf

        
        valid_locations = BoardUtility.get_valid_locations(tmp_board)


        final_move = []
        if player_number == 1:
            v = infm
            bbb = True
            for loc in valid_locations:
                #print ("salam " + str(remained_depth) + ' ' + str(loc))
                if bbb == False:
                    break
                for i in range(4):
                    rg = i + 1
                    # skip rotation
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "skip", 1)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "skip"]
                    if v <= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    alpha = max(alpha, v)
                    if alpha >= beta:
                        bbb = False
                        break
                    # clockwise
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "clockwise", 1)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "clockwise"]
                    if v <= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    alpha = max(alpha, v)
                    if alpha >= beta:
                        bbb = False
                        break
                    # anticlockwise
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "anticlockwise", 1)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "anticlockwise"]
                    if v <= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    alpha = max(alpha, v)
                    if alpha >= beta:
                        bbb = False
                        break
            return final_move, v
        
        else:
            v = inf
            bbb = True
            for loc in valid_locations:
                #print ("salam " + str(remained_depth) + ' ' + str(loc))
                if bbb == False:
                    break
                for i in range(4):
                    rg = i + 1
                    # skip rotation
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "skip", 2)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "skip"]
                    if v >= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    beta = min(beta, v)
                    if alpha >= beta:
                        bbb = False
                        break
                    # clockwise
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "clockwise", 2)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "clockwise"]
                    if v >= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    beta = min(beta, v)
                    if alpha >= beta:
                        bbb = False
                        break
                    # anticlockwise
                    tmp_board = copy.deepcopy(board)
                    BoardUtility.make_move(tmp_board, loc[0], loc[1], rg, "anticlockwise", 2)
                    move, u = self.dfs(remained_depth - 1, tmp_board, 3 - player_number, alpha, beta)
                    move1 = [loc[0], loc[1], rg, "anticlockwise"]
                    if v >= u:
                        v = u
                        final_move = copy.deepcopy(move1)
                    beta = min(beta, v)
                    if alpha >= beta:
                        bbb = False
                        break
            return final_move, v
            
    


    
    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        inf = 100000
        infm = -200000
        alpha = copy.copy(infm)
        beta = copy.copy(inf)

        if random.random() < self.prob_stochastic:
            return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]

        move, g = self.dfs(self.depth, board, 1, alpha, beta)
        

        row = move[0]
        col = move[1]
        rg = move[2]
        rotation = move[3]
        region = copy.copy(rg)

        print (g)
        return [[row, col], region, rotation]