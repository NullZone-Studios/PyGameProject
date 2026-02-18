import math
import pygame
from GameEssentials import GameObject, GameWorld
from Components import BoxCollider, ShapeRenderer, Script, AudioSource


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
        projectile.AddComponent(AudioSource(soundName=f"projectile_{self.__hash__()}", soundPath="src/sound/energy_sound.wav", autoPlay=True, loop=True))
        GameWorld.GetInstance().Instantiate(projectile)
        projectile.Awake()
        projectile.Start()
        if self._shoot_sound:
            self._shoot_sound.Play()
    
    def OnCollisionEnter(self, other):
        if other.tag == "Projectile" and other.GetComponent(Projectile).owner.tag == "Player":
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
        # self._elapsed += deltaTime
        # target = self._get_target()
        # if not target:
        #     return

        # turret_pos = self.GameObject.Transform.WorldPosition
        # target_pos = target.Transform.WorldPosition
        # direction = target_pos - turret_pos
        # if direction.length() == 0:
        #     return
        # direction.normalize_ip()

        # self._aim_at(direction)

        # self._cooldown -= deltaTime
        # if self._cooldown <= 0:
        #     self._cooldown = self._current_interval()
        #     self._spawn_projectile(direction)



class RimTurret(BaseTurret):
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
