from queue import PriorityQueue
from queue import Queue
import math
import pygame

def manhatten(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def civ(p1, p2):
    return (max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1])))

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star_decide(draw, grid, start, end, key):
    if key == pygame.K_m:
        a_star(draw, grid, start, end, manhatten)
    if key == pygame.K_e:
        a_star(draw, grid, start, end, euclidean)
    if key == pygame.K_a:
        a_star(draw, grid, start, end, civ)

def a_star(draw, grid, start, end, function):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = function(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + function(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False

def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False


def dfs(draw, start, end):
    def recursive_dfs(node, visited, came_from):

        visited.append(node)
        node.make_open()
        draw()

        if node == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in node.neighbours:
            if neighbour not in visited:
                came_from[neighbour] = node
                p = recursive_dfs(neighbour, visited, came_from)
                if p:
                    return p

        return False

    came_from = {}
    visited = []
    return recursive_dfs(start, visited, came_from)


def bfs(draw, start, end):
    queue = Queue()
    visited = []
    came_from = {}
    queue.put(start)
    visited.append(start)

    while not queue.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:

            if neighbour not in visited:
                visited.append(neighbour)
                queue.put(neighbour)
                came_from[neighbour] = current
                neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
