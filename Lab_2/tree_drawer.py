import pygame
import math

class TreeDrawer:
    def __init__(self, tree) -> None:
        pygame.init()
        self.tree = tree
        self.surface = pygame.display.set_mode((1280, 720))
        self.font = pygame.font.Font("regular_font.otf", 20)
        self.d = 100
        self.radius = 40
        self.node_x = 1280 // 2
        self.child_x = [self.node_x - (3 - i) * self.d for i in range(7)]
        self.node_y = 200
        self.parent_y = self.node_y - 100
        self.child_y = self.node_y + 100

    def draw(self, index, maximiser):
        self.surface.fill((24, 24, 24))
        self.__draw_node(self.node_x, self.node_y, maximiser, tree[index])
        if index != 0:
            self.__draw_node(self.node_x, self.parent_y, not maximiser, tree[(index - 1) // 7])
            pygame.draw.line(self.surface, (255, 255, 255), (self.node_x, self.node_y - self.radius), (self.node_x, self.parent_y + self.radius))

        for child in range(7):
            if index * 7 + 1 + child >= len(tree):
                break
            child_x = self.child_x[child]
            self.__draw_node(child_x, self.child_y, not maximiser, tree[index * 7 + 1 + child])
            hyp = math.dist((self.node_x, self.node_y), (child_x, self.child_y))
            dx = child_x - self.node_x
            dy = 100
            cos_angle = dx / hyp
            sin_angle = dy / hyp
            pygame.draw.line(self.surface, (255, 255, 255), (self.node_x + cos_angle * self.radius, self.node_y + sin_angle * self.radius), (child_x, self.child_y - self.radius))
        pygame.display.update()

    def __draw_node(self, x, y, maximiser, value) -> None:
        if maximiser:
            pygame.draw.circle(self.surface, (255, 0, 0), (x, y), self.radius)
        else:
            pygame.draw.circle(self.surface, (0, 255, 0), (x, y), self.radius)
        text = self.font.render(str(value), False, (255, 255, 255))
        self.surface.blit(text, text.get_rect(center=(x, y)))
    
    def circle_intersects(self, mouse_x, mouse_y, x, y):
        return (mouse_x - x) * (mouse_x - x) + (mouse_y - y) * (mouse_y - y) <= self.radius * self.radius


tree = [10, 20, 30, 40, 50, 60, 70, 80, 90]
d = TreeDrawer(tree)
index = 0
maximising = True

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            if d.circle_intersects(mouse_x, mouse_y, d.node_x, d.parent_y) and index != 0:
                index = (index - 1) // 7
                maximising = not maximising
            
            for child in range(7):
                if d.circle_intersects(mouse_x, mouse_y, d.child_x[child], d.child_y) and index * 7 + 1 + child <= len(tree):
                    index = index * 7 + 1 + child
                    maximising = not maximising
                    break

    d.draw(index, maximising)

