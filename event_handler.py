import pygame


def event_handler(event, level):
    if event.type == pygame.MOUSEWHEEL:
        if not level.player.timers["tool_switch"].active:
            if event.y > 0:
                level.player.change_tool("up")
            elif event.y < 0:
                level.player.change_tool("down")
