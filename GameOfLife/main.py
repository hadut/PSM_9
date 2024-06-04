import pygame
import numpy as np
import sys

'''
Ten program przedstawia symulację słynnego automatu komórkowego "Gra w życie". Polega on na ty, że są komórki, które
mają określoną wartość 1 (żyje) albo 0 (nie żyje). Regóły gry są proste, w zależności od pewnej ilości 'żywych' sąsiadów
komórka zmienia swój stan z 1 na 0, bądź z 0 na 1.  
'''


class GameOfLife:
    def __init__(self, x, y, showcase):
        # Przypisujemy parametry x (określający szerokość planszy) i y (określający wysokość planszy)
        self.x = x
        self.y = y

        # Tworzymy dwie macierze, o szerokości x i wysokości y, do przechowywania wartości komórek, jedna ma stan
        # obecny, a druga po jednym kroku
        self.current = np.zeros(shape=(y, x))
        self.next = np.zeros(shape=(y, x))

        # Przykładowy scenariusz, przygotowany do prezentacji
        self.showcase = showcase
        if self.showcase:
            self.current[15][11] = 1
            self.current[15][12] = 1
            self.current[16][11] = 1
            self.current[16][12] = 1

            self.current[15][21] = 1
            self.current[16][21] = 1
            self.current[17][21] = 1
            self.current[14][22] = 1
            self.current[18][22] = 1
            self.current[13][23] = 1
            self.current[13][24] = 1
            self.current[19][23] = 1
            self.current[19][24] = 1
            self.current[16][25] = 1
            self.current[14][26] = 1
            self.current[18][26] = 1
            self.current[15][27] = 1
            self.current[16][27] = 1
            self.current[17][27] = 1
            self.current[16][28] = 1

            self.current[15][31] = 1
            self.current[15][32] = 1
            self.current[14][31] = 1
            self.current[14][32] = 1
            self.current[13][31] = 1
            self.current[13][32] = 1
            self.current[12][33] = 1
            self.current[16][33] = 1
            self.current[12][35] = 1
            self.current[11][35] = 1
            self.current[16][35] = 1
            self.current[17][35] = 1

            self.current[13][45] = 1
            self.current[13][46] = 1
            self.current[14][45] = 1
            self.current[14][46] = 1

        # Tworzymy macierz o wysokości 2 i szerokości 9 do przechowywania zasad zmiany wartości komórki
        self.rules = np.zeros(shape=(2, 9))

        # Ustawiamy domyślne wartości zasad
        self.rules[0][3] = 1
        self.rules[1][3] = 1
        self.rules[1][2] = 1

        # Ustawiamy częstotliwość z jaką będzie updatowany obraz
        self.fps = 30

        # Tworzymy zmienną do pilnowania, czy symulacja wystartowała, albo czy jest zatrzymana
        self.started = False

    # Metoda run uruchamia aplikację
    def run(self):
        # Uruchamiamy aplikację pygame
        pygame.init()

        # Ustawiamy tytuł okna "Game of Life"
        pygame.display.set_caption("Game of Life")

        # Ustawiamy wielkość komórki
        if self.showcase:
            cellSize = 10
        else:
            cellSize = 50

        # Ustawiamy odpowiednią wielkość aplikacji, tak aby zmieściła wszystkie komórki i bardzo proste menu
        width = self.x * cellSize
        height = (self.y + 2) * cellSize
        window = pygame.display.set_mode((width, height))

        # Wywołujemy metodę view
        self.view(window, cellSize, width, height)

    # Metoda view
    def view(self, window, cellSize, width, height):
        # Wypełniamy tło kolorem (255, 255, 255), czyli białym
        window.fill((255, 255, 255))

        # Rysujemy prostokąt przedstawiający przycisk "Start"
        pygame.draw.rect(window, (150, 150, 150),
                         (5, height - cellSize * 2 + 5, cellSize * 5 - 10, cellSize * 2 - 10))
        # Ustawiamy czcionkę
        font = pygame.font.SysFont('Corbel', 35)
        # Dodajemy tekst do "przycisku"
        startText = font.render('Start', True, (0, 0, 0))
        window.blit(startText, (cellSize + 15, height - cellSize + 5 - 35 / 2))

        # Rysujemy prostokąt przedstawiający przycisk "Stop"
        pygame.draw.rect(window, (150, 150, 150),
                         (cellSize * 5, height - cellSize * 2 + 5, cellSize * 5 - 10, cellSize * 2 - 10))
        # Dodajemy tekst do "przycisku"
        stopText = font.render('Stop', True, (0, 0, 0))
        window.blit(stopText, (cellSize * 6 + 20, height - cellSize + 5 - 35 / 2))

        # Rysujemy prostokąty przedstawiające menu do zmiany zasad
        pygame.draw.rect(window, (150, 150, 150),
                         (width - 555, height - cellSize * 2 + 5, cellSize * 10, (cellSize * 2 - 10) / 3))
        pygame.draw.rect(window, (255, 0, 0), (width - 555, height - cellSize * 2 + 5 +
                                               (cellSize * 2 - 10) / 3, cellSize, (cellSize * 2 - 10) / 3))
        pygame.draw.rect(window, (50, 205, 50), (width - 555, height - cellSize * 2 + 5 +
                                                 (cellSize * 2 - 10) / 3 * 2, cellSize, (cellSize * 2 - 10) / 3))
        # Ustawiamy nową czcionkę
        font2 = pygame.font.SysFont('Corbel', 24)
        # Dla każdej liczby sąsiadów dodajemy tekst
        for i in range(len(self.rules[0])):
            text = font2.render(str(i), True, (0, 0, 0))
            window.blit(text,
                        (width - 540 + (i + 1) * cellSize, height - cellSize * 2 + ((cellSize * 2 - 10) / 3 - 24)))
        # Dodajemy tekst tytułowy do tabelki zasad
        stateText = font2.render('State', True, (0, 0, 0))
        window.blit(stateText, (width - 550, height - cellSize * 2 + ((cellSize * 2 - 10) / 3 - 20)))
        # Dodajemy tekst do obu stanów
        deadText = font2.render(str(0), True, (0, 0, 0))
        window.blit(deadText, (width - 535, height - cellSize * 2 + (cellSize * 2 - 10) / 3 * 2 - 20))
        liveText = font2.render(str(1), True, (0, 0, 0))
        window.blit(liveText, (width - 535, height - 30))
        # Dla każdego stanu dodajemy tekst i kolor tła określający zasadę w danym przypadku
        for state in range(len(self.rules)):
            for neighbours in range(len(self.rules[0])):
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

        # Dla każdej komórki zmieniamy kolor na czarny, jeżeli komórka jest "żywa"
        for i in range(2, self.y):
            for j in range(self.x):
                if self.current[i][j] == 1:
                    pygame.draw.rect(window, color=(0, 0, 0), rect=(j * cellSize, i * cellSize, cellSize, cellSize))
                else:
                    pygame.draw.rect(window, color=(255, 255, 255),
                                     rect=(j * cellSize, i * cellSize, cellSize, cellSize))

        # Rysujemy linie rozdzielające komórki na planszy
        for i in range(cellSize, width, cellSize):
            pygame.draw.line(window, color=(150, 150, 150), start_pos=(i, 0),
                             end_pos=(i, height - 2 * cellSize))
        for i in range(cellSize, height - cellSize, cellSize):
            pygame.draw.line(window, color=(150, 150, 150), start_pos=(0, i), end_pos=(width, i))

        # Główna pętla programu
        while True:
            # Pobieramy lokalizację myszki
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                # Jeżeli zamknięto aplikację, kończymy program
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Jeśli wciśnięto klawisz
                elif event.type == pygame.KEYDOWN:
                    # Jeżeli wciśnięto przycisk ESC, kończymy program
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    # Jeśli wciśnięto przycisk Space zmieniamy stan symulacji
                    if event.key == pygame.K_SPACE:
                        if not self.started:
                            self.started = True
                        else:
                            self.started = False
                # Jeśli wciśnięto przycisk myszy
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Jeśli lokalizacja myszy jest na przycisku "Start" i symulacja jest zatrzymana, uruchamiamy
                    # symulację
                    if (not self.started and 5 < pos[0] < cellSize * 5 - 10 + 5 and
                            cellSize * self.y < pos[1] < height - 5):
                        self.started = True
                    # Jeśli lokalizacja myszy jest na przycisku "Stop" i symulacja działa, zatrzymujemy symulację
                    if (self.started and cellSize * 5 < pos[0] < cellSize * 5 - 10 + cellSize * 5 and
                            cellSize * self.y < pos[1] < height - 5):
                        self.started = False
                    # Jeśli symulacja jest zatrzymana i lokalizacja myszy jest na jednym z przycisków w tabeli zasad,
                    # to zmieniamy odpowiednią zasadę na przeciwną (z 0 na 1, albo z 1 na 0)
                    if (not self.started and width - 505 < pos[0] < width - 555 + cellSize * 10 and
                            height - cellSize * 2 + 5 + (cellSize * 2 - 10) / 3 < pos[1] < height - 5):
                        # Bierzemy lokalizację w tabeli, w zależności od rozmiaru komórek i od lokalizacji w aplikacji
                        column = (pos[0] - (width - 550)) // cellSize - 1
                        row = int((pos[1] - (height - cellSize * 2 + 5 + (cellSize * 2 - 10) / 3)) //
                                  ((cellSize * 2 - 10) / 3))
                        # Zmieniamy wartość w macierzy zasad
                        self.rules[row][column] = 1 - self.rules[row][column]
                        # Zmieniamy kolor przycisków
                        if self.rules[row][column] == 0:
                            color = (255, 0, 0)
                        else:
                            color = (50, 205, 50)
                        pygame.draw.rect(window, color, (width - 505 + column * cellSize,
                                                         height - cellSize * 2 + 5 + ((cellSize * 2 - 10) / 3) * (
                                                                 row + 1), cellSize, (cellSize * 2 - 10) / 3))
                        # Zmieniamy tekst przycisków
                        text = font2.render(str(int(self.rules[row][column])), True, (0, 0, 0))
                        window.blit(text, (width - 540 + (column + 1) * cellSize,
                                           height - cellSize * 2 + ((cellSize * 2 - 10) / 3 - 24) + (
                                                   cellSize * 2 - 10) / 3 * (
                                                   row + 1)))
                    # Jeśli symulacja nie trwa i lokalizacja myszy jest na jednej z komórek, to zmieniamy jej wartość
                    if not self.started and pos[1] < cellSize * self.y:
                        # Przeliczamy lokalizację na miejsce w macierzy
                        column = pos[0] // cellSize
                        row = pos[1] // cellSize
                        # Zmieniamy wartość
                        self.current[row][column] = 1 - self.current[row][column]
                        # Zmieniamy kolor w zależności od nowej wartości
                        if self.current[row][column] == 1:
                            pygame.draw.rect(window, color=(0, 0, 0),
                                             rect=(column * cellSize, row * cellSize, cellSize, cellSize))
                        else:
                            pygame.draw.rect(window, color=(255, 255, 255),
                                             rect=(column * cellSize, row * cellSize, cellSize, cellSize))

            # Jeśli symulacja trwa, to uruchamiamy obliczenia, zmieniamy aktualną macierz oraz czyścimy macierz następną
            if self.started:
                self.calulate(window, cellSize)
                self.current = self.next
                self.next = np.zeros(shape=(self.y, self.x))

            # Aktualizujemy linie planszy
            for i in range(cellSize, width, cellSize):
                pygame.draw.line(window, color=(150, 150, 150), start_pos=(i, 0),
                                 end_pos=(i, height - 2 * cellSize))
            for i in range(cellSize, height - cellSize, cellSize):
                pygame.draw.line(window, color=(150, 150, 150), start_pos=(0, i), end_pos=(width, i))

            # Odświerzamy widok planszy
            pygame.display.flip()
            pygame.time.Clock().tick(self.fps)

    # Wylicza jeden krok symulacji
    def calulate(self, window, cellSize):
        for i in range(self.y):
            for j in range(self.x):
                # Zliczamy ile dana komórka ma "żywych" sąsiadów
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
                # Zmieniamy wartość w danej komórce w zależności od zasad
                self.next[i][j] = self.rules[int(self.current[i][j])][int(aliveNeighbours)]
                # Aktualizujemy kolory komórek
                if self.current[i][j] == 1:
                    pygame.draw.rect(window, color=(0, 0, 0), rect=(j * cellSize, i * cellSize, cellSize, cellSize))
                else:
                    pygame.draw.rect(window, color=(255, 255, 255),
                                     rect=(j * cellSize, i * cellSize, cellSize, cellSize))


# Jeśli program uruchomiony jako main, to uruchom aplikację symulacji
if __name__ == "__main__":
    showcase = False
    if showcase:
        game = GameOfLife(150, 75, showcase)
    else:
        game = GameOfLife(30, 13, showcase)
    game.run()
