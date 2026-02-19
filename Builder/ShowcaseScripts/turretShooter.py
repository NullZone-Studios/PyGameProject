import math
import pygame
from GameEssentials import GameObject, GameWorld
from Components import BoxCollider, ShapeRenderer, Script, AudioSource
import random

class Projectile(Script):
    def __init__(self, direction: pygame.Vector3, speed: float = 12.0, lifetime: float = 5.0, owner: GameObject | None = None):
        super().__init__()
        self.direction = pygame.Vector3(direction)
        if self.direction.length() != 0:
            self.direction.normalize_ip()
        self.speed = speed
        self.lifetime = lifetime
        self.owner = owner

    def Start(self):
        self.audioSource = self.GameObject.GetFirstComponentOfType(AudioSource)

    def Update(self, deltaTime: float):
        self.lifetime -= deltaTime
        if self.lifetime <= 0:
            self.GameObject.Destroy()
            return

        move = self.direction * self.speed * deltaTime
        self.GameObject.Transform.Translate(move.x, move.y, move.z)

    def OnCollisionEnter(self, other: BoxCollider):
        if other.GameObject == self.owner:
            return
        else:
            self.GameObject.Destroy()
        
    def OnDestroy(self):
        if self.audioSource:
            self.audioSource.Stop()

class BaseTurret(Script):
    def __init__(self):
        super().__init__()
        self._shoot_sound: AudioSource = None
    
    def Shoot(self):
        target = self._get_target()
        if not target:
            return

        turret_pos = self.GameObject.Transform.WorldPosition
        target_pos = target.Transform.WorldPosition
        direction = target_pos - turret_pos
        if direction.length() == 0:
            return
        direction.normalize_ip()

        self._aim_at(direction)
        self._spawn_projectile(direction)
    
    def _current_interval(self) -> float:
        # 1% faster per second: interval scales by 1 / (1.01 ** t)
        return self.base_fire_interval / (1.01 ** self._elapsed)

    def _get_target(self) -> GameObject | None:
        from .player import Player
        if Player.PlayerObject:
            return Player.PlayerObject
        return GameWorld.GetInstance().FindByTag("Player")

    def _aim_at(self, direction: pygame.Vector3):
        yaw = math.atan2(direction.x, direction.z)
        ground = math.hypot(direction.x, direction.z)
        pitch = math.atan2(-direction.y, ground)
        self.GameObject.Transform.Rotation = pygame.Vector3(pitch, yaw, 0)

    def _spawn_projectile(self, direction: pygame.Vector3):
        projectile = GameObject("CrystalShot", "Projectile")
        projectile.Transform.Position = self.GameObject.Transform.WorldPosition + direction * 1.2
        projectile.AddComponent(
            ShapeRenderer(
                shape="cone",
                color=self.projectile_color,
                scale=self.projectile_scale,
            )
        )
        projectile.AddComponent(BoxCollider(pygame.Vector3(0.3, 0.3, 0.3)))
        projectile.AddComponent(
            Projectile(
                direction=direction,
                speed=self.projectile_speed,
                lifetime=self.projectile_lifetime,
                owner=self.GameObject,
            )
        )
        projectile.AddComponent(AudioSource(soundName=f"projectile_{self.__hash__()}_{random.randint(1, 1000)}", soundPath="src/sound/energy_sound.wav", autoPlay=True, loop=True))
        GameWorld.GetInstance().Instantiate(projectile)
        projectile.Awake()
        projectile.Start()
        if self._shoot_sound:
            self._shoot_sound.Play()
    
    def OnCollisionEnter(self, other):
        if other.GameObject.Tag == "Projectile" and other.GameObject.GetComponent(Projectile).owner.Tag == "Player":
            self.GameObject.Destroy()

class CrystalTurret(BaseTurret):
    def __init__(
        self,
        fire_interval: float = 5.0,
        projectile_speed: float = 12.0,
        projectile_lifetime: float = 5.0,
        projectile_scale: tuple[float, float, float] = (0.2, 0.2, 0.2),
        projectile_color: pygame.Color = pygame.Color(255, 80, 80),
    ):
        super().__init__()
        self.base_fire_interval = fire_interval
        self.projectile_speed = projectile_speed
        self.projectile_lifetime = projectile_lifetime
        self.projectile_scale = projectile_scale
        self.projectile_color = projectile_color
        self._cooldown = 0.0
        self._elapsed = 0.0
        

    def Start(self):
        self._cooldown = self._current_interval()


    def Update(self, deltaTime: float):
        if not self._shoot_sound:
            for comp in self.GameObject.GetAllComponentsOfType(AudioSource):
                if comp.soundName == f"shoot_{self.GameObject.__hash__()}":
                    self._shoot_sound = comp
                    break

