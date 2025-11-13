import random
import math
import time
import threading
import copy
import time
import concurrent.futures  
import profile




BOARD_SIZE = 8

PLAYER_NUM = 2
MCTS_NUM   = 1

MAX_THINK_TIME = 20


#------------------------------------
# Print out the board
#------------------------------------
def printBoard( board ):
	mcts_stones   = 0
	player_stones = 0


	print("  0 1 2 3 4 5 6 7 ")
	print(" +-+-+-+-+-+-+-+-+")

	for i in range(0,BOARD_SIZE):
		print( "" + str(i) + "|", end="")
		for j in range(0,BOARD_SIZE):
			if board[i][j] == 0 :
				print(" |", end="")
			elif board[i][j] == MCTS_NUM :
				print("x|", end="")
				mcts_stones += 1
			else :
				print("o|", end="")
				player_stones += 1
		print("")
		print(" +-+-+-+-+-+-+-+-+")
	
	print("Your stones:", player_stones, "  MCTS stones:", mcts_stones)

#------------------------------------
# Return a new initialized board
#------------------------------------
def getInitialBoard():
	board = {}

	for i in range(0,BOARD_SIZE):
		board[i] = {}

		for j in range(0,BOARD_SIZE):
			board[i][j] = 0

	board[BOARD_SIZE/2 -1][BOARD_SIZE/2 -1] = MCTS_NUM
	board[BOARD_SIZE/2   ][BOARD_SIZE/2   ] = MCTS_NUM

	board[BOARD_SIZE/2 -1][BOARD_SIZE/2   ] = PLAYER_NUM
	board[BOARD_SIZE/2   ][BOARD_SIZE/2 -1] = PLAYER_NUM

	return board

#------------------------------------
# Return a copy of a board
#------------------------------------
def copyBoard(dest_board, src_board):

	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			dest_board[i][j] = src_board[i][j]


#------------------------------------
# Return the number of specified stones in a board
#------------------------------------
def countStones(board, turn):
	stones = 0
	
	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			if board[i][j] == turn:
				stones += 1

	return stones

#------------------------------------
# Return a list of all positions in which the specified player can place a stone.
#------------------------------------
def checkPlacablePositions(board, turn):
	#placable_positions 全ての置ける位置
	placable_positions = []

	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			if board[i][j] != 0:
				continue
			if updateBoard(board, turn, i, j, checkonly=True) > 0:#revesed_stoneの値を入手したときにcheclonlyはfalseになる
				#updateBoard(現在のボード, turn, i, j, checkonly=True　チェックするだけ
				placable_positions.append( (i,j) )
	return placable_positions


#------------------------------------
# Place a stone (when checkonly is True, it only returns the number 
# of stones to be turned and it does not modify the board)
# 
# Return: the number of stones to be turned 
# (The new stone placed is not contained in the number)
#------------------------------------
def updateBoard(board, turn, i, j, checkonly=False):
	
	if not(checkonly):
		board[i][j] = turn

	reversed_stone = 0

	#-------------------------------------------------
	flag = False
	for i2 in range(i+1, BOARD_SIZE):
		if board[i2][j] == 0 :
			break
		if board[i2][j] == turn:
			flag = True
			break
	if flag:
		for i3 in range(i+1, i2):
			if not(checkonly):
				board[i3][j] = turn
			reversed_stone += 1

	flag = False
	for i2 in reversed(range(0, i)):
		if board[i2][j] == 0 :
			break
		if board[i2][j] == turn:
			flag = True
			break
	if flag:
		for i3 in reversed(range(i2+1, i)):
			if not(checkonly):
				board[i3][j] = turn
			reversed_stone += 1

	#-------------------------------------------------
	flag = False
	for j2 in range(j+1, BOARD_SIZE):
		if board[i][j2] == 0 :
			break
		if board[i][j2] == turn:
			flag = True
			break
	if flag:
		for j3 in range(j+1, j2):
			if not(checkonly):
				board[i][j3] = turn
			reversed_stone += 1

	flag = False
	for j2 in reversed(range(0, j)):
		if board[i][j2] == 0 :
			break
		if board[i][j2] == turn:
			flag = True
			break
	if flag:
		for j3 in reversed(range(j2+1, j)):
			if not(checkonly):
				board[i][j3] = turn
			reversed_stone += 1
	#-------------------------------------------------

	flag = False
	for m in range(1, min(BOARD_SIZE-i, BOARD_SIZE-j)):
		if board[i+m][j+m] == 0 :
			break
		if board[i+m][j+m] == turn:
			flag = True
			break
	if flag:
		for m3 in range(1, m):
			if not(checkonly):
				board[i+m3][j+m3] = turn
			reversed_stone += 1

	flag = False
	for m in range(1, min(i,j)+1):
		if board[i-m][j-m] == 0 :
			break
		if board[i-m][j-m] == turn:
			flag = True
			break
	if flag:
		for m3 in range(1, m):
			if not(checkonly):
				board[i-m3][j-m3] = turn
			reversed_stone += 1


	flag = False
	for m in range(1, min(i+1, BOARD_SIZE-j)):
		if board[i-m][j+m] == 0 :
			break
		if board[i-m][j+m] == turn:
			flag = True
			break
	if flag:
		for m3 in range(1, m):
			if not(checkonly):
				board[i-m3][j+m3] = turn
			reversed_stone += 1

	flag = False
	for m in range(1, min(BOARD_SIZE-i,j+1)):
		if board[i+m][j-m] == 0 :
			break
		if board[i+m][j-m] == turn:
			flag = True
			break
	if flag:
		for m3 in range(1, m):
			if not(checkonly):
				board[i+m3][j-m3] = turn
			reversed_stone += 1
			
	#-------------------------------------------------

	return reversed_stone
	
