import pygame
import numpy as np
import sys


class GameOfLife:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current = np.zeros(shape=(y, x))
        self.next = np.zeros(shape=(y, x))
        self.rules = np.zeros(shape=(2, 9))
        self.rules[0][3] = 1
        self.rules[1][3] = 1
        self.rules[1][2] = 1
        self.fps = 5
        self.started = False

    def setRules(self):
        pass

    def run(self):
        pygame.init()
        pygame.display.set_caption("Game of Life")
        cellSize = 50
        width = self.x * cellSize
        height = (self.y + 2) * cellSize
        window = pygame.display.set_mode((width, height))
        self.view(window, cellSize, width, height)

    def view(self, window, cellSize, width, height):
        window.fill((255, 255, 255))
        pygame.draw.rect(window, (150, 150, 150),
                         (5, height - cellSize * 2 + 5, cellSize * 5 - 10, cellSize * 2 - 10))
        font = pygame.font.SysFont('Corbel', 35)
        startText = font.render('Start', True, (0, 0, 0))
        window.blit(startText, (cellSize + 15, height - cellSize + 5 - 35 / 2))
        pygame.draw.rect(window, (150, 150, 150),
                         (cellSize * 5, height - cellSize * 2 + 5, cellSize * 5 - 10, cellSize * 2 - 10))
        stopText = font.render('Stop', True, (0, 0, 0))
        window.blit(stopText, (cellSize * 6 + 20, height - cellSize + 5 - 35 / 2))
        pygame.draw.rect(window, (150, 150, 150),
                         (width - 555, height - cellSize * 2 + 5, cellSize * 10, (cellSize * 2 - 10) / 3))
        pygame.draw.rect(window, (255, 0, 0), (width - 555, height - cellSize * 2 + 5 +
                                               (cellSize * 2 - 10) / 3, cellSize, (cellSize * 2 - 10) / 3))
        pygame.draw.rect(window, (50, 205, 50), (width - 555, height - cellSize * 2 + 5 +
                                                 (cellSize * 2 - 10) / 3 * 2, cellSize, (cellSize * 2 - 10) / 3))
        font2 = pygame.font.SysFont('Corbel', 24)
        for i in range(len(self.rules[0])):
            text = font2.render(str(i), True, (0, 0, 0))
            window.blit(text,
                        (width - 540 + (i + 1) * cellSize, height - cellSize * 2 + ((cellSize * 2 - 10) / 3 - 24)))
        stateText = font2.render('State', True, (0, 0, 0))
        window.blit(stateText, (width - 550, height - cellSize * 2 + ((cellSize * 2 - 10) / 3 - 20)))
        deadText = font2.render(str(0), True, (0, 0, 0))
        window.blit(deadText, (width - 535, height - cellSize * 2 + (cellSize * 2 - 10) / 3 * 2 - 20))
        liveText = font2.render(str(1), True, (0, 0, 0))
        window.blit(liveText, (width - 535, height - 30))
        for state in range(len(self.rules)):
            for neighbours in range(len(self.rules[0])):
                color = (0, 0, 0)
                if self.rules[state][neighbours] == 0:
                    color = (255, 0, 0)
                else:
                    color = (50, 205, 50)
                pygame.draw.rect(window, color, ((width - 555 + (neighbours + 1) * cellSize),
                                                 height - cellSize * 2 + 5 + (cellSize * 2 - 10) / 3 * (state + 1),
                                                 cellSize, (cellSize * 2 - 10) / 3))
                text = font2.render(str(int(self.rules[state][neighbours])), True, (0, 0, 0))
                window.blit(text, (width - 540 + (neighbours + 1) * cellSize,
                                   height - cellSize * 2 + ((cellSize * 2 - 10) / 3 - 24) + (cellSize * 2 - 10) / 3 * (
                                               state + 1)))
        for i in range(2, self.y):
            for j in range(self.x):
                if self.current[i][j] == 1:
                    pygame.draw.rect(window, color=(0, 0, 0), rect=(j * cellSize, i * cellSize, cellSize, cellSize))
                else:
                    pygame.draw.rect(window, color=(255, 255, 255),
                                     rect=(j * cellSize, i * cellSize, cellSize, cellSize))
        for state in range(cellSize, width, cellSize):
            pygame.draw.line(window, color=(150, 150, 150), start_pos=(state, 0),
                             end_pos=(state, height - 2 * cellSize))
        for state in range(cellSize, height - cellSize, cellSize):
            pygame.draw.line(window, color=(150, 150, 150), start_pos=(0, state), end_pos=(width, state))
        while True:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (not self.started and 5 < pos[0] < cellSize * 5 - 10 + 5 and
                            cellSize * self.y < pos[1] < height - 5):
                        self.started = True
                    if (self.started and cellSize * 5 < pos[0] < cellSize * 5 - 10 + cellSize * 5 and
                            cellSize * self.y < pos[1] < height - 5):
                        self.started = False
                    if (not self.started and width - 505 < pos[0] < width - 555 + cellSize * 10 and
                            height - cellSize * 2 + 5 + (cellSize * 2 - 10) / 3 < pos[1] < height - 5):
                        column = (pos[0] - (width - 550)) // cellSize - 1
                        row = int((pos[1] - (height - cellSize * 2 + 5 + (cellSize * 2 - 10) / 3)) //
                                  ((cellSize * 2 - 10) / 3))
                        self.rules[row][column] = 1 - self.rules[row][column]
                        color = (0, 0, 0)
                        if self.rules[row][column] == 0:
                            color = (255, 0, 0)
                        else:
                            color = (50, 205, 50)
                        pygame.draw.rect(window, color, (width - 505 + column * cellSize,
                                                         height - cellSize * 2 + 5 + ((cellSize * 2 - 10) / 3) * (
                                                                 row + 1), cellSize, (cellSize * 2 - 10) / 3))
                        text = font2.render(str(int(self.rules[row][column])), True, (0, 0, 0))
                        window.blit(text, (width - 540 + (column + 1) * cellSize,
                                           height - cellSize * 2 + ((cellSize * 2 - 10) / 3 - 24) + (
                                                       cellSize * 2 - 10) / 3 * (
                                                   row + 1)))
                    if not self.started and pos[1] < cellSize * self.y:
                        column = pos[0] // cellSize
                        row = pos[1] // cellSize
                        self.current[row][column] = 1 - self.current[row][column]
                        if self.current[row][column] == 1:
                            pygame.draw.rect(window, color=(0, 0, 0),
                                             rect=(column * cellSize, row * cellSize, cellSize, cellSize))
                        else:
                            pygame.draw.rect(window, color=(255, 255, 255),
                                             rect=(column * cellSize, row * cellSize, cellSize, cellSize))
            if self.started:
                self.calulate(window, cellSize)
                self.current = self.next
                self.next = np.zeros(shape=(self.y, self.x))
            for state in range(cellSize, width, cellSize):
                pygame.draw.line(window, color=(150, 150, 150), start_pos=(state, 0),
                                 end_pos=(state, height - 2 * cellSize))
            for state in range(cellSize, height - cellSize, cellSize):
                pygame.draw.line(window, color=(150, 150, 150), start_pos=(0, state), end_pos=(width, state))
            pygame.display.flip()
            pygame.time.Clock().tick(self.fps)

    def calulate(self, window, cellSize):
        for i in range(self.y):
            for j in range(self.x):
                aliveNeighbours = 0
                if i - 1 < 0:
                    if j - 1 < 0:
                        aliveNeighbours += self.current[self.y + i - 1][self.x + j - 1]
                    else:
                        aliveNeighbours += self.current[self.y + i - 1][j - 1]
                    if j + 1 == self.x:
                        aliveNeighbours += self.current[self.y + i - 1][j + 1 - self.x]
                    else:
                        aliveNeighbours += self.current[self.y + i - 1][j + 1]
                    aliveNeighbours += self.current[self.y + i - 1][j]
                else:
                    if j - 1 < 0:
                        aliveNeighbours += self.current[i - 1][self.x + j - 1]
                    else:
                        aliveNeighbours += self.current[i - 1][j - 1]
                    if j + 1 == self.x:
                        aliveNeighbours += self.current[i - 1][j + 1 - self.x]
                    else:
                        aliveNeighbours += self.current[i - 1][j + 1]
                    aliveNeighbours += self.current[i - 1][j]
                if i + 1 == self.y:
                    if j - 1 < 0:
                        aliveNeighbours += self.current[i + 1 - self.y][self.x + j - 1]
                    else:
                        aliveNeighbours += self.current[i + 1 - self.y][j - 1]
                    if j + 1 == self.x:
                        aliveNeighbours += self.current[i + 1 - self.y][j + 1 - self.x]
                    else:
                        aliveNeighbours += self.current[i + 1 - self.y][j + 1]
                    aliveNeighbours += self.current[i + 1 - self.y][j]
                else:
                    if j - 1 < 0:
                        aliveNeighbours += self.current[i + 1][self.x + j - 1]
                    else:
                        aliveNeighbours += self.current[i + 1][j - 1]
                    if j + 1 == self.x:
                        aliveNeighbours += self.current[i + 1][j + 1 - self.x]
                    else:
                        aliveNeighbours += self.current[i + 1][j + 1]
                    aliveNeighbours += self.current[i + 1][j]
                if j + 1 == self.x:
                    aliveNeighbours += self.current[i][j + 1 - self.x]
                else:
                    aliveNeighbours += self.current[i][j + 1]
                if j - 1 < 0:
                    aliveNeighbours += self.current[i][self.x + j - 1]
                else:
                    aliveNeighbours += self.current[i][j - 1]
                self.next[i][j] = self.rules[int(self.current[i][j])][int(aliveNeighbours)]
                if self.current[i][j] == 1:
                    pygame.draw.rect(window, color=(0, 0, 0), rect=(j * cellSize, i * cellSize, cellSize, cellSize))
                else:
                    pygame.draw.rect(window, color=(255, 255, 255),
                                     rect=(j * cellSize, i * cellSize, cellSize, cellSize))


if __name__ == "__main__":
    gameOfLife = GameOfLife(30, 13)
    gameOfLife.run()