class MFOrbitTurret(BaseTurret):
    def __init__(
        self,
        fire_interval: float = 5.0,
        projectile_speed: float = 12.0,
        projectile_lifetime: float = 5.0,
        projectile_scale: tuple[float, float, float] = (0.2, 0.2, 0.2),
        projectile_color: pygame.Color = pygame.Color(255, 80, 80),
        orbit_center: pygame.Vector3 = pygame.Vector3(0, 0, 0),
        orbit_radius: float = 20.0,
        orbit_angular_speed: float = 0.9,
        orbit_clockwise: bool = True,
    ):
        super().__init__()
        self.base_fire_interval = fire_interval
        self.projectile_speed = projectile_speed
        self.projectile_lifetime = projectile_lifetime
        self.projectile_scale = projectile_scale
        self.projectile_color = projectile_color
        self.orbit_center = pygame.Vector3(orbit_center)
        self.orbit_radius = max(0.1, orbit_radius)
        self.orbit_angular_speed = max(0.0, orbit_angular_speed)
        self.orbit_clockwise = orbit_clockwise
        self._cooldown = 0.0
        self._elapsed = 0.0
        self._shoot_sound: AudioSource = None
        self._orbit_angle = 0.0
        self._orbit_height = 0.0
        self._ai_change_timer = 0.0
        self._base_change_interval_min = 2.0
        self._base_change_interval_max = 4.0
        self._base_min_speed = 0.25
        self._base_max_speed = 0.9
        self._max_speed_cap = 3.5
        self._base_flip_chance = 0.30
        self.max_life = 3
        self.current_life = 3
        self._shot_timer = 0.0
        self._next_shot_delay = self.base_fire_interval
        self._base_projectile_speed = projectile_speed
    
    def Start(self):
        from .gameMaster import GameMaster

        current_pos = self.GameObject.Transform.Position
        self._orbit_height = current_pos.y

        offset = current_pos - self.orbit_center
        radial = pygame.Vector2(offset.x, offset.z)
        if radial.length_squared() > 0:
            self.orbit_radius = radial.length()
            self._orbit_angle = math.atan2(offset.z, offset.x)
        else:
            self._orbit_angle = 0.0

        game_master = GameMaster.CurrentGameMaster
        difficulty = max(1.0, game_master.difficulty) if game_master is not None else 1.0

        # Difficulty-scaled life range:
        # low difficulty trends around [3..5], high difficulty trends toward [5..10].
        min_life = min(10, max(3, int(3 + (difficulty - 1.0) * 0.7)))
        max_life = min(10, max(min_life, int(5 + (difficulty - 1.0) * 1.2)))
        self.max_life = random.randint(min_life, max_life)
        self.current_life = self.max_life

        self.BasicAIChanger()
        self._next_shot_delay = self._RollNextShotDelay(difficulty)
        self._shot_timer = self._next_shot_delay

    def _GetDifficulty(self) -> float:
        from .gameMaster import GameMaster

        game_master = GameMaster.CurrentGameMaster
        return max(1.0, game_master.difficulty) if game_master is not None else 1.0

    def _RollNextShotDelay(self, difficulty: float) -> float:
        # Higher difficulty shoots faster and with less predictable gaps.
        base_min = max(0.18, self.base_fire_interval / (1.0 + difficulty * 0.35))
        base_max = max(base_min + 0.05, self.base_fire_interval / (1.0 + difficulty * 0.12))
        variance = random.uniform(-0.25, 0.25) * (1.0 + difficulty * 0.35)
        return max(0.12, random.uniform(base_min, base_max) + variance)
    
    def BasicAIChanger(self):
        difficulty = self._GetDifficulty()

        # Harder difficulty increases speed ceiling and unpredictability.
        min_speed = max(0.1, self._base_min_speed + (difficulty * 0.08))
        max_speed = min(self._max_speed_cap, self._base_max_speed + (difficulty * 0.35))
        if max_speed <= min_speed:
            max_speed = min_speed + 0.1
        self.orbit_angular_speed = random.uniform(min_speed, max_speed)

        # Direction flips become more likely with higher difficulty.
        flip_chance = min(0.95, self._base_flip_chance + (difficulty * 0.08))
        if random.random() < flip_chance:
            self.orbit_clockwise = not self.orbit_clockwise
        else:
            self.orbit_clockwise = random.choice([True, False])

        # Wait-time variance grows with difficulty.
        base_wait = random.uniform(self._base_change_interval_min, self._base_change_interval_max)
        variance = random.uniform(-0.5, 0.5) * (1.0 + (difficulty * 0.35))
        self._ai_change_timer = max(0.2, base_wait + variance)

        # Harder difficulty makes bullet speed harsher and more erratic.
        speed_min = max(8.0, self._base_projectile_speed * (0.8 + difficulty * 0.06))
        speed_max = max(speed_min + 0.5, self._base_projectile_speed * (1.0 + difficulty * 0.18))
        self.projectile_speed = random.uniform(speed_min, speed_max)
        
    def Update(self, deltaTime: float):
        if not self._shoot_sound:
            for comp in self.GameObject.GetAllComponentsOfType(AudioSource):
                if comp.soundName == f"shoot_{self.GameObject.__hash__()}":
                    self._shoot_sound = comp
                    break

        self._ai_change_timer -= deltaTime
        if self._ai_change_timer <= 0:
            self.BasicAIChanger()

        self._shot_timer -= deltaTime
        if self._shot_timer <= 0:
            self.Shoot()
            self._shot_timer = self._RollNextShotDelay(self._GetDifficulty())

        direction = -1.0 if self.orbit_clockwise else 1.0
        self._orbit_angle += direction * self.orbit_angular_speed * deltaTime

        new_x = self.orbit_center.x + math.cos(self._orbit_angle) * self.orbit_radius
        new_z = self.orbit_center.z + math.sin(self._orbit_angle) * self.orbit_radius
        self.GameObject.Transform.SetPosition(pygame.Vector3(new_x, self._orbit_height, new_z))

    def OnCollisionEnter(self, other):
        projectile = other.GameObject.GetFirstComponentOfType(Projectile)
        if other.GameObject.Tag == "Projectile" and projectile and projectile.owner and projectile.owner.Tag == "Player":
            self.current_life -= 1
            if self.current_life <= 0:
                self.GameObject.Destroy()
                
        