#---------------------------------------------------------------------------------------------

#------------------------------------
# Get a hand-input position
#------------------------------------
def handinputNextPosition(board, turn):
	print("head in")#読み込まれているかの確認

	while True:
		print("Possible positions are ", checkPlacablePositions(board, turn))#配置可能な位置の確認
		print("")

		while True:
			stri = input("Input vertical position[0-"+ str(BOARD_SIZE-1) +"]: ")
			if stri.isdigit() and int(stri) >= 0 and int(stri) < BOARD_SIZE:
				break
		while True:
			strj = input("Input horizontal position[0-"+ str(BOARD_SIZE-1) +"]: ")
			if strj.isdigit() and int(strj) >= 0 and int(strj) < BOARD_SIZE:
				break

		i = int(stri)
		j = int(strj)

		print("Your input : (", i, ",", j,")")

		if board[i][j] == 0 and updateBoard(board, turn, i, j, checkonly=True) > 0:#空白の状態かつupdateboarddの
			break
		print("not correct position!!")

	return (i,j)



#------------------------------------
# Decide the next position utilizing MCTS
#------------------------------------


def mctsNextPosition(board,p,e):
	print("試行中...")
	print(f"現在のスレッド:{threading.current_thread().name}")

	def calc_ucb1( node_tuple, t, cval ):
		name, nplayout, reward, childrens = node_tuple

		if nplayout == 0:
			nplayout = 0.00000000001

		if t == 0:
			t = 1

		return (reward / nplayout) + cval * math.sqrt( 2*math.log( t ) / nplayout )
	def find_playout( brd, turn, depth = 0):
		
		def eval_board( brd ):
			player_stone = countStones(brd, p)
			mcts_stone   = countStones(brd, e)

			if mcts_stone > player_stone:
				return True
			return False


		# Playouts are stoped at the threshold depth.
		# In early stages of a game, detailed evaluation seems to be not necessary.
		if depth > 33:
			return eval_board( brd )

		turn_positions = checkPlacablePositions(brd, turn)

		# Check if the player can place a stone
		if len(turn_positions) == 0:
			if turn == p:
				neg_turn = e
			else:
				neg_turn = p

			neg_turn_positions = checkPlacablePositions(brd, neg_turn)
			
			if len(neg_turn_positions) == 0:
				# Return the result when both player cannot place a stone
				return eval_board( brd )
			else:
				# Change the turn when the other can place a stone
				turn = neg_turn
				turn_positions = neg_turn_positions
		
		# Place a stone randomly
		ijpair = turn_positions[ random.randrange(0, len(turn_positions)) ]
		updateBoard(brd, turn, ijpair[0], ijpair[1])

		# Change the turn
		if turn == MCTS_NUM:
			turn = PLAYER_NUM
		else:
			turn = MCTS_NUM

		return find_playout( brd, turn, depth=depth+1)


	def expand_node(brd, turn):
		positions = checkPlacablePositions(brd, turn)
		result = []
		
		for ijpair in positions:
			result.append( (ijpair, 0, 0, []) )

		return result

	def find_path_default_policy( root, total_playout ):
		current_path      = []
		current_childrens = root

		parent_playout = total_playout

		isMCTSTurn = True

		while True:
			if len(current_childrens) == 0:
				break

			maxidxlist = [0]
			cidx       = 0
			if isMCTSTurn:
				maxval = -1
			else:
				maxval = 2

			for n_tuple in current_childrens:
				t_ijpair, t_nplayout, t_reward, t_childrens = n_tuple

				# In MCTS's turn, the node with the largest value is selected.
				# In the other's turn, the node with the least value is selected.

				if isMCTSTurn:
					cval = calc_ucb1( n_tuple, parent_playout, -0.1 )

					if cval >= maxval:
						if cval == maxval:
							maxidxlist.append( cidx )
						else:
							maxidxlist = [ cidx ]
							maxval     = cval
				else:
					cval = calc_ucb1( n_tuple, parent_playout, 0.1 )

					if cval <= maxval:
						if cval == maxval:
							maxidxlist.append( cidx )
						else:
							maxidxlist = [ cidx ]
							maxval     = cval

				cidx += 1

			# When plural candidates exist, a position is chosen randomly
			maxidx = maxidxlist[ random.randrange(0, len(maxidxlist)) ]
			t_ijpair, t_nplayout, t_reward, t_childrens = current_childrens[maxidx]

			current_path.append( t_ijpair )
			parent_playout = t_nplayout
			current_childrens = t_childrens

			isMCTSTurn = not(isMCTSTurn)

		return current_path

	#-----------------------------------------------------
	root = expand_node(board, p)
	current_board = getInitialBoard()
	current_board2 = getInitialBoard()

	start_time = time.time()
	

	for loop in range(0, 5000):
		# print(f"現在のスレッド:{threading.current_thread().name}")
