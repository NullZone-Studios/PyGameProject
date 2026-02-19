from Components.script import Script
from Components.UI.UILabel import Label
from .gameMaster import GameMaster
from .player import Player

class GameScoreUpdater(Script):
    def __init__(self, scoreLabel: Label, livesLabel: Label, waveLabel: Label, bossLabel: Label, gameMaster: GameMaster, player: Player):
        self.score = scoreLabel
        self.lives = livesLabel
        self.wave = waveLabel
        self.boss = bossLabel
        self.gm = gameMaster
        self.player = player
        
    def Update(self, deltaTime):
        
        self.score.Text = f"SCORE: {self.gm.currentScore}"
        self.lives.Text = f"LIVES LEFT: {self.player.life}"
        self.wave.Text = f"WAVE: {self.gm.currentWave}"
        self.boss.Text = "BOSS LEVEL" if self.gm.boss_alive else ""
        
        return super().Update(deltaTime)