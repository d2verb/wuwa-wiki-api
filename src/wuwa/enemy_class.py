from enum import Enum


class EnemyClass(str, Enum):
    COMMON = "水風級"
    ELITE = "巨浪級"
    OVERLORD = "怒涛級"
    CALAMITY = "津波級"