class OrbitTurret(BaseTurret):
    def __init__(
        self,
        fire_interval: float = 5.0,
        projectile_speed: float = 12.0,
        projectile_lifetime: float = 5.0,
        projectile_scale: tuple[float, float, float] = (0.2, 0.2, 0.2),
        projectile_color: pygame.Color = pygame.Color(255, 80, 80),
        orbit_center: pygame.Vector3 = pygame.Vector3(0, 0, 0),
        orbit_radius: float = 20.0,
        orbit_angular_speed: float = 0.9,
        orbit_clockwise: bool = True,
    ):
        super().__init__()
        self.base_fire_interval = fire_interval
        self.projectile_speed = projectile_speed
        self.projectile_lifetime = projectile_lifetime
        self.projectile_scale = projectile_scale
        self.projectile_color = projectile_color
        self.orbit_center = pygame.Vector3(orbit_center)
        self.orbit_radius = max(0.1, orbit_radius)
        self.orbit_angular_speed = max(0.0, orbit_angular_speed)
        self.orbit_clockwise = orbit_clockwise
        self._cooldown = 0.0
        self._elapsed = 0.0
        self._shoot_sound: AudioSource = None
        self._orbit_angle = 0.0
        self._orbit_height = 0.0

    def Start(self):
        current_pos = self.GameObject.Transform.Position
        self._orbit_height = current_pos.y

        offset = current_pos - self.orbit_center
        radial = pygame.Vector2(offset.x, offset.z)
        if radial.length_squared() > 0:
            self.orbit_radius = radial.length()
            self._orbit_angle = math.atan2(offset.z, offset.x)
        else:
            self._orbit_angle = 0.0
        
    def Update(self, deltaTime: float):
        if not self._shoot_sound:
            for comp in self.GameObject.GetAllComponentsOfType(AudioSource):
                if comp.soundName == f"shoot_{self.GameObject.__hash__()}":
                    self._shoot_sound = comp
                    break

        direction = -1.0 if self.orbit_clockwise else 1.0
        self._orbit_angle += direction * self.orbit_angular_speed * deltaTime

        new_x = self.orbit_center.x + math.cos(self._orbit_angle) * self.orbit_radius
        new_z = self.orbit_center.z + math.sin(self._orbit_angle) * self.orbit_radius
        self.GameObject.Transform.SetPosition(pygame.Vector3(new_x, self._orbit_height, new_z))
                
    def Shoot(self):
        target = self._get_target()
        if not target:
            return

        turret_pos = self.GameObject.Transform.WorldPosition
        target_pos = target.Transform.WorldPosition
        direction = target_pos - turret_pos
        if direction.length() == 0:
            return
        direction.normalize_ip()

        self._aim_at(direction)
        self._spawn_projectile(direction)

    def _get_target(self) -> GameObject | None:
        if GameWorld.GetInstance().MainCamera:
            return GameWorld.GetInstance().MainCamera.GameObject
        return GameWorld.GetInstance().FindByTag("Camera")

    def _aim_at(self, direction: pygame.Vector3):
        yaw = math.atan2(direction.x, direction.z)
        ground = math.hypot(direction.x, direction.z)
        pitch = math.atan2(-direction.y, ground)
        self.GameObject.Transform.Rotation = pygame.Vector3(pitch, yaw, 0)

    def _spawn_projectile(self, direction: pygame.Vector3):
        projectile = GameObject("CrystalShot", "Projectile")
        projectile.Transform.Position = self.GameObject.Transform.WorldPosition + direction * 1.2
        projectile.AddComponent(
            ShapeRenderer(
                shape="cone",
                color=self.projectile_color,
                scale=self.projectile_scale,
            )
        )
        projectile.AddComponent(BoxCollider(pygame.Vector3(0.3, 0.3, 0.3)))
        projectile.AddComponent(
            Projectile(
                direction=direction,
                speed=self.projectile_speed,
                lifetime=self.projectile_lifetime,
                owner=self.GameObject,
            )
        )
        GameWorld.GetInstance().Instantiate(projectile)
        projectile.Awake()
        projectile.Start()
        if self._shoot_sound:
            self._shoot_sound.Play()
