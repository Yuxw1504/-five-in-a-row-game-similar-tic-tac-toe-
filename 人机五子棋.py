def showboard(board):
    # 由于在交互式环境中无法使用os.system('clear')，我们省略这一步，直接打印棋盘
    print("   1  2  3  4  5  6  7  8  9")
    for r in range(9):
        row_data = f"{r+1} "
        for c in range(9):
            if board[r][c] == 0:
                row_data += " + "
            elif board[r][c] == 1:
                row_data += " 黑"
            else:
                row_data += " 白"
        print(row_data)

def is_win(board, row, col, piece):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 水平、垂直、两个对角线方向
    for dx, dy in directions:
        count = 1
        for i in range(1, 5):  # 向前查找
            if 0 <= row + i*dx < 9 and 0 <= col + i*dy < 9 and board[row + i*dx][col + i*dy] == piece:
                count += 1
            else:
                break
        for i in range(1, 5):  # 向后查找
            if 0 <= row - i*dx < 9 and 0 <= col - i*dy < 9 and board[row - i*dx][col - i*dy] == piece:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

def is_tie(board):
    for row in board:
        if 0 in row:
            return False
    return True

def player_move(board):
    while True:
        try:
            player_input = input("你是黑子，请输入你的落子位置（行列，例如：55，表示5行5列）：")
            row, col = int(player_input[0]) - 1, int(player_input[1]) - 1
            if 0 <= row < 9 and 0 <= col < 9 and board[row][col] == 0:
                board[row][col] = 1
                return (row, col)  # 返回玩家的落子位置
            else:
                print("无效输入或位置已被占用，请重新输入！")
        except (ValueError, IndexError):
            print("输入格式错误，请按正确格式输入！")


    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 四个方向：水平、垂直、两个对角线
    total_score = 0
    for dx, dy in directions:
        count = 0  # 当前方向上相同棋子的数量
        for i in range(-4, 5):  # 检查以当前位置为中心，前后四格内的棋子
            nx, ny = row + dx * i, col + dy * i
            if 0 <= nx < 9 and 0 <= ny < 9:
                if board[nx][ny] == player:
                    count += 1
                elif board[nx][ny] != 0:
                    count = 0  # 遇到对方棋子，重置计数
                    break
        total_score += count
    return total_score

    """评估线段中的得分情况"""
    score = 0
    if segment.count(player) == 4 and segment.count(0) == 1:
        score += 1000  # 连成4子
    elif segment.count(player) == 3 and segment.count(0) == 2:
        score += 100  # 连成3子并有两端空位
    return score

    """为特定位置评分，考虑防守和进攻"""
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 水平、垂直、对角线
    for dx, dy in directions:
        line = []
        for i in range(-4, 5):  # 检查以该点为中心，长度为9的线
            nx, ny = row + dx * i, col + dy * i
            if 0 <= nx < 9 and 0 <= ny < 9:
                line.append(board[nx][ny])
            else:
                line.append(None)  # 边界外的位置
        # 评估这条线对当前玩家的得分
        for i in range(5):
            segment = line[i:i+5]
            if None not in segment:
                score += evaluate_line(segment, player)
                if player == 1:  # 额外检查电脑（假设为白棋）的防守需要
                    score += evaluate_line(segment, 2) * 0.5
    return score


    best_score = -1
    best_move = (0, 0)

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:  # 空位
                # 综合评估当前位置的得分，包括进攻和防守
                total_score = evaluate_position(board, r, c)
                if total_score > best_score:
                    best_score = total_score
                    best_move = (r, c)

    # 落子
    board[best_move[0]][best_move[1]] = 2
    return best_move

    def computer_move(board, move_number, last_player_move):
      if move_number == 1:
        # 如果是电脑的第一步，且电脑是后手，优先选择靠近中心但略偏离的位置
        center_positions = [(4, 4), (4, 3), (3, 4), (3, 3)]
        for pos in center_positions:
            if board[pos[0]][pos[1]] == 0:
                board[pos[0]][pos[1]] = 2
                return pos
    
    best_score = -1
    best_move = (0, 0)
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:  # 空位
                # 计算当前位置的得分，以电脑的视角（假定电脑为2号玩家）
                score = score_position(board, r, c, 2)
                # 加大防守分数的权重，防止玩家形成威胁
                player_score = score_position(board, r, c, 1) * 1.2
                total_score = score + player_score
                if total_score > best_score:
                    best_score = total_score
                    best_move = (r, c)
    board[best_move[0]][best_move[1]] = 2
    return best_move

