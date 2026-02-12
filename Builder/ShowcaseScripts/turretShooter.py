import math
import pygame
from GameEssentials import GameObject
from GameWorld import GameWorld
from Components import BoxCollider, ShapeRenderer, Script


class Projectile(Script):
    def __init__(self, direction: pygame.Vector3, speed: float = 12.0, lifetime: float = 5.0, owner: GameObject | None = None):
        super().__init__()
        self.direction = pygame.Vector3(direction)
        if self.direction.length() != 0:
            self.direction.normalize_ip()
        self.speed = speed
        self.lifetime = lifetime
        self.owner = owner

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
        if other.GameObject.Tag == "Projectile":
            return
        self.GameObject.Destroy()


class CrystalTurret(Script):
    def __init__(
        self,
        fire_interval: float = 2.5,
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
        self._elapsed += deltaTime
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

        self._cooldown -= deltaTime
        if self._cooldown <= 0:
            self._cooldown = self._current_interval()
            self._spawn_projectile(direction)

    def _current_interval(self) -> float:
        # 1% faster per second: interval scales by 1 / (1.01 ** t)
        return self.base_fire_interval / (1.01 ** self._elapsed)

    def _get_target(self) -> GameObject | None:
        if GameWorld.MainCamera:
            return GameWorld.MainCamera.GameObject
        return GameWorld.FindByTag("Camera")

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
        GameWorld.Instantiate(projectile)
        projectile.Awake()
        projectile.Start()
