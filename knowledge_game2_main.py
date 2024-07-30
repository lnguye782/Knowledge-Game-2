import pygame
import sys
import knowledge_game2_module

pygame.init()

# Define some basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define font for rendering text
font = pygame.font.Font(None, 32)

# Set up main game window
window_size = (600, 720)
main_screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Knowledge Game 2")

# Define the grid table
grid_table_size = 5
cell_size = window_size[0] // grid_table_size
grid_score_table = [
    [2, 1, 1, 1, 2],
    [1, 2, 1, 2, 1],
    [1, 1, 5, 1, 1],
    [1, 2, 1, 2, 1],
    [2, 1, 1, 1, 2],
]

# Read and store questions from .csv
get_question_bank = knowledge_game2_module.read_csv("all_subject_question_bank.csv")

# Assign random questions to cells
get_question_cell, get_answer_cell = knowledge_game2_module.assign_random_question_to_cells(grid_table_size, grid_score_table, get_question_bank)

# Get team names
team_names = knowledge_game2_module.get_team_names()

# Initialize game state
cell_selected = None
cell_answered = {}
current_player = 1
current_player_score = {1: 0, 2: 0}

# Game Loop
running_main_screen = True
while running_main_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_main_screen = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Find x and y coordinates of the mouse
            mouse_col = mouse_x // cell_size
            mouse_row = (mouse_y-120) // cell_size
            # Test mouse and cell coordinates
            # print(f"Mouse clicked at: ({mouse_x}, {mouse_y}) -> Cell: ({mouse_row}, {mouse_col})")
            
            cell_selected = (mouse_row, mouse_col)
            if cell_selected in get_question_cell and cell_selected not in cell_answered:
                current_question = get_question_cell[cell_selected]
                current_answer = get_answer_cell[cell_selected]
                current_question_score = grid_score_table[mouse_row][mouse_col]
                knowledge_game2_module.show_question_screen(current_player, current_player_score, current_question, current_answer, current_question_score, cell_selected, cell_answered)
                
                # Check if the cell was answered during the question screen
                if cell_selected in cell_answered:
                    # Store the player who answered correcly
                    cell_answered[cell_selected] = current_player
                
                # Switch player turn
                current_player = 2 if current_player == 1 else 1

            # Check if one of the players reaches 15 points
            if knowledge_game2_module.check_win_condition(current_player_score):
                knowledge_game2_module.show_winning_screen(3 - current_player, current_player_score, team_names)
                running_main_screen = False

    # Fill background of the main screen with WHITE
    main_screen.fill(WHITE)

    # Draw grid table of the game
    for row in range(grid_table_size):
        for col in range(grid_table_size):
            rect_cell = pygame.Rect((col * cell_size), (row * cell_size) + 120, cell_size, cell_size)
            # Draw the rectangle cells with BLACK and border width of 2
            pygame.draw.rect(main_screen, BLACK, rect_cell, 1)
            # Draw the border line on top
            pygame.draw.line(main_screen, BLACK, (0, 120), (window_size[0], 120), 2)

            # Display the score in the cells
            text_score = font.render(str(grid_score_table[row][col]), True, BLACK)
            text_rect = text_score.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2 + 120))
            main_screen.blit(text_score, text_rect)

            # Draw Red box for Player 1 and Blue box for Player 2
            if (row, col) in cell_answered:
                # Update the rectangle cell
                answered_rect_cell = pygame.Rect((col * cell_size) + 25, (row * cell_size) + 145, cell_size - 50, cell_size - 50)
                answered_text_score = font.render(str(grid_score_table[row][col]), True, WHITE)
               
                # Display the box in the cells
                player_who_answered = cell_answered[(row, col)]
                if player_who_answered == 1:
                    pygame.draw.rect(main_screen, RED, answered_rect_cell)
                    main_screen.blit(answered_text_score, text_rect)
                elif player_who_answered == 2:
                    pygame.draw.rect(main_screen, BLUE, answered_rect_cell)
                    main_screen.blit(answered_text_score, text_rect)

    # Show both player scores
    text_player1_score = font.render("{}: {} points".format(team_names[1], current_player_score[1]), True, RED)
    text_player2_score = font.render("{}: {} points".format(team_names[2], current_player_score[2]), True, BLUE)
    text_player1_score_rect = text_player1_score.get_rect(topleft=(20, 30))
    text_player2_score_rect = text_player2_score.get_rect(topleft=(20, 60))
    main_screen.blit(text_player1_score, text_player1_score_rect)
    main_screen.blit(text_player2_score, text_player2_score_rect)

    # Show player turn
    text_player_turn = font.render("{}'s Turn".format(team_names[current_player]), True, BLACK)
    text_player_turn_rect = text_player_turn.get_rect(center=(500, 100))
    main_screen.blit(text_player_turn, text_player_turn_rect)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()