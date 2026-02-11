from __future__ import annotations

from GameEssentials import GameObject

class GameMaster:
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
        self.starting_difficulty = starting_difficulty
        self.difficulty = starting_difficulty
        self.wave_difficulty_increase = wave_difficulty_increase
        self.boss_difficulty_increase = boss_difficulty_increase
        self.boss_wave_interval = boss_wave_interval
        self.final_wave: int | None = final_wave if final_wave > 0 else None
        self.max_difficulty: float | None = max_difficulty
        self.normal_waves_completed = 0
        self.boss_waves_completed = 0
        self.is_boss_wave = False
        self.boss_alive = False
        self.is_running = False
        self.is_paused = False
        self.is_game_over = False

    @property
    def gameObjects(self) -> list[GameObject]:
        from GameWorld import GameWorld
        return GameWorld.GameObjects

    def AddObject(self, obj: GameObject) -> None:
        from GameWorld import GameWorld

        if obj not in GameWorld.GameObjects:
            GameWorld.Instantiate(obj)
            obj.Awake()
            obj.Start()

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
        self.final_wave = final_wave if final_wave > 0 else None

    def SetInfiniteWaves(self) -> None:
        self.final_wave = None

    def HasReachedFinalWave(self) -> bool:
        return self.final_wave is not None and self.currentWave >= self.final_wave

    def SetMaxDifficulty(self, max_difficulty: float | None) -> None:
        self.max_difficulty = max_difficulty
        self._ApplyDifficultyCap()

    def SetInfiniteDifficulty(self) -> None:
        self.max_difficulty = None

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
        # Engine.Update owns object update + culling.
        # GameMaster.Update is reserved for high-level game state logic only.
        return
