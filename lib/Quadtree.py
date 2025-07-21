import pygame


class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.tiles = []
        self.divided = False

    def count_tiles(self):
        count = len(self.tiles)
        if self.divided:
            count += self.northeast.count_tiles()
            count += self.northwest.count_tiles()
            count += self.southeast.count_tiles()
            count += self.southwest.count_tiles()
        return count

    def subdivide(self):
        x, y, w, h = self.boundary
        half_w, half_h = w // 2, h // 2

        self.northeast = Quadtree(
            pygame.Rect(x + half_w, y, half_w, half_h), self.capacity
        )
        self.northwest = Quadtree(pygame.Rect(x, y, half_w, half_h), self.capacity)
        self.southeast = Quadtree(
            pygame.Rect(x + half_w, y + half_h, half_w, half_h), self.capacity
        )
        self.southwest = Quadtree(
            pygame.Rect(x, y + half_h, half_w, half_h), self.capacity
        )

        self.divided = True

    def insert_group(self, sprite_group):
        for sprite in sprite_group:
            self.insert(sprite)

    def insert(self, tile):
        if not self.boundary.colliderect(tile.rect):
            return False

        if len(self.tiles) < self.capacity:
            self.tiles.append(tile)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northeast.insert(tile):
                return True
            if self.northwest.insert(tile):
                return True
            if self.southeast.insert(tile):
                return True
            if self.southwest.insert(tile):
                return True

    def query(self, range, found=None):
        if found is None:
            found = []

        if not self.boundary.colliderect(range):
            return found

        for tile in self.tiles:
            if range.colliderect(tile.rect):
                found.append(tile)

        if self.divided:
            self.northeast.query(range, found)
            self.northwest.query(range, found)
            self.southeast.query(range, found)
            self.southwest.query(range, found)

        return found

    def draw(self, surface, offset):
        adjusted_boundary = self.boundary.move(-offset.x, -offset.y)
        pygame.draw.rect(surface, (0, 255, 0), adjusted_boundary, 1)

        if self.divided:
            self.northeast.draw(surface, offset)
            self.northwest.draw(surface, offset)
            self.southeast.draw(surface, offset)
            self.southwest.draw(surface, offset)
