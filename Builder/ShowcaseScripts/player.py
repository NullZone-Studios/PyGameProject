from Builder.ShowcaseScripts.GameInput import GameInputLayer, MouseKeys
from Components.script import Script
import pygame

from Components import ShapeRenderer, BoxCollider, AudioSource
from GameEssentials.Input.buttonState import ButtonState
from .turretShooter import Projectile
from GameEssentials import GameObject, GameWorld
from typing import Optional
import random


class Player(Script):
    PlayerObject: GameObject = None
    
    def __init__(self, inputLayer: GameInputLayer):
        if Player.PlayerObject is not None:
            raise Exception("Player already exists! Multiple instances of Player are not allowed.")
        super().__init__()
        self.screen: pygame.Surface = pygame.display.get_surface()
        self.base_shoot_cooldown = 1.0
        self.shoot_cooldown = 0.0
        self.inputLayer = inputLayer
        self.life = 3
        self.shootingActivated = False
        self.invulnerability_time = 1.0  # Time remaining for invulnerability after being hit
        self._AudioSource: AudioSource = None
        
    def Shoot(self, position: Optional[pygame.Vector2] = None):
        if self.shoot_cooldown <= 0:
            camera_obj = None
            if GameWorld.GetInstance().MainCamera:
                camera_obj = GameWorld.GetInstance().MainCamera.GameObject
            if camera_obj is None:
                camera_obj = GameWorld.GetInstance().FindByTag("Camera")

            source_obj = camera_obj if camera_obj is not None else self.GameObject
            direction = -source_obj.Transform.Forward
            self._spawn_projectile(direction, spawn_origin=source_obj.Transform.WorldPosition)
            self.shoot_cooldown = self.base_shoot_cooldown
            if self._AudioSource and self._AudioSource.soundName == "player_shoot":
                self._AudioSource.Play()
    
    def ActivateShooting(self):
        self.shootingActivated = not self.shootingActivated
        if self.shootingActivated:
            self.inputLayer.AddKeyEvent(pygame.K_SPACE, ButtonState.PRESSED, self.Shoot)
            self.inputLayer.AddMouseButtonEvent(MouseKeys.LEFT, ButtonState.PRESSED, self.Shoot)
            
        else:
            self.inputLayer.RemoveKeyEvent(pygame.K_SPACE, ButtonState.PRESSED, self.Shoot)
            self.inputLayer.RemoveMouseButtonEvent(MouseKeys.LEFT, ButtonState.PRESSED, self.Shoot)
    
    def Start(self):
        self._AudioSource = self.GameObject.GetFirstComponentOfType(AudioSource)
        Player.PlayerObject = self.GameObject
        return super().Start()
        
    
    def _spawn_projectile(self, direction: pygame.Vector3, spawn_origin: pygame.Vector3 | None = None):
        projectile = GameObject("CrystalShot", "Projectile")
        origin = spawn_origin if spawn_origin is not None else self.GameObject.Transform.WorldPosition
        projectile.Transform.Position = origin + direction * 1.2
        projectile.AddComponent(
            ShapeRenderer(
                shape="cone",
                color=pygame.Color("darkgoldenrod2"),
                scale=(0.2, 0.2, 0.2),
            )
        )
        projectile.AddComponent(BoxCollider(pygame.Vector3(0.3, 0.3, 0.3)))
        projectile.AddComponent(
            Projectile(
                direction=direction,
                speed=35.0,
                lifetime=5.0,
                owner=self.GameObject,
            )
        )
        projectile.AddComponent(AudioSource(soundName=f"projectile_{self.__hash__()}_{random.randint(1, 1000)}", soundPath="src/sound/energy_sound.wav", autoPlay=True, loop=True))
        GameWorld.GetInstance().Instantiate(projectile)
        projectile.Awake()
        projectile.Start()
            
    def Update(self, deltaTime):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= deltaTime
            
        if self.invulnerability_time > 0:
            self.invulnerability_time -= deltaTime
            
    def OnCollisionEnter(self, other):
        if other.GameObject.Tag == "Projectile" and other.GameObject.GetComponent(Projectile).owner.Tag != "Player" and self.invulnerability_time <= 0:
            self.life -= 1
            self.invulnerability_time = 1.0  # Set invulnerability time to 1 second
            print(f"Player hit! Remaining life: {self.life}")
            if self.life <= 0:
                print("Player has been destroyed!")
                from .gameMaster import GameMaster
                GameMaster.CurrentGameMaster.EndGame()
        return super().OnCollisionEnter(other)
