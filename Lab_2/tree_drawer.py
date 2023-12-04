import pygame
import math


class TreeDrawer:
    def __init__(self, tree, surface, font) -> None:
        self.tree = tree
        self.surface = surface
        self.font = font
        self.d = 80
        self.radius = 30
        self.node_x = 1280 - 300
        self.child_x = [self.node_x - (3 - i) * self.d for i in range(7)]
        self.node_y = 200
        self.parent_y = self.node_y - 100
        self.child_y = self.node_y + 100

    def draw(self, index, maximiser):
        self.__draw_node(self.node_x, self.node_y, maximiser, self.tree[index])
        if index != 0:
            self.__draw_node(
                self.node_x, self.parent_y, not maximiser, self.tree[(index - 1) // 7]
            )
            pygame.draw.line(
                self.surface,
                (255, 255, 255),
                (self.node_x, self.node_y - self.radius),
                (self.node_x, self.parent_y + self.radius),
            )

        for child in range(7):
            if index * 7 + 1 + child >= len(self.tree):
                break
            child_x = self.child_x[child]
            self.__draw_node(
                child_x, self.child_y, not maximiser, self.tree[index * 7 + 1 + child]
            )
            hyp = math.dist((self.node_x, self.node_y), (child_x, self.child_y))
            dx = child_x - self.node_x
            dy = 100
            cos_angle = dx / hyp
            sin_angle = dy / hyp
            pygame.draw.line(
                self.surface,
                (255, 255, 255),
                (
                    self.node_x + cos_angle * self.radius,
                    self.node_y + sin_angle * self.radius,
                ),
                (child_x, self.child_y - self.radius),
            )

    def __draw_node(self, x, y, maximiser, value) -> None:
        if value == None:
            return

        if maximiser:
            pygame.draw.circle(self.surface, (255, 255, 0), (x, y), self.radius)
        else:
            pygame.draw.circle(self.surface, (255, 0, 0), (x, y), self.radius)

        if value < 0:
            render_string = "-" + str(-value)
        else:
            render_string = str(value)
        text = self.font.render(render_string, False, (255, 255, 255))
        self.surface.blit(text, text.get_rect(center=(x, y)))

    def circle_intersects(self, mouse_x, mouse_y, x, y):
        return (mouse_x - x) * (mouse_x - x) + (mouse_y - y) * (
            mouse_y - y
        ) <= self.radius * self.radius
