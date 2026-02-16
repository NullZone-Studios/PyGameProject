from __future__ import annotations

import random
import pygame
from pygame import Vector3

from showcase import CollisionLogger, Rotator
from GameEssentials import GameObject, GameWorld
from Components import ShapeRenderer,  DebugColliderRenderer, Script
from .turretShooter import CrystalTurret

class GameMaster(Script):

    def __init__(
        self,
        boss_wave_interval: int = 5,
        starting_difficulty: float = 1.0,
        wave_difficulty_increase: float = 0.1,
        boss_difficulty_increase: float = 0.2,
        final_wave: int = 10,
        max_difficulty: float | None = None,
    ) -> None:
        super().__init__()
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
        self.base_enemies_per_wave = 2
        self.enemies_per_wave_growth = 1
        self.enemies_per_difficulty = 2.0
        self.base_spawn_interval = 2.0
        self.min_spawn_interval = 0.4
        self.max_spawn_interval = 4.0
        self.max_active_enemies_base = 2
        self.max_active_enemies_per_difficulty = 1.0
        self.time_until_next_enemy_spawn = 0.0
        self.spawnLocations = {
            "top": Vector3(0, 20, 20),
            "bottom": Vector3(0, -20, 20),
            "left": Vector3(-20, 0, 20),
            "right": Vector3(20, 0, 20),
        }
        self.currentScore = 0
        self._ApplyDifficultyCap()

    @property
    def gameObjects(self) -> list[GameObject]:
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
        self.StartWave()

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

        self.IncreaseCurrentWave(1)
        self.is_boss_wave = self._ShouldStartBossWave(self.currentWave)

        if self.is_boss_wave:
            self.StartBossBattle()
        else:
            self.PrepareWaveEnemies()

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

    def PrepareWaveEnemies(self) -> None:
        self.yet_to_spawn_turrets.clear()

        target_enemy_count = max(
            1,
            int(
                self.base_enemies_per_wave
                + (self.currentWave * self.enemies_per_wave_growth)
                + (self.difficulty * self.enemies_per_difficulty)
            ),
        )

        for _ in range(target_enemy_count):
            self.yet_to_spawn_turrets.append(self._BuildWaveTurret())

        self.time_until_next_enemy_spawn = self._CalculateNextSpawnDelay(self._GetActiveEnemyCount())
        self._TrySpawnNextEnemy()

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

    def _BuildWaveTurret(self) -> GameObject:
        spawn_name = random.choice(list(self.spawnLocations.keys()))
        turret = GameObject(f"WaveTurret_{self.currentWave}_{len(self.yet_to_spawn_turrets)}", "Enemy")
        turret.Transform.Position = Vector3(self.spawnLocations[spawn_name])
        turret.AddComponent(CollisionLogger(pygame.Vector3(1, 1, 1), "Crystal"))
        turret.AddComponent(DebugColliderRenderer())
        turret.AddComponent(Rotator())
        turret.AddComponent(CrystalTurret(fire_interval=max(0.5, 2.5 / max(1.0, self.difficulty))))
        turret.AddComponent(ShapeRenderer(shape="crystal", color=pygame.Color(220, 245, 255)))
        return turret

    def _GetActiveEnemyCount(self) -> int:
        return len(self.spawnedWaveTurrets)

    def _MaxActiveEnemies(self) -> int:
        return max(
            1,
            int(self.max_active_enemies_base + (self.difficulty * self.max_active_enemies_per_difficulty)),
        )

    def _CalculateNextSpawnDelay(self, active_enemies: int) -> float:
        difficulty_scale = max(0.35, 1.0 / (1.0 + (self.difficulty * 0.4)))
        active_enemy_penalty = 1.0 + (active_enemies * 0.25)
        delay = self.base_spawn_interval * difficulty_scale * active_enemy_penalty
        return max(self.min_spawn_interval, min(delay, self.max_spawn_interval))

    def _TrySpawnNextEnemy(self) -> None:
        if not self.yet_to_spawn_turrets:
            return

        if self._GetActiveEnemyCount() >= self._MaxActiveEnemies():
            return

        next_turret = self.yet_to_spawn_turrets.pop(0)
        for obj in self.spawnedWaveTurrets:
            if obj._destroyed:
                continue
            if obj.Transform.Position == next_turret.Transform.Position:
                self.yet_to_spawn_turrets.insert(0, next_turret)
                return
        self.AddObject(next_turret)
        self.time_until_next_enemy_spawn = self._CalculateNextSpawnDelay(self._GetActiveEnemyCount())

    def Update(self, deltaTime: float) -> None:
        self.spawnedWaveTurrets = [obj for obj in self.spawnedWaveTurrets if not obj._destroyed]

        if not self.is_running or self.is_paused or self.is_game_over:
            return

        if self.is_boss_wave:
            return

        if not self.yet_to_spawn_turrets:
            return

        self.time_until_next_enemy_spawn -= deltaTime
        if self.time_until_next_enemy_spawn <= 0:
            self._TrySpawnNextEnemy()

        return
