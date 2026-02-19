from Components.script import Script
from Components.UI.UILabel import Label

class HighScoreHandler(Script):
    def __init__(self, highscoreLabel: Label, lastScoreLabel: Label):
        super().__init__()
        self.highscore = highscoreLabel
        self.lastScore = lastScoreLabel
        self.high: int = 0
        self.last: int = 0
    
    def Awake(self):
        self.last, self.high = self.loadScores()
        return super().Awake()
    
    def Update(self, deltaTime):
        self.highscore.Text = f"HIGHSCORE: {self.high}"
        self.lastScore.Text = f"LAST SCORE: {self.last}"
        return super().Update(deltaTime)
    
    def loadScores(self) -> tuple[int, int]:
        try:
            with open("highscore.data", "r") as file:
                lines = file.readlines()
                scores = {}
                for line in lines:
                    key, value = line.strip().split(":")
                    scores[key] = int(value)
                return scores.get("last_score", 0), scores.get("highscore", 0)
        except FileNotFoundError:
            return 0, 0
        
    def saveScores(self):
        with open("highscore.data", "w") as file:
            file.writelines([
                f"last_score:{self.last}\n",
                f"highscore:{self.high}\n"
            ])
            
    def NewScore(self, value: int):
        if value > self.high:
            self.high = value
        self.last = value
        self.saveScores()