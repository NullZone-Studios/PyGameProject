import pygame
import math

from Components.script import Script
from Builder.ShowcaseScripts.gameMaster import GameMaster
from Builder.ShowcaseScripts.player import Player
from GameEssentials import GameWorld


class CameraController(Script):
    def __init__(
        self,
        menu_offset: pygame.Vector3 = pygame.Vector3(0, 20, 0),
        gameplay_offset: pygame.Vector3 = pygame.Vector3(0, 0, 0),
        menu_lerp_speed: float = 3.0,
        gameplay_lerp_speed: float = 10.0,
    ) -> None:
        super().__init__()
        self.menu_offset = pygame.Vector3(menu_offset)
        self.gameplay_offset = pygame.Vector3(gameplay_offset)
        self.menu_lerp_speed = max(0.01, menu_lerp_speed)
        self.gameplay_lerp_speed = max(0.01, gameplay_lerp_speed)

    def _get_player_object(self):
        if Player.PlayerObject is not None:
            return Player.PlayerObject
        return GameWorld.GetInstance().FindByTag("Player")

    def _lerp_position(self, target: pygame.Vector3, deltaTime: float, speed: float) -> None:
        current = self.GameObject.Transform.Position
        t = min(1.0, speed * deltaTime)
        self.GameObject.Transform.SetPosition(current.lerp(target, t))

    def _look_at_target(self, target_world_position: pygame.Vector3) -> None:
        cam_pos = self.GameObject.Transform.Position
        direction = target_world_position - cam_pos
        if direction.length_squared() == 0:
            return
        direction.normalize_ip()

        yaw = math.atan2(direction.x, direction.z)
        ground = math.hypot(direction.x, direction.z)
        pitch = math.atan2(-direction.y, ground)
        self.GameObject.Transform.SetRotation(pygame.Vector3(pitch, yaw, 0))

    def Start(self) -> None:
        player_obj = self._get_player_object()
        if player_obj is None:
            return
        player_pos = player_obj.Transform.Position
        self.GameObject.Transform.SetPosition(player_pos + self.menu_offset)
        self._look_at_target(player_pos)

    def _update_menu_camera(self, player_obj, deltaTime: float) -> None:
        player_pos = player_obj.Transform.Position
        target_pos = player_pos + self.menu_offset
        self._lerp_position(target_pos, deltaTime, self.menu_lerp_speed)
        self._look_at_target(player_pos)

    def _update_gameplay_camera(self, player_obj, deltaTime: float) -> None:
        forward = player_obj.Transform.Forward
        if forward.length() == 0:
            forward = pygame.Vector3(0, 0, 1)

        right = player_obj.Transform.Right
        up = player_obj.Transform.Up
        target_pos = (
            player_obj.Transform.Position
            + (right * self.gameplay_offset.x)
            + (up * self.gameplay_offset.y)
            - (forward * self.gameplay_offset.z)
        )

        self._lerp_position(target_pos, deltaTime, self.gameplay_lerp_speed)
        self._look_at_target(player_obj.Transform.Position)

    def Update(self, deltaTime: float) -> None:
        player_obj = self._get_player_object()
        if player_obj is None:
            return

        game_master = GameMaster.CurrentGameMaster
        is_playing = bool(game_master and game_master.is_running and not game_master.is_game_over)

        if is_playing:
            self._update_gameplay_camera(player_obj, deltaTime)
        else:
            self._update_menu_camera(player_obj, deltaTime)
