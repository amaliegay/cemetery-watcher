import pygame

from settings import *
from tools import *
from spells import *
from utils import *


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports
        self.tools_surface = {}
        for tool_id in tools.keys():
            self.tools_surface[tool_id] = import_asset(
                "assets/Objects/", tools[tool_id]
            )

        self.spells_surface = {}
        for spell_id in spells.keys():
            self.spells_surface[spell_id] = import_asset(
                "assets/Objects/", spells[spell_id]
            )

    def display(self):
        # tools
        tool_surface = self.tools_surface[self.player.readied_tool]
        tool_rect = tool_surface.get_rect(midbottom=OVERLAY_POSITION["tool"])
        self.display_surface.blit(tool_surface, tool_rect)

        # spell
        spell_surface = self.spells_surface[self.player.readied_spell]
        spell_rect = spell_surface.get_rect(midbottom=OVERLAY_POSITION["spell"])
        self.display_surface.blit(spell_surface, spell_rect)
