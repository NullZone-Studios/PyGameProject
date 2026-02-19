import pygame
import math

from Components.script import Script
from Builder.ShowcaseScripts.gameMaster import GameMaster
from Builder.ShowcaseScripts.player import Player
from GameEssentials import GameWorld


class CameraController(Script):
    def __init__(
        self,
        menu_offset: pygame.Vector3 = pygame.Vector3(0, 24, 0),
        menu_lerp_duration: float = 1.0,
        gameplay_lerp_duration: float = 0.12,
        look_target_offset: pygame.Vector3 = pygame.Vector3(0, 1.0, 0),
    ) -> None:
        super().__init__()
        self.menu_offset = pygame.Vector3(menu_offset)
        self.menu_lerp_duration = max(0.01, menu_lerp_duration)
        self.gameplay_lerp_duration = max(0.01, gameplay_lerp_duration)
        self.look_target_offset = pygame.Vector3(look_target_offset)

    def _get_player_object(self):
        if Player.PlayerObject is not None:
            return Player.PlayerObject
        return GameWorld.GetInstance().FindByTag("Player")
        
    def _lerp_position(self, target: pygame.Vector3, deltaTime: float, duration: float) -> None:
        target = pygame.Vector3(target)
        current = self.GameObject.Transform.Position
        t = min(1.0, deltaTime / max(0.0001, duration))
        self.GameObject.Transform.SetPosition(current.lerp(target, t))

    def _lerp_rotation(self, target: pygame.Vector3, deltaTime: float, duration: float) -> None:
        current = self.GameObject.Transform.Rotation
        t = min(1.0, deltaTime / max(0.0001, duration))

        def _shortest_angle_delta(a: float, b: float) -> float:
            return (b - a + math.pi) % (2 * math.pi) - math.pi

        new_pitch = current.x + _shortest_angle_delta(current.x, target.x) * t
        new_yaw = current.y + _shortest_angle_delta(current.y, target.y) * t
        new_roll = current.z + _shortest_angle_delta(current.z, target.z) * t
        self.GameObject.Transform.SetRotation(pygame.Vector3(new_pitch, new_yaw, new_roll))

    def _look_at_target(self, target_world_position: pygame.Vector3) -> None:
        cam_pos = self.GameObject.Transform.WorldPosition
        direction = cam_pos - target_world_position
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
        player_pos = player_obj.Transform.WorldPosition + self.look_target_offset
        self.GameObject.Transform.SetPosition(player_pos + self.menu_offset)
        self._look_at_target(player_pos)

    def _update_menu_camera(self, player_obj, deltaTime: float) -> None:
        player_pos = player_obj.Transform.WorldPosition + self.look_target_offset
        target_pos = player_pos + self.menu_offset
        self._lerp_position(target_pos, deltaTime, self.menu_lerp_duration)
        self._look_at_target(player_pos)

    def _update_gameplay_camera(self, player_obj, deltaTime: float) -> None:
        target_pos = player_obj.Transform.WorldPosition

        self._lerp_position(target_pos, deltaTime, self.gameplay_lerp_duration)
        self._lerp_rotation(player_obj.Transform.Rotation, deltaTime, self.gameplay_lerp_duration)

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