def evaluate_threats(board, row, col):
    """评估给定位置的威胁程度，并根据防守需要进行评分"""
    # 设置评分标准
    scores = {'four': 10000, 'open_three': 5000}
    total_score = 0

    # 检查四个方向上的棋子排列情况
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        for i in range(-4, 5):
            segment = []
            for j in range(5):
                nx, ny = row + (i+j)*dx, col + (i+j)*dy
                if 0 <= nx < 9 and 0 <= ny < 9:
                    segment.append(board[nx][ny])
                else:
                    segment.append(-1)  # 边界外视为阻挡

            if len(segment) == 5:
                if segment.count(1) == 4 and segment.count(0) == 1:
                    total_score += scores['four']
                elif segment.count(1) == 3 and segment.count(0) == 2:
                    if i == 0 or i == 4:  # 检查两端是否开放
                        if (0 <= row - dx < 9 and 0 <= col - dy < 9 and board[row-dx][col-dy] == 0) or \
                           (0 <= row + 5*dx < 9 and 0 <= col + 5*dy < 9 and board[row+5*dx][col+5*dy] == 0):
                            total_score += scores['open_three']

    return total_score

def evaluate_position(board, row, col):
    """评估给定位置的进攻和防守价值"""
    scores = {'four': 10000, 'open_three': 5000, 'three': 1000, 'two': 500}
    defense_score = 0
    offense_score = 0

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        for i in range(-4, 5):
            segment = []
            for j in range(5):
                nx, ny = row + (i+j)*dx, col + (i+j)*dy
                if 0 <= nx < 9 and 0 <= ny < 9:
                    segment.append(board[nx][ny])
                else:
                    segment.append(-1)  # 边界外视为阻挡

            if len(segment) == 5:
                if segment.count(1) == 4 and segment.count(0) == 1:
                    defense_score += scores['four']  # 防守四连
                elif segment.count(2) == 4 and segment.count(0) == 1:
                    offense_score += scores['four']  # 进攻四连
                elif segment.count(1) == 3 and segment.count(0) == 2:
                    if (0 <= row - dx < 9 and 0 <= col - dy < 9 and board[row-dx][col-dy] == 0) or \
                       (0 <= row + 5*dx < 9 and 0 <= col + 5*dy < 9 and board[row+5*dx][col+5*dy] == 0):
                        defense_score += scores['open_three']  # 防守活三
                elif segment.count(2) == 3 and segment.count(0) == 2:
                    if (0 <= row - dx < 9 and 0 <= col - dy < 9 and board[row-dx][col-dy] == 0) or \
                       (0 <= row + 5*dx < 9 and 0 <= col + 5*dy < 9 and board[row+5*dx][col+5*dy] == 0):
                        offense_score += scores['open_three']  # 进攻活三
                # 可以继续添加其他模式的评分

    return defense_score + offense_score

def computer_move(board, last_player_move):
    best_score = -1
    best_move = (0, 0)

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:  # 空位
                # 综合评估当前位置的得分，包括进攻和防守
                total_score = evaluate_position(board, r, c)
                if total_score > best_score:
                    best_score = total_score
                    best_move = (r, c)

    # 落子
    board[best_move[0]][best_move[1]] = 2
    return best_move
    best_score = -1
    best_move = None

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:  # 空位
                # 评估当前空位的得分（考虑进攻和防守）
                total_score = evaluate_position(board, r, c)
                if total_score > best_score:
                    best_score = total_score
                    best_move = (r, c)
    
    # 根据评分最高的位置进行落子
    if best_move:
        board[best_move[0]][best_move[1]] = 2
        return best_move
    else:
        # 如果没有合适的落子位置，可以随机选择或处理为游戏结束
        print("没有合适的落子位置，检查逻辑")
        return None

def play_game():
    board = [[0 for _ in range(9)] for _ in range(9)]
    last_player_move = (0, 0)  # 初始化玩家的最后落子位置
    while True:
        showboard(board)
        player_row, player_col = player_move(board)
        last_player_move = (player_row, player_col)  # 更新玩家的最后落子位置
        if is_win(board, player_row, player_col, 1):
            showboard(board)
            print("恭喜你，你赢了！")
            break
        if is_tie(board):
            showboard(board)
            print("平局！")
            break
        computer_row, computer_col = computer_move(board, last_player_move)  # 传递玩家的最后落子位置给电脑
        if is_win(board, computer_row, computer_col, 2):
            showboard(board)
            print("电脑赢了！")
            break
        if is_tie(board):
            showboard(board)
            print("平局！")
            break

# 开始游戏
play_game()
