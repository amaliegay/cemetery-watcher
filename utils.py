from os import walk

import pygame


def import_folder(path):
    print("import_folder(" + path + ")")
    surface_list = []

    for dirpath, dirnames, filenames in walk(path):
        print(dirpath)
        print(dirnames)
        print(filenames)
        for image in filenames:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    print(surface_list)
    return surface_list