#	for loop in range(0, 10000000):
		# Check the time limit 
		if (time.time() - start_time) >= MAX_THINK_TIME:
			break

		#--------------------------------------
		# Default policy
		current_path = find_path_default_policy( root, loop )#(現在のスレッドの居場所の確認)

		# current_path contains a list of positions to be placed stones.
		# Following lines places stones according to the list.
		# 
		# Note that the turn changes alternately.
		# Currently, a node corresponding to the situation requesting "pass" has no child nodes.
		# Thus it is not necessary to consider a player placing multiple stones at once.


		# ここから下も現在のスレッドの確認に必要
		copyBoard(current_board, board)
		turn = MCTS_NUM
		for ijpair in current_path:
			updateBoard(current_board, turn, ijpair[0], ijpair[1])
			if turn == MCTS_NUM:
				turn = PLAYER_NUM
			else:
				turn = MCTS_NUM

		#--------------------------------------
		# Playout

		# the board needs to be copied because the board data is modified in find_playout

		# copyBoard(current_board2, current_board,)
		# isWon = find_playout( current_board2, turn)


	# # 	# スレッド数
	# 	NUM_THREADS = 4

	# 	# 結果を保存するリスト
	# 	thread_results = [None] * NUM_THREADS
	# 	threads = []

		
	# 	def threaded_playout(index, board_snapshot, turn):
	# 		local_board = copy.deepcopy(board_snapshot)
	# 		result = find_playout(local_board, turn)
	# 		thread_results[index] = result

	# # 現在の盤面を保存
	
	# 	board_snapshot = copy.deepcopy(current_board)

	# # スレッドの作成と開始
	# 	for i in range(NUM_THREADS):#4回繰り返す
	# 		t = threading.Thread(target=threaded_playout, args=(i, board_snapshot, turn), name=f"PlayoutThread-{i}")
	# 		t.start()
	# 		threads.append(t)

	# # 全スレッドの終了待ち
	# 	for t in threads:
	# 		t.join()

	# # 1番目の結果を使う（or any logic, like majority vote）


	# 	isWon = thread_results[0]#ここは0ではなく拡張
	# 	#ここの0を


		#  処理にかかった時間データを使用

		NUM_THREADS = 4
		def threaded_playout(board_snapshot, turn):
			local_board = copy.deepcopy(board_snapshot)
			return find_playout(local_board, turn)

		board_snapshot = copy.deepcopy(current_board)
		with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
			futures = [executor.submit(threaded_playout, board_snapshot, turn) for _ in range(NUM_THREADS)]
			results = [f.result() for f in futures]
			#print(results)#デバック用



# 多数決による勝敗判定
		isWon = results.count(True) > (NUM_THREADS // 2)
				

		#--------------------------------------

		if loop%500 == 0 and loop > 0:
			print("loop:", loop, current_path, len(current_path), " eval val: ", isWon)
		

		#--------------------------------------
		# Up date of the tree (from the root of the tree to leafs)

		current_childrens = root

		for ijpair in current_path:
			idx = 0
			for n_tuple in current_childrens:
				t_ijpair, t_nplayout, t_reward, t_childrens = n_tuple
				if ijpair[0] == t_ijpair[0] and ijpair[1] == t_ijpair[1]:
					break
				idx += 1

			if ijpair[0] == t_ijpair[0] and ijpair[1] == t_ijpair[1]:
				t_nplayout += 1
				if isWon:
					t_reward   += 1
				
				if t_nplayout >= 5 and len(t_childrens) == 0:
					t_childrens = expand_node(current_board, turn)

				current_childrens[idx] = (t_ijpair, t_nplayout, t_reward, t_childrens)
			else:
				print("failed")

			current_childrens = t_childrens
		#--------------------------------------
	end = time.time()  # 現在時刻（処理完了後）を取得
	time_diff = end - start_time  # 処理完了後の時刻から処理開始前の時刻を減算する
	print(time_diff)
	#-----------------------------------------------------

	print("loop count: ", loop)

	max_avg_reward = -1
	result_ij_pair = (0,0)

	for n_tuple in root:
		t_ijpair, t_nplayout, t_reward, t_childrens = n_tuple

		if (t_nplayout > 0) and (t_reward / t_nplayout > max_avg_reward):
			result_ij_pair = t_ijpair
			max_avg_reward = t_reward / t_nplayout
	
	return result_ij_pair


# ---------------------------------------------------------------

def mctsNextPositionThread(board,p,e):
	print("試行中...")
	

	def calc_ucb1( node_tuple, t, cval ):
		name, nplayout, reward, childrens = node_tuple

		if nplayout == 0:
			nplayout = 0.00000000001

		if t == 0:
			t = 1

		return (reward / nplayout) + cval * math.sqrt( 2*math.log( t ) / nplayout )

	def find_playout( brd, turn, depth = 0):
		def eval_board( brd ):
			player_stone = countStones(brd, e)
			mcts_stone   = countStones(brd, p)

			if mcts_stone > player_stone:
				return True
			return False


		# Playouts are stoped at the threshold depth.
		# In early stages of a game, detailed evaluation seems to be not necessary.
		if depth > 32:
			return eval_board( brd )

		turn_positions = checkPlacablePositions(brd, turn)

		# Check if the player can place a stone
		if len(turn_positions) == 0:
			if turn == e:
				neg_turn = p
			else:
				neg_turn = e

			neg_turn_positions = checkPlacablePositions(brd, neg_turn)
			
			if len(neg_turn_positions) == 0:
				# Return the result when both player cannot place a stone
				return eval_board( brd )
			else:
				# Change the turn when the other can place a stone
				turn = neg_turn
				turn_positions = neg_turn_positions
		
		# Place a stone randomly
		ijpair = turn_positions[ random.randrange(0, len(turn_positions)) ]
		updateBoard(brd, turn, ijpair[0], ijpair[1])

		# Change the turn
		if turn == MCTS_NUM:
			turn = PLAYER_NUM
		else:
			turn = MCTS_NUM

		return find_playout( brd, turn, depth=depth+1)


	def expand_node(brd, turn):
		positions = checkPlacablePositions(brd, turn)
		result = []
		
		for ijpair in positions:
			result.append( (ijpair, 0, 0, []) )

		return result

	def find_path_default_policy( root, total_playout ):
		current_path      = []
		current_childrens = root

		parent_playout = total_playout

		isMCTSTurn = True

		while True:
			if len(current_childrens) == 0:
				break

			maxidxlist = [0]
			cidx       = 0
			if isMCTSTurn:
				maxval = -1
			else:
				maxval = 2

			for n_tuple in current_childrens:
				t_ijpair, t_nplayout, t_reward, t_childrens = n_tuple

				# In MCTS's turn, the node with the largest value is selected.
				# In the other's turn, the node with the least value is selected.

				if isMCTSTurn:
					cval = calc_ucb1( n_tuple, parent_playout, -0.1 )

					if cval >= maxval:
						if cval == maxval:
							maxidxlist.append( cidx )
						else:
							maxidxlist = [ cidx ]
							maxval     = cval
				else:
					cval = calc_ucb1( n_tuple, parent_playout, 0.1 )

					if cval <= maxval:
						if cval == maxval:
							maxidxlist.append( cidx )
						else:
							maxidxlist = [ cidx ]
							maxval     = cval

				cidx += 1

			# When plural candidates exist, a position is chosen randomly
			maxidx = maxidxlist[ random.randrange(0, len(maxidxlist)) ]
			t_ijpair, t_nplayout, t_reward, t_childrens = current_childrens[maxidx]

			current_path.append( t_ijpair )
			parent_playout = t_nplayout
			current_childrens = t_childrens

			isMCTSTurn = not(isMCTSTurn)

		return current_path

	#-----------------------------------------------------
	root = expand_node(board, p)
	current_board = getInitialBoard()
	current_board2 = getInitialBoard()

	start_time = time.time()
	

	for loop in range(0, 5000):

		# Check the time limit 
		if (time.time() - start_time) >= MAX_THINK_TIME:
			break

		#--------------------------------------
		# Default policy
		current_path = find_path_default_policy( root, loop )

		# current_path contains a list of positions to be placed stones.
		# Following lines places stones according to the list.
		# 
		# Note that the turn changes alternately.
		# Currently, a node corresponding to the situation requesting "pass" has no child nodes.
		# Thus it is not necessary to consider a player placing multiple stones at once.

		copyBoard(current_board, board)
		turn = MCTS_NUM
		for ijpair in current_path:
			updateBoard(current_board, turn, ijpair[0], ijpair[1])
			if turn == MCTS_NUM:
				turn = PLAYER_NUM
			else:
				turn = MCTS_NUM

		#--------------------------------------
		# Playout

		# the board needs to be copied because the board data is modified in find_playout

		copyBoard(current_board2, current_board,)
		isWon = find_playout( current_board2, turn)


#
		  # 処理にかかった時間データを使用

# 	NUM_THREADS = 4

# 	def threaded_playout(board_snapshot, turn):
# 		local_board = copy.deepcopy(board_snapshot)
# 		return find_playout(local_board, turn)

# # 現在の盤面を保存
# 	board_snapshot = copy.deepcopy(current_board)

# # スレッドプールで複数のプレイアウトを同時に実行
# 	with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
# 		futures = [executor.submit(threaded_playout, board_snapshot, turn) for _ in range(NUM_THREADS)]
# 		results = [f.result() for f in futures]

# # 複数の結果から多数決（True の数が多ければ勝ちと判定）
# 		isWon = results.count(True) > (NUM_THREADS // 2)
				

		#--------------------------------------

		if loop%500 == 0 and loop > 0:
			print("loop:", loop, current_path, len(current_path), " eval val: ", isWon)
		

		#--------------------------------------
		# Up date of the tree (from the root of the tree to leafs)

		current_childrens = root

		for ijpair in current_path:
			idx = 0
			for n_tuple in current_childrens:
				t_ijpair, t_nplayout, t_reward, t_childrens = n_tuple
				if ijpair[0] == t_ijpair[0] and ijpair[1] == t_ijpair[1]:
					break
				idx += 1

			if ijpair[0] == t_ijpair[0] and ijpair[1] == t_ijpair[1]:
				t_nplayout += 1
				if isWon:
					t_reward   += 1
				
				if t_nplayout >= 5 and len(t_childrens) == 0:
					t_childrens = expand_node(current_board, turn)

				current_childrens[idx] = (t_ijpair, t_nplayout, t_reward, t_childrens)
			else:
				print("failed")

			current_childrens = t_childrens
		#--------------------------------------
	end = time.time()  # 現在時刻（処理完了後）を取得
	time_diff = end - start_time  # 処理完了後の時刻から処理開始前の時刻を減算する
	print(time_diff)
	#-----------------------------------------------------

	print("loop count: ", loop)

	max_avg_reward = -1
	result_ij_pair = (0,0)

	for n_tuple in root:
		t_ijpair, t_nplayout, t_reward, t_childrens = n_tuple

		if (t_nplayout > 0) and (t_reward / t_nplayout > max_avg_reward):
			result_ij_pair = t_ijpair
			max_avg_reward = t_reward / t_nplayout
	
	return result_ij_pair


#---------------------------------------------------------------------------------------------
def getInitialBoard():
    board = {}
    for i in range(0,BOARD_SIZE):
        board[i] = {}
        for j in range(0,BOARD_SIZE):
            board[i][j] = 0

    # ↓ Python3 では / が float になるので // に修正  # NEW
    c = BOARD_SIZE // 2                                       # NEW
    board[c - 1][c - 1] = MCTS_NUM
    board[c    ][c    ] = MCTS_NUM
    board[c - 1][c    ] = PLAYER_NUM
    board[c    ][c - 1] = PLAYER_NUM
    return board

# ...（中略：関数定義はそのまま）...

if __name__ == "__main__" :
    f = open('myfile.txt', 'w')
    roops=100
    for roops in range(100):
        random.seed(10000)
        print("ループ回数",roops)

        current_board = getInitialBoard()#ボードの初期化
        printBoard( current_board )

        isPlayerTurn = True #どっちの手番か trueならplayerから

        # ====== 計測用の入れ物 ======                       # NEW
        move_times = []                                      # NEW
        move_count = 0                                       # NEW
        def dump_avg_if_needed():                            # NEW
            """10手ごとに平均を表示・保存"""                   # NEW
            if move_count > 0 and move_count % 10 == 0:      # NEW
                last10 = move_times[-10:]                    # NEW
                avg10 = sum(last10) / 10.0                   # NEW
                msg = f"[Game {roops}] 手{move_count-9:02d}〜{move_count:02d}の平均: {avg10:.6f} 秒"  # NEW
                print(msg)                                   # NEW
                f.write(msg + "\n")                          # NEW
        # ================================================   # NEW

        while True:
            player_possibility = len(checkPlacablePositions(current_board, PLAYER_NUM))#貴方の置ける位置
            mcts_possibility   = len(checkPlacablePositions(current_board, MCTS_NUM))#敵の置ける位置

            if player_possibility == 0 and mcts_possibility == 0:#もうこれ以上置けない
                break
            if (isPlayerTurn and player_possibility == 0) or (not(isPlayerTurn) and mcts_possibility == 0):#パスのコード
                isPlayerTurn = not(isPlayerTurn)#パスするしかないため相手にターンを渡す
                continue

            if isPlayerTurn:
                print("Your turn:  ")
            else:
                print("MCTS's turn:  ")

            # ====== 1手の計測開始 ======                     # NEW
            start_move = time.perf_counter()                  # NEW

            if isPlayerTurn:
                stone_pos = mctsNextPosition(current_board,p=PLAYER_NUM,e=MCTS_NUM)
                updateBoard(current_board, PLAYER_NUM, stone_pos[0], stone_pos[1])
            else:
                stone_pos = mctsNextPositionThread(current_board,p=MCTS_NUM,e=PLAYER_NUM)
                print("MCTS's answer: ", stone_pos)
                updateBoard(current_board, MCTS_NUM, stone_pos[0], stone_pos[1])

            elapsed = time.perf_counter() - start_move        # NEW
            move_times.append(elapsed)                        # NEW
            move_count += 1                                   # NEW
            print(f"この一手の時間: {elapsed:.6f} 秒")         # NEW
            dump_avg_if_needed()                              # NEW
            # ====== 1手の計測終了 ======                     # NEW

            printBoard( current_board )
            isPlayerTurn = not(isPlayerTurn)

        # ====== ゲーム終了時：端数（10で割り切れない分）も参考表示 ======  # NEW
        if move_count % 10 != 0 and move_count > 0:                                         # NEW
            rem = move_count % 10                                                           # NEW
            lastk = move_times[-rem:]                                                       # NEW
            avgk = sum(lastk) / float(rem)                                                  # NEW
            msg = f"[Game {roops}] 端数 {move_count-rem+1:02d}〜{move_count:02d} の平均: {avgk:.6f} 秒"  # NEW
            print(msg)                                                                      # NEW
            f.write(msg + "\n")                                                             # NEW
        # ===================================================================  # NEW

        player_stone = countStones(current_board, PLAYER_NUM)
        mcts_stone   = countStones(current_board, MCTS_NUM)
        print("RESULT:")
        print("  sensei stones   : ", player_stone)
        print("  Tread stones : ", mcts_stone)
        if player_stone > mcts_stone :
            print("You won")
            f.write('you won'+str(player_stone)+"  "+"mct lose"+str(mcts_stone)+"\n")
        elif player_stone == mcts_stone :
            print("Draw")
            f.write('you Draw'+str(player_stone)+"  "+"mct Draw"+str(mcts_stone)+"\n")
        else:
            print("You lose")
            f.write('you lose'+str(player_stone)+"  "+"mct won"+str(mcts_stone)+"\n")
        printBoard( current_board )
    f.close()