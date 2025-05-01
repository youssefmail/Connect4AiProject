import pygame
import asyncio
import platform

from game_logic import State, HumanPlayerByGUI, HumanPlayer, copyOfObject
from game_ai import AiPlayer

class HumanPlayerByGUI(HumanPlayer):
    def __init__(self, name="Player", gui=None):
        super().__init__(name)
        self.gui = gui  # Reference to the ConnectFourGUI object
        self.selected_action = None  # Store the action chosen via mouse click

    def get_player_action(self, copy_of_current_state):
        pass
        if self.gui is None:
            raise Exception("GUI not set for HumanPlayerByGUI")
        # Set the GUI's state and wait for a column click
        self.gui.set_state(copy_of_current_state)
        self.selected_action = None  # Reset action
        self.gui.set_waiting_for_action(True)  # Signal GUI to wait for human input
        # Wait until an action is selected
        while self.selected_action is None:
            if self.gui.handle_events():  # Process Pygame events
                self.gui.draw()  # Redraw the board
            pygame.time.Clock().tick(60)  # Control frame rate
        self.gui.set_waiting_for_action(False)
        return self.selected_action


class ConnectFourGUI:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 700, 700  # <-- Made height bigger to add space for text
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Connect Four")
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Colors
        self.BLUE = (25, 100, 200)
        self.LIGHT_BLUE = (100, 150, 255)  # <-- New light blue for hover effects
        self.BLACK = (0, 0, 0)
        self.RED = (220, 20, 60)
        self.YELLOW = (255, 215, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (160, 160, 160)
        self.DARK_GRAY = (50, 50, 50)

        # Menu buttons
        self.pvp_button = pygame.Rect(250, 250, 200, 60)
        self.pvai_button = pygame.Rect(250, 350, 200, 60)
        self.exit_button = pygame.Rect(250, 450, 200, 60)
        self.font = pygame.font.SysFont('arial', 40, bold=True)  # <-- Nicer font
        self.small_font = pygame.font.SysFont('arial', 30)

        # Game variables
        self.menu_active = True
        self.game_over = False
        self.state = None
        self.players = []
        self.current_player_index = 0
        self.waiting_for_action = False

    def set_state(self, state):
        self.state = state

    def set_waiting_for_action(self, waiting):
        self.waiting_for_action = waiting

    def draw_button(self, rect, text, hover=False):
        color = self.LIGHT_BLUE if hover else self.BLUE
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        pygame.draw.rect(self.screen, self.WHITE, rect, 3, border_radius=15)
        text_surface = self.small_font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_menu(self):
        self.screen.fill(self.DARK_GRAY)
        title = self.font.render("Connect Four", True, self.WHITE)
        title_rect = title.get_rect(center=(self.WIDTH//2, 150))
        self.screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        self.draw_button(self.pvp_button, "Player vs Player", self.pvp_button.collidepoint(mouse_pos))
        self.draw_button(self.pvai_button, "Player vs AI", self.pvai_button.collidepoint(mouse_pos))
        self.draw_button(self.exit_button, "Exit", self.exit_button.collidepoint(mouse_pos))

    def draw_board(self):
        if self.state is None:
            return
        board = self.state.get_board_as_list()
        self.screen.fill(self.BLUE)

        # Draw cells
        for row in range(6):
            for col in range(7):
                x = col * 100 + 50
                y = row * 100 + 150
                pygame.draw.circle(self.screen, self.BLACK, (x, y), 42)  # black background circle
                color = self.GRAY if board[row][col] == 0 else self.RED if board[row][col] == 1 else self.YELLOW
                pygame.draw.circle(self.screen, color, (x, y), 38)  # smaller colored circle

        # Draw turn indicator
        if not self.game_over and not self.state.is_terminate():
            turn_player = self.state.get_who_player_turn()
            turn_text = f"Player {turn_player}'s Turn ({self.players[self.current_player_index].name})"
            color = self.RED if turn_player == 1 else self.YELLOW
            text_surface = self.small_font.render(turn_text, True, color)
            self.screen.blit(text_surface, (self.WIDTH // 2 - text_surface.get_width() // 2, 50))

    def draw_game_over(self):
        winner = self.state.get_winner_player_number()
        if winner == 1:
            text = f"Player 1 ({self.players[0].name}) Wins!"
            color = self.RED
        elif winner == 2:
            text = f"Player 2 ({self.players[1].name}) Wins!"
            color = self.YELLOW
        else:
            text = "It's a Draw!"
            color = self.WHITE

        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.WIDTH//2, 100))
        self.screen.blit(text_surface, text_rect)

        restart_text = self.small_font.render("Click anywhere to return to menu", True, self.WHITE)
        restart_rect = restart_text.get_rect(center=(self.WIDTH//2, 150))
        self.screen.blit(restart_text, restart_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if self.menu_active:
                    if self.pvp_button.collidepoint(pos):
                        self.players = [HumanPlayerByGUI("Player 1", self), HumanPlayerByGUI("Player 2", self)]
                        self.state = State()
                        self.current_player_index = 0
                        self.menu_active = False
                        self.game_over = False
                    elif self.pvai_button.collidepoint(pos):
                        self.players = [HumanPlayerByGUI("You", self), AiPlayer(name="AI", level=4)]
                        self.state = State()
                        self.current_player_index = 0
                        self.menu_active = False
                        self.game_over = False
                    elif self.exit_button.collidepoint(pos):
                        return False
                elif self.waiting_for_action:
                    col = pos[0] // 100
                    if 0 <= col < 7 and self.state.is_available_action(col):
                        if isinstance(self.players[self.current_player_index], HumanPlayerByGUI):
                            self.players[self.current_player_index].selected_action = col
                            self.waiting_for_action = False
                elif self.game_over:
                    self.menu_active = True
                    self.state = None
                    self.players = []
                    self.current_player_index = 0
                    self.waiting_for_action = False
        return True

    def draw(self):
        if self.menu_active:
            self.draw_menu()
        else:
            self.draw_board()
            if self.game_over:
                self.draw_game_over()
        pygame.display.flip()

    async def play_turn(self):
        if self.state is None or self.menu_active:
            return
        if self.state.is_terminate():
            self.game_over = True
            return
        player = self.players[self.current_player_index]
        try:
            action = player.get_player_action(copyOfObject(self.state))
            if action is not None and self.state.is_available_action(action):
                self.state.take_action(action)
            else:
                self.game_over = True
                return
        except Exception as e:
            print(f"Error during player action: {e}")
            self.game_over = True
            return
        self.current_player_index = 1 - self.current_player_index

    async def main_loop(self):
        while True:
            if not self.handle_events():
                break
            if not self.menu_active and not self.game_over:
                await self.play_turn()
            self.draw()
            await asyncio.sleep(1.0 / self.FPS)
        pygame.quit()

def start_gui():
    gui = ConnectFourGUI()
    asyncio.run(gui.main_loop())


if platform.system() == "Emscripten":
    asyncio.ensure_future(ConnectFourGUI().main_loop())
else:
    if __name__ == "__main__":
        asyncio.run(ConnectFourGUI().main_loop())
