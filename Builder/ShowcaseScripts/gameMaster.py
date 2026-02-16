from __future__ import annotations

from GameEssentials import GameObject

class GameMaster:
    
    _instance = None
    
    def __init__(
        self,
        boss_wave_interval: int = 5,
        starting_difficulty: float = 1.0,
        wave_difficulty_increase: float = 0.1,
        boss_difficulty_increase: float = 0.2,
        final_wave: int = 10,
        max_difficulty: float | None = None,
    ) -> None:
        self.currentWave = 0
        self.starting_difficulty = max(0.0, starting_difficulty)
        self.difficulty = self.starting_difficulty
        self.wave_difficulty_increase = max(0.0, wave_difficulty_increase)
        self.boss_difficulty_increase = max(0.0, boss_difficulty_increase)
        self.boss_wave_interval = boss_wave_interval
        self.spawnedWaveTurrets: list[GameObject] = []
        self.yet_to_spawn_turrets: list[GameObject] = []
        self.final_wave: int | None = final_wave if final_wave > 0 else None
        self.max_difficulty: float | None = max(0.0, max_difficulty) if max_difficulty is not None else None
        self.normal_waves_completed = 0
        self.boss_waves_completed = 0
        self.is_boss_wave = False
        self.boss_alive = False
        self.is_running = False
        self.is_paused = False
        self.is_game_over = False
        self._ApplyDifficultyCap()

    @property
    def Instance(self) -> GameMaster:
        from GameEssentials import GameMaster
        if GameMaster._instance is None:
            GameMaster._instance = GameMaster()
        return GameMaster._instance

    @property
    def gameObjects(self) -> list[GameObject]:
        from GameEssentials import GameMaster
        return GameWorld.GetInstance().GameObjects

    def AddObject(self, obj: GameObject) -> None:
        if obj not in GameWorld.GetInstance().GameObjects:
            GameWorld.GetInstance().Instantiate(obj)
            obj.Awake()
            obj.Start()
            self.spawnedWaveTurrets.append(obj)
            
    def RemoveObject(self, obj: GameObject) -> None:
        if obj in self.gameObjects:
            obj.Destroy()

    def StartGame(self) -> None:
        self.is_running = True
        self.is_paused = False
        self.is_game_over = False
        self.currentWave = 0
        self.normal_waves_completed = 0
        self.boss_waves_completed = 0
        self.difficulty = self.starting_difficulty
        self.is_boss_wave = False
        self.boss_alive = False

    def Pause(self) -> None:
        if self.is_running and not self.is_game_over:
            self.is_paused = True

    def Resume(self) -> None:
        if self.is_running and not self.is_game_over:
            self.is_paused = False

    def EndGame(self) -> None:
        self.is_running = False
        self.is_game_over = True
        self.is_paused = False

    def StartWave(self) -> None:
        if self.HasReachedFinalWave():
            self.EndGame()
            return

        self.currentWave += 1
        self.is_boss_wave = self._ShouldStartBossWave(self.currentWave)

        if self.is_boss_wave:
            self.StartBossBattle()
        else:
            self.SpawnWaveEnemies()

    def EndWave(self) -> None:
        if self.is_boss_wave:
            self.EndBossBattle()
            self.boss_waves_completed += 1
        else:
            self.normal_waves_completed += 1

        self._RecalculateDifficulty()
            
        if self.HasReachedFinalWave():
            self.EndGame()

    def SetWaveLimit(self, final_wave: int) -> None:
        self.final_wave = max(1, final_wave)
        if self.currentWave > self.final_wave:
            self.currentWave = self.final_wave

    def SetInfiniteWaves(self) -> None:
        self.final_wave = None

    def SetCurrentWave(self, wave: int) -> None:
        bounded_wave = max(0, wave)
        if self.final_wave is not None:
            bounded_wave = min(bounded_wave, self.final_wave)
        self.currentWave = bounded_wave

    def IncreaseCurrentWave(self, amount: int = 1) -> None:
        self.SetCurrentWave(self.currentWave + max(0, amount))

    def DecreaseCurrentWave(self, amount: int = 1) -> None:
        self.SetCurrentWave(self.currentWave - max(0, amount))

    def HasReachedFinalWave(self) -> bool:
        return self.final_wave is not None and self.currentWave >= self.final_wave

    def SetMaxDifficulty(self, max_difficulty: float | None) -> None:
        self.max_difficulty = max(0.0, max_difficulty) if max_difficulty is not None else None
        self._ApplyDifficultyCap()

    def SetInfiniteDifficulty(self) -> None:
        self.max_difficulty = None

    def SetStartingDifficulty(self, difficulty: float) -> None:
        bounded_difficulty = max(0.0, difficulty)
        if self.max_difficulty is not None:
            bounded_difficulty = min(bounded_difficulty, self.max_difficulty)
        self.starting_difficulty = bounded_difficulty
        self._RecalculateDifficulty()

    def IncreaseStartingDifficulty(self, amount: float = 0.1) -> None:
        self.SetStartingDifficulty(self.starting_difficulty + max(0.0, amount))

    def DecreaseStartingDifficulty(self, amount: float = 0.1) -> None:
        self.SetStartingDifficulty(self.starting_difficulty - max(0.0, amount))

    def SpawnWaveEnemies(self) -> None:
        # Placeholder hook for enemy/turret/projectile systems.
        pass

    def StartBossBattle(self) -> None:
        self.boss_alive = True
        self.SpawnBoss()

    def EndBossBattle(self) -> None:
        self.boss_alive = False
        self.is_boss_wave = False

    def SpawnBoss(self) -> None:
        # Placeholder hook for boss spawn logic.
        pass

    def _ShouldStartBossWave(self, waveNumber: int) -> bool:
        if self._IsFinalWave(waveNumber):
            return True
        return self.boss_wave_interval > 0 and waveNumber % self.boss_wave_interval == 0

    def _IsFinalWave(self, waveNumber: int) -> bool:
        return self.final_wave is not None and waveNumber == self.final_wave

    def _RecalculateDifficulty(self) -> None:
        raw_difficulty = (
            self.starting_difficulty
            + (self.normal_waves_completed * self.wave_difficulty_increase)
            + (self.boss_waves_completed * self.boss_difficulty_increase)
        )
        self.difficulty = round(raw_difficulty, 6)
        self._ApplyDifficultyCap()

    def _ApplyDifficultyCap(self) -> None:
        if self.max_difficulty is not None:
            self.difficulty = min(self.difficulty, self.max_difficulty)

    def Update(self, deltaTime: float) -> None:
        for obj in self.spawnedWaveTurrets:
            if obj._destroyed:
                self.spawnedWaveTurrets.remove(obj)
        
        return
