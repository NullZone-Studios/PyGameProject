from typing import Dict, List, Set, Tuple
from GameWorld import GameWorld
from Components.collider import BoxCollider
from GameEssentials.gameObject import GameObject

class CollisionSystem:
    _previous_pairs: Set[Tuple[int, int]] = set()
    _last_colliders: List[BoxCollider] = []

    @staticmethod
    def _collect_colliders(obj: GameObject, colliders: List[BoxCollider]) -> None:
        if obj.Enabled:
            for component in obj.Components:
                if isinstance(component, BoxCollider) and component.Enabled:
                    colliders.append(component)
            for child in obj.Children:
                CollisionSystem._collect_colliders(child, colliders)

    @staticmethod
    def _pair_key(a: BoxCollider, b: BoxCollider) -> Tuple[int, int]:
        ida = id(a)
        idb = id(b)
        return (ida, idb) if ida < idb else (idb, ida)

    @staticmethod
    def _notify(obj: GameObject, method: str, other: BoxCollider) -> None:
        for component in obj.Components:
            handler = getattr(component, method, None)
            if callable(handler):
                handler(other)

    @staticmethod
    def Update() -> None:
        colliders: List[BoxCollider] = []
        for obj in GameWorld.GameObjects:
            CollisionSystem._collect_colliders(obj, colliders)

        CollisionSystem._last_colliders = colliders

        collider_map: Dict[int, BoxCollider] = {id(c): c for c in colliders}

        current_pairs: Set[Tuple[int, int]] = set()

        for i in range(len(colliders)):
            a = colliders[i]
            for j in range(i + 1, len(colliders)):
                b = colliders[j]
                if a.Intersects(b):
                    pair = CollisionSystem._pair_key(a, b)
                    current_pairs.add(pair)
                    if pair in CollisionSystem._previous_pairs:
                        CollisionSystem._notify(a.GameObject, "OnCollisionStay", b)
                        CollisionSystem._notify(b.GameObject, "OnCollisionStay", a)
                    else:
                        CollisionSystem._notify(a.GameObject, "OnCollisionEnter", b)
                        CollisionSystem._notify(b.GameObject, "OnCollisionEnter", a)

        ended_pairs = CollisionSystem._previous_pairs - current_pairs
        for pair in ended_pairs:
            a = collider_map.get(pair[0])
            b = collider_map.get(pair[1])
            if not a or not b:
                continue
            CollisionSystem._notify(a.GameObject, "OnCollisionExit", b)
            CollisionSystem._notify(b.GameObject, "OnCollisionExit", a)

        CollisionSystem._previous_pairs = current_pairs

    @staticmethod
    def GetColliders() -> List[BoxCollider]:
        return list(CollisionSystem._last_colliders)
