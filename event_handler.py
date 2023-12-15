import pygame


def event_handler(event, level):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if not level.player.timers["tool_switch"].active:
            level.player.change_tool()
