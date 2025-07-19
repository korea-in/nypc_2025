# ================================
# Game 클래스: 게임 상태 관리
# ================================
class Game:

    def __init__(self, board, first):
        self.board = board            # 게임 보드 (2차원 배열)
        self.first = first            # 선공 여부
        self.passed = False           # 마지막 턴에 패스했는지 여부

    # 사각형 (r1, c1) ~ (r2, c2)이 유효한지 검사 (합이 10이고, 네 변을 모두 포함)
    def isValid(self, board, r1, c1, r2, c2):
        sums = 0
        r1fit = c1fit = r2fit = c2fit = False
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if board[r][c] > 0:
                    sums += board[r][c]
                    if r == r1:
                        r1fit = True
                    if r == r2:
                        r2fit = True
                    if c == c1:
                        c1fit = True
                    if c == c2:
                        c2fit = True
        return sums == 10 and r1fit and r2fit and c1fit and c2fit

    def sumNumber(self, board, r1, c1, r2, c2):
        sums = 0
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if(board[r][c] > 0): sums += board[r][c]
        return sums

    def getAllSelectableCombinations(self, board):
        result = []
        for r1 in range(len(board)):
            for c1 in range(len(board[0])):
                result.extend(self.getSelectableCombinations(board, r1, c1))
        return result

    def getSelectableCombinations(self, board, r1, c1):
        moved = False
        result = []
        for r2 in range(r1, len(board)):
            moved = False
            for c2 in range(c1, len(board[0])):
                num = self.sumNumber(board, r1, c1, r2, c2)
                if num > 10: break
                elif num < 10:
                    moved = True
                    continue
                elif num == 10:
                    if self.isValid(board, r1, c1, r2, c2):
                        result.append((r1, c1, r2, c2))
                    else:
                        break
            if(moved == False): break
        return result
    
    def calculatePriority(self, r1, c1, r2, c2):
        global testSelectCombine, realSelectCombine
        testSelectCombine = []
        
        # 수를 놓기 전 계산 가능한 점수(가산점 대상)
        takeOtherScore = 0       # 뺏은 상대방 점수
        saveMyScore = 0          # 지킨 나의 점수
        getNewScore = 0          # 얻은 점수
        removeCombineCount = 0   # 지워지는 선택 가능한 수
        
        # 수를 놓고 나서 계산 해야하는 점수(가감점 대상)
        createCombineCount = 0   # 새로 생기는 선택 가능한 수
        maxTakeMyScore = 0       # 새로 생기는 수 중에서 뺏기는 최대 점수
        maxGetOtherScore = 0     # 최대 점수 기준 수에서 상대방이 얻게 되는 점수
        
        #print("계산 대상 조합: (%d, %d) ~ (%d, %d)" % (r1, c1, r2, c2))
        
        testBoard = [row[:] for row in self.board]
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                if(self.board[r][c] == 0): saveMyScore+=1
                elif(self.board[r][c] < 0): takeOtherScore+=1
                else: getNewScore+=1
                testBoard[r][c] = 0
        #print("임의의 보드판에 조합 선택 반영, 뺏은칸: %d, 지킨칸: %d, 얻은칸: %d" % (takeOtherScore, saveMyScore, getNewScore))
        
        testSelectCombine = self.getAllSelectableCombinations(testBoard)
        removeCombineCount = len(realSelectCombine) - len(testSelectCombine)
        #print("테스트 보드에서 선택 가능한 수 찾기 완료, 지워지는 선택 가능한 수: %d" % (removeCombineCount))
        
        diffCombineList = [x for x in testSelectCombine if x not in realSelectCombine]
        createCombineCount = len(diffCombineList)
        #print("=== 새로 생긴 수 ===")
        #print(diffCombineList)
        
        for diffCombine in diffCombineList:
            (r1, c1, r2, c2) = diffCombine
            takeMyScore = 0
            getOtherScore = 0
            for r in range(r1, r2+1):
                for c in range(c1, c2+1):
                    if(testBoard[r][c] == 0): takeMyScore+=1
                    elif(testBoard[r][c] > 0): getOtherScore+=1
                if(maxTakeMyScore < takeMyScore):
                    maxTakeMyScore = takeMyScore
                    maxGetOtherScore = getOtherScore
        
        #print("===========================================")
        #for i in range(len(self.board)): #print(self.board[i])
        #print("===========================================")
        #for i in range(len(self.board)): #print(testBoard[i])
        #print("===========================================")
        
        myScore = 0
        otherScore = 0
        for r in range(r1, len(self.board)):
            for c in range(c1, len(self.board[0])):
                    if(self.board[r][c] == 0): myScore+=1
                    elif(self.board[r][c] < 0): otherScore+=1

        if(myScore <= otherScore) :
            result = (
                  (takeOtherScore     * 5)
                + (saveMyScore        * 1)
                + (getNewScore        * 3)
                + (removeCombineCount * 2)
                - (createCombineCount * 1)
                - (maxTakeMyScore     * 2)
                - (maxGetOtherScore   * 2)
            )
        else : 
            result = (
                  (takeOtherScore     * 3)
                + (saveMyScore        * 2)
                + (getNewScore        * 2)
                + (removeCombineCount * 1)
                - (createCombineCount * 2)
                - (maxTakeMyScore     * 3)
                - (maxGetOtherScore   * 2)
            )
        return result


    # ================================================================
    # ===================== [필수 구현] ===============================
    # 합이 10인 유효한 사각형을 찾아 (r1, c1, r2, c2) 튜플로 반환
    # 없으면 (-1, -1, -1, -1) 반환 (패스 의미)
    # ================================================================
    def calculateMove(self, _myTime, _oppTime):
        global realSelectCombine, gameTurn
        gameTurn += 1
        realSelectCombine = []
        
        bestCombine = (-1, -1, -1, -1)
        bestPriority = -1
        
        realSelectCombine = self.getAllSelectableCombinations(self.board)

        for combine in realSelectCombine:
            (r1, c1, r2, c2) = combine
            priority = self.calculatePriority(r1, c1, r2, c2)
            if(bestPriority < priority):
                bestPriority = priority
                bestCombine = (r1, c1, r2, c2)

        #print(bestCombine)
        tr1, tc1, tr2, tc2 = bestCombine
        return tr1, tc1, tr2, tc2
    # =================== [필수 구현 끝] =============================

    # 상대방의 수를 받아 보드에 반영
    def updateOpponentAction(self, action, _time):
        self.updateMove(*action, False)

    # 주어진 수를 보드에 반영 (칸을 0으로 지움)
    def updateMove(self, r1, c1, r2, c2, _isMyMove):
        if r1 == c1 == r2 == c2 == -1:
            self.passed = True
            return
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if(_isMyMove) : self.board[r][c] = 0
                else : self.board[r][c] = -1
                
        self.passed = False


# ================================
# main(): 입출력 처리 및 게임 진행
# ================================
def main():
    while True:
        line = input().split()

        if len(line) == 0:
            continue

        command, *param = line

        if command == "READY":
            # 선공 여부 확인
            turn = param[0]
            global first
            first = turn == "FIRST"
            print("OK", flush=True)
            continue

        if command == "INIT":
            global gameTurn
            gameTurn = 0
            # 보드 초기화
            board = [list(map(int, row)) for row in param]
            global game
            game = Game(board, first)
            continue

        if command == "TIME":
            # 내 턴: 수 계산 및 실행
            myTime, oppTime = map(int, param)
            ret = game.calculateMove(myTime, oppTime)
            game.updateMove(*ret, True)
            print(*ret, flush=True)
            continue

        if command == "OPP":
            # 상대 턴 반영
            r1, c1, r2, c2, time = map(int, param)
            game.updateOpponentAction((r1, c1, r2, c2), time)
            continue

        if command == "FINISH":
            break

        assert False, f"Invalid command {command}"

if __name__ == "__main__":
    main()