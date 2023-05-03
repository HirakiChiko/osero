class Osero:

    def __init__(self):
        self.empty = 'e'
        self.black_stone = 'b'
        self.white_stone = 'w'
        self.recommend = 'r'
        self.error_message = ""
        self.question_message = ""
        self.end_message = ""
        self.end_flag = False
        self.no_recommend = False
        #self.log_message = ""

        self.my_stone = self.black_stone
        self.opponent_stone = self.white_stone

        self.board = self.create_board()
        self.check_stone()

        self.question()


    def create_board(self):
        board = [[self.empty for i in range(8)] for j in range(8)]
        board[3][3],board[4][4] = self.white_stone,self.white_stone
        board[3][4],board[4][3] = self.black_stone,self.black_stone
        return board


    # 任意の座標がどの状態かを調べる
    def check_masu(self,l,r):
        return self.board[l][r]

    def edit_board(self,l,r,state):
        self.board[l][r] = state


    # 置ける場所を調べる
    def check_stone(self):
        self.all_recommend_list = [[],[]]
        for l,line in enumerate(self.board):
            for r,row in enumerate(line):
                if row == self.empty:
                    stone_dir_list = self.check_8masu(l,r) # 周囲8マスにある相手の石と方向
                    a = self.is_sand(l,r,stone_dir_list)
                    if a != False:   # どれか1方向以上挟める状態か
                        self.edit_board(l,r,self.recommend)
                        self.all_recommend_list[0].append(a[0])
                        self.all_recommend_list[1].append(a[1])
        if self.all_recommend_list == [[],[]]:
            if self.no_recommend == True:
                self.end_flag = True
                #self.log_message = "どちらの石も置ける場所がありませんでした"
            else:
                #self.log_message = "{}は置ける場所がありませんでした".format(self.my_stone)
                self.no_recommend = True
                self.switch()
                self.check_stone()
        else:
            self.no_recommend = False


    # 任意のマスの周囲8マスを調べる
    # 相手の石が置いてある場合、置いてある石の方向を示す数字を返す
    def check_8masu(self,l,r):
        direction_list = [[l-1,r-1],[l-1,r],[l-1,r+1],[l,r-1],[l,r+1],[l+1,r-1],[l+1,r],[l+1,r+1]]
        l2 = []
        for i,youso in enumerate(direction_list):
            try:
                # 相手の石があったら、
                if self.check_masu(youso[0],youso[1]) == self.opponent_stone:
                    l2.append(i)
            except:
                pass
        return(l2)

    # 挟めるかどうか
    def is_sand(self,l,r,stone_dir_list):
        direction_list = [[-1,-1],[-1,0],[-1,+1],[0,-1],[0,+1],[+1,-1],[+1,0],[+1,+1]]
        ans = False
        tmp = []
        for i in stone_dir_list:
            d1 = direction_list[i][0]
            d2 = direction_list[i][1]
            Flag = 0
            for j in range(8):
                if Flag == 0:
                    try:
                        if self.check_masu(l+d1, r+d2) == self.my_stone:
                            tmp.append(i)
                            Flag = 1
                        elif self.check_masu(l+d1, r+d2) == self.opponent_stone:
                            d1 += direction_list[i][0]
                            d2 += direction_list[i][1]
                        else:
                            Flag = 1
                        if l+d1 <0 or r+d2<0 :
                            Flag = 1
                    except IndexError:
                        break
        if tmp != []:
                ans = [[l,r],tmp]
        return ans
    
    # ひっくり返す
    def reverse_stone(self,l,r):
        direction_list = [[-1,-1],[-1,0],[-1,+1],[0,-1],[0,+1],[+1,-1],[+1,0],[+1,+1]]
        if [l,r] in self.all_recommend_list[0]:
            ind = self.all_recommend_list[0].index([l,r])
            self.edit_board(l,r,state=self.my_stone)
            for i in self.all_recommend_list[1][ind]:
                d1 = direction_list[i][0]
                d2 = direction_list[i][1]
                while True:
                    if self.check_masu(l+d1,r+d2) == self.opponent_stone:
                        self.edit_board(l+d1,r+d2,state=self.my_stone)
                        d1 += direction_list[i][0]
                        d2 += direction_list[i][1]
                    if self.check_masu(l+d1,r+d2) == self.my_stone:
                        break
    
    # boardのおける場所の表示を消す
    def erase_recommend(self):
        for i in self.all_recommend_list[0]:
            if self.check_masu(l=i[0],r=i[1]) == self.recommend:
                self.edit_board(l=i[0],r=i[1],state = self.empty)

    def switch(self):
        if self.my_stone == self.black_stone:
            self.my_stone = self.white_stone
            self.opponent_stone = self.black_stone
        elif self.my_stone == self.white_stone:
            self.my_stone = self.black_stone
            self.opponent_stone = self.white_stone

    def question(self):
        if self.my_stone == "b":
            self.question_message = "黒の石を置いてください"
        if self.my_stone == "w":
            self.question_message = "白の石を置いてください"

    
    # 置く→ひっくり返す→置いていい場所を消す→次に置いていい場所を表示
    def set_reverse_erase_recommend(self,l):
        self.edit_board(l[0],l[1], state=self.my_stone)
        self.reverse_stone(l[0],l[1])
        self.erase_recommend()
        self.switch()
        self.check_stone()
        if self.end_judge():
            self.end()
            return
        self.question()


    # 入力された回答が正しいか
    def check_answer(self,loc):
        self.error_message = ""
        l = list(map(int,list(loc)))
        if l in self.all_recommend_list[0]:
            self.set_reverse_erase_recommend(l)
        else:
            self.error_message = "そこには置けません"


    def end_judge(self):
        if self.end_flag == True:
            return True
        empty_num = 0
        for list in self.board:
            empty_num += list.count(self.empty)
            empty_num += list.count(self.recommend)
        if empty_num == 0:
            return True


    # 終了
    def end(self):
        #self.end_message = ""
        self.question_message = ""
        self.question_message = ""
        black_stone_num = 0
        white_stone_num = 0
        for list in self.board:
            black_stone_num += list.count(self.black_stone)
            white_stone_num += list.count(self.white_stone)
        b_num = "黒："+str(black_stone_num)
        w_num = "白："+str(white_stone_num)
        if black_stone_num > white_stone_num:
            result = "\n黒の勝ちです"
        elif black_stone_num < white_stone_num:
            result = "\n白の勝ちです"
        elif black_stone_num == white_stone_num:
            result = "\n引き分けです"
        self.end_message = "対戦終了\n" + b_num + w_num + result


    def reset(self):
        self.board = self.create_board()
        self.my_stone = self.black_stone
        self.check_stone()