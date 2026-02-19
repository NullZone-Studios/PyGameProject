from Builder.ShowcaseScripts.GameInput import GameInputLayer, MouseKeys
from Builder.ShowcaseScripts.gameMaster import GameMaster
from Components.script import Script
import pygame

from Components import ShapeRenderer, BoxCollider, AudioSource
from GameEssentials.Input.buttonState import ButtonState
from .turretShooter import Projectile
from GameEssentials import GameObject, GameWorld
import random


class Player(Script):
    def __init__(self, inputLayer: GameInputLayer):
        super().__init__()
        self.screen: pygame.Surface = pygame.display.get_surface()
        self.base_shoot_cooldown = 1.0
        self.shoot_cooldown = 0.0
        self.inputLayer = inputLayer
        self.life = 3
        self.invulnerability_time = 0.0  # Time remaining for invulnerability after being hit
        self._AudioSource: AudioSource = None
        
        inputLayer.AddKeyEvent(pygame.K_SPACE, ButtonState.PRESSED, lambda : self.Shoot())
        inputLayer.AddMouseButtonEvent(MouseKeys.LEFT, ButtonState.PRESSED, lambda position: self.Shoot())
    
    def Start(self):
        self._AudioSource = self.GameObject.GetFirstComponentOfType(AudioSource)
        return super().Start()
        
    def Shoot(self):
        if self.shoot_cooldown <= 0:
            direction = -self.GameObject.Transform.Forward
            self._spawn_projectile(direction)
            self.shoot_cooldown = self.base_shoot_cooldown
            if self._AudioSource and self._AudioSource.soundName == "player_shoot":
                self._AudioSource.Play()
    
    
    def _spawn_projectile(self, direction: pygame.Vector3):
        projectile = GameObject("CrystalShot", "Projectile")
        projectile.Transform.Position = self.GameObject.Transform.WorldPosition + direction * 1.2
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
                speed=20.0,
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
                GameMaster.CurrentGameMaster.EndGame()  # Assuming there's an EndGame method to handle game over logic
                # Here you could add logic to handle player death, such as respawning or ending the game.
        return super().OnCollisionEnter(other)