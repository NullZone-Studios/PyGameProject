import random
from collections import deque
import pygame
from pygame import Vector3

from Components.collider import BoxCollider
from GameEssentials import GameObject, GameWorld
from Components import ShapeRenderer,  DebugColliderRenderer, Script, AudioSource
from .turretShooter import CrystalTurret, OrbitTurret, BaseTurret
from .collisionLogger import CollisionLogger
from .rotator import Rotator

class GameMaster(Script):

    CurrentGameMaster = None

    def __init__(
        self,
        boss_wave_interval: int = 5,
        starting_difficulty: float = 1.0,
        wave_difficulty_increase: float = 0.1,
        boss_difficulty_increase: float = 0.2,
        final_wave: int = 10,
        max_difficulty: float | None = None,
    ) -> None:
        if GameMaster.CurrentGameMaster is not None:
            raise Exception("GameMaster instance already exists! Multiple instances of GameMaster are not allowed.")
        super().__init__()
        self.currentWave = 0
        self.starting_difficulty = max(0.0, starting_difficulty)
        self.difficulty = self.starting_difficulty
        self.wave_difficulty_increase = max(0.0, wave_difficulty_increase)
        self.boss_difficulty_increase = max(0.0, boss_difficulty_increase)
        self.boss_wave_interval = boss_wave_interval
        self.spawnedWaveTurrets: list[GameObject] = []
        self.yet_to_spawn_turrets: deque[GameObject] = deque()
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
        self.starting_turrets_shooting_delay = 5.0
        self.cooldown_before_shooting = self._recalculateShootingCooldown()
        self.currentActiveTurret : BaseTurret | None = None
        self.baseActiveTurretMinimumShoots = 2
        self.baseActiveTurretMaximumShoots = 5
        self.currentActiveTurretShoots = random.randint(self.baseActiveTurretMinimumShoots, self.baseActiveTurretMaximumShoots)
        self.spawnLocations = {
            "top": Vector3(20, 0, -20),
            "bottom": Vector3(-20, 0, 20),
            "left": Vector3(-20, 0, -20),
            "right": Vector3(20, 0, 20),
            "outerRim": Vector3(0, 0, -40)
        }
        self._spawn_location_keys = tuple(self.spawnLocations.keys())
        self._active_spawn_slots: set[str] = set()
        self.currentScore = 0

    def Awake(self) -> None:
        GameMaster.CurrentGameMaster = self
        return super().Awake()
    
    @property
    def gameObjects(self) -> list[GameObject]:
        return GameWorld.GetInstance().GameObjects

    def AddObject(self, obj: GameObject) -> None:
        if obj._destroyed or obj in self.spawnedWaveTurrets or self.GameObject is None:
            return
        self.GameObject.AddChild(obj)
        self.spawnedWaveTurrets.append(obj)
        spawn_slot = getattr(obj, "_spawn_slot", None)
        if isinstance(spawn_slot, str):
            self._active_spawn_slots.add(spawn_slot)
            
    def RemoveObject(self, obj: GameObject) -> None:
        if self.GameObject is not None and obj.Parent is self.GameObject:
            self.GameObject.RemoveChild(obj)
        if obj in self.spawnedWaveTurrets:
            self.spawnedWaveTurrets.remove(obj)
        spawn_slot = getattr(obj, "_spawn_slot", None)
        if isinstance(spawn_slot, str):
            self._active_spawn_slots.discard(spawn_slot)
        if not obj._destroyed:
            obj.Destroy()

    def StartGame(self) -> None:
        # Clean up any leftover enemies from a previous run before resetting state.
        for obj in self.spawnedWaveTurrets:
            if self.GameObject is not None and obj.Parent is self.GameObject:
                self.GameObject.RemoveChild(obj)
            if not obj._destroyed:
                obj.Destroy()
        for obj in self.yet_to_spawn_turrets:
            if not obj._destroyed:
                obj.Destroy()

        self.is_running = True
        self.is_paused = False
        self.is_game_over = False
        self.currentWave = 0
        self.normal_waves_completed = 0
        self.boss_waves_completed = 0
        self.difficulty = self.starting_difficulty
        self.is_boss_wave = False
        self.boss_alive = False
        self.currentScore = 0
        self.yet_to_spawn_turrets.clear()
        self.spawnedWaveTurrets.clear()
        self._active_spawn_slots.clear()
        from .player import Player
        player = Player.PlayerObject.GetFirstComponentOfType(Player)
        player.ActivateShooting()
        player.life = 3
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
        from .player import Player
        Player.PlayerObject.GetFirstComponentOfType(Player).ActivateShooting()

    def StartWave(self) -> None:
        if self.HasReachedFinalWave():
            self.EndGame()
            return

        self.IncreaseCurrentWave(1)
        self.is_boss_wave = self._ShouldStartBossWave(self.currentWave)
        self.cooldown_before_shooting = self._recalculateShootingCooldown()

        if self.is_boss_wave:
            self.StartBossBattle()
        else:
            self.PrepareWaveEnemies()

    def EndWave(self) -> None:
        
        if self.is_boss_wave:
            self.EndBossBattle()
            self.currentScore += int(500 * self.difficulty)  # Bonus for defeating boss wave
            self.boss_waves_completed += 1
        else:
            self.currentScore += int(250 * self.difficulty)  # Bonus for completing normal wave
            self.normal_waves_completed += 1

        self._RecalculateDifficulty()
            
        if self.HasReachedFinalWave():
            self.EndGame()
        else:
            self.StartWave()

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

        # If this wave is large enough, guarantee one spawn from each location first.
        if target_enemy_count > 5:
            guaranteed_locations = list(self._spawn_location_keys)
            random.shuffle(guaranteed_locations)
            for spawn_name in guaranteed_locations:
                self.yet_to_spawn_turrets.append(self._BuildWaveTurret(spawn_name=spawn_name))

            remaining = target_enemy_count - len(guaranteed_locations)
            for _ in range(remaining):
                self.yet_to_spawn_turrets.append(self._BuildWaveTurret())
        else:
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

    def _BuildWaveTurret(self, spawn_name: str | None = None) -> GameObject:
        if spawn_name is None:
            spawn_name = random.choice(self._spawn_location_keys)
        turret = GameObject(f"WaveTurret_{self.currentWave}_{len(self.yet_to_spawn_turrets)}", "Enemy")
        turret.Transform.Position = Vector3(self.spawnLocations[spawn_name])
        turret._spawn_slot = spawn_name  # type: ignore
        turret.AddComponent(BoxCollider(pygame.Vector3(2, 2, 2)))
        turret.AddComponent(CollisionLogger(pygame.Vector3(1, 1, 1), "Turret"))
        turret.AddComponent(DebugColliderRenderer())
        turret.AddComponent(Rotator())
        if spawn_name == "outerRim":
            turret.AddComponent(ShapeRenderer(shape="cube", color=pygame.Color(255, 200, 255)))
            turret.AddComponent(OrbitTurret(fire_interval=max(0.5, 5 / max(1.0, self.difficulty)), orbit_center=Vector3(0,0,0), orbit_radius=20.0, orbit_angular_speed=0.50, orbit_clockwise=random.choice([True, False])))
        else:
            turret.AddComponent(CrystalTurret(fire_interval=max(0.5, 5 / max(1.0, self.difficulty))))
            turret.AddComponent(ShapeRenderer(shape="crystal", color=pygame.Color(200, 255, 255)))
        turret.AddComponent(AudioSource(f"spawn_{turret.__hash__()}", "src/sound/spawn_turret.wav"))
        turret.AddComponent(AudioSource(f"shoot_{turret.__hash__()}", "src/sound/shoot_sound.wav"))
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

        next_turret = self.yet_to_spawn_turrets.popleft()
        spawn_slot = getattr(next_turret, "_spawn_slot", None)
        if isinstance(spawn_slot, str) and spawn_slot in self._active_spawn_slots:
            self.yet_to_spawn_turrets.appendleft(next_turret)
            return
        self.AddObject(next_turret)
        audioSources = next_turret.GetAllComponentsOfType(AudioSource)
        for audioSource in audioSources:
            if audioSource.soundName == f"spawn_{next_turret.__hash__()}":
                audioSource.Play()
        self.time_until_next_enemy_spawn = self._CalculateNextSpawnDelay(self._GetActiveEnemyCount())

    def EasyMode(self) -> None:
        self.starting_difficulty = 1.0
        self.wave_difficulty_increase = 0.1
        self.boss_difficulty_increase = 0.2
        self._RecalculateDifficulty()
        
    def HardMode(self) -> None:  
        self.starting_difficulty = 2.0
        self.wave_difficulty_increase = 0.3
        self.boss_difficulty_increase = 0.5
        self._RecalculateDifficulty()
        
    def InsaneMode(self) -> None:
        self.starting_difficulty = 4.0
        self.wave_difficulty_increase = 0.5
        self.boss_difficulty_increase = 1.0
        self._RecalculateDifficulty()
    
    def _recalculateShootingCooldown(self) -> float:
        return max(0.5, self.starting_turrets_shooting_delay / max(1.0, self.difficulty))

    def _GetRandomShooter(self) -> BaseTurret | None:
        shooters: list[BaseTurret] = []
        for turret_obj in self.spawnedWaveTurrets:
            if turret_obj._destroyed:
                continue
            shooter = turret_obj.GetFirstComponentOfType(CrystalTurret)
            if shooter is None:
                shooter = turret_obj.GetFirstComponentOfType(OrbitTurret)
            if shooter is not None:
                shooters.append(shooter)
        if not shooters:
            return None
        return random.choice(shooters)
        
    
    def Update(self, deltaTime: float) -> None:
        surviving_turrets: list[GameObject] = []
        destroyed_count = 0
        for obj in self.spawnedWaveTurrets:
            if obj._destroyed:
                destroyed_count += 1
                if self.GameObject is not None and obj.Parent is self.GameObject:
                    self.GameObject.RemoveChild(obj)
                spawn_slot = getattr(obj, "_spawn_slot", None)
                if isinstance(spawn_slot, str):
                    self._active_spawn_slots.discard(spawn_slot)
            else:
                surviving_turrets.append(obj)
        self.currentScore += int(15 * self.difficulty * destroyed_count)
        self.spawnedWaveTurrets = surviving_turrets

        if not self.is_running or self.is_paused or self.is_game_over:
            return

        if self.is_boss_wave:
            return

        if (len(self.yet_to_spawn_turrets) == 0) and (self._GetActiveEnemyCount() == 0 and not self.boss_alive):
            self.EndWave()
            return

        if not self.yet_to_spawn_turrets:
            return

        if len(self.spawnedWaveTurrets) == 0 and len(self.yet_to_spawn_turrets) == 0:
            self.EndWave()
            return
        
        self.cooldown_before_shooting -= deltaTime
        if self.cooldown_before_shooting <= 0:
            if not self.currentActiveTurret or self.currentActiveTurret.GameObject._destroyed:
                self.currentActiveTurret = self._GetRandomShooter()
                self.currentActiveTurretShoots = random.randint(self.baseActiveTurretMinimumShoots, self.baseActiveTurretMaximumShoots)
            self.cooldown_before_shooting = self._recalculateShootingCooldown()
            if self.spawnedWaveTurrets and self.currentActiveTurret and not self.currentActiveTurret.GameObject._destroyed:
                self.currentActiveTurret.Shoot()
                self.currentActiveTurretShoots -= 1
                if self.currentActiveTurretShoots == 0:
                    self.currentActiveTurretShoots = random.randint(self.baseActiveTurretMinimumShoots, self.baseActiveTurretMaximumShoots)
                    self.currentActiveTurret = self._GetRandomShooter()

        
        self.time_until_next_enemy_spawn -= deltaTime
        if self.time_until_next_enemy_spawn <= 0:
            self._TrySpawnNextEnemy()

        return
