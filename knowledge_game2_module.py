import pygame
import sys
import csv
import random

# Define some basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def get_team_names():
    # Define font for rendering text
    font = pygame.font.Font(None, 45)

    # Set up team name input screen window
    window_size = (600, 720)
    team_name_screen = pygame.display.set_mode(window_size)  

    # Initialize name state
    running_name_screen = True
    team_names = {1: "", 2: ""}
    current_player = 1
    temp_text = ''
    input_box = pygame.Rect(200, 300, 400, 50)
    active = False
    color_active = pygame.Color('dodgerblue2')
    color_inactive = pygame.Color('lightskyblue3')
    color_current = color_inactive

    while running_name_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on the input box
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                # Change current color of the input box
                color_current = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        team_names[current_player] = temp_text
                        temp_text = ''
                        current_player += 1
                        if current_player > 2:
                            running_name_screen = False
                    elif event.key == pygame.K_BACKSPACE:
                        temp_text = temp_text[:-1]
                    else:
                        temp_text += event.unicode
        
        # Fill background of the name screen with WHITE
        team_name_screen.fill(WHITE)

        user_input_text = font.render(temp_text, True, color_current)
        input_box.w = max(200, user_input_text.get_width() + 10) # Resize the box if the text is too long
        pygame.draw.rect(team_name_screen, color_current, input_box, 2)
        team_name_screen.blit(user_input_text, (input_box.x + 5, input_box.y + 10))

        instruction_text = font.render("Enter Team {} Name:".format(current_player), True, BLACK)
        instruction_text_rect = instruction_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 100))
        team_name_screen.blit(instruction_text, instruction_text_rect)

        pygame.display.flip()

    return team_names

def read_csv(file_name):
    # Initialize dictionary
    question_dict = {
        1: [], 
        2: [], 
        5: []
    }
    with open(file_name, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        # Skip header
        next(csv_reader)
        for row in csv_reader:
            question_score_value = int(row[0])
            question_to_read = row[1]
            answer_to_read = row[2]
            question_dict[question_score_value].append((question_to_read, answer_to_read))

    return question_dict

def assign_random_question_to_cells(grid_size, grid_table, question_bank):  
    # Initialize dictionary
    question_cell = {}
    answer_cell = {}

    for row in range(grid_size):
        for col in range(grid_size):
            # Read the score value of the current cell
            read_score = grid_table[row][col]
            # Store questions and answers, from question bank based on read_score, as a list
            available_questions = [q for q in question_bank[read_score] if q not in question_cell.values()]
            # Assign one random question to the current cell
            if available_questions:
                selected_question = random.choice(available_questions)
                question_cell[(row, col)] = selected_question[0]
                answer_cell[(row, col)] = selected_question[1]
                # Remove the selected questions from question bank
                question_bank[read_score].remove(selected_question)

    return question_cell, answer_cell

def show_question_screen(current_player, current_player_score, current_question, current_answer, current_question_score, cell_selected, cell_answered):
    # Define font for rendering text
    font = pygame.font.Font(None, 35)

    # Set up question screen window
    window_size = (600, 720)
    question_screen = pygame.display.set_mode(window_size)
    
    # Initialize game state
    running_question_screen = True
    timer_start = pygame.time.get_ticks()

    # Question with 5-point gets 90 seconds, 2-point gets 45 seconds, 1-point gets 30 seconds
    if current_question_score == 5:
        timer_limit = 90000 + 1000 # 90 seconds timer
    elif current_question_score == 2:
        timer_limit = 45000 + 1000 # 45 seconds timer
    else:
        timer_limit = 30000 + 1000 # 30 seconds timer

    while running_question_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_question_screen = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Update player's score if they answer correct
                if rect_correct_button.collidepoint(mouse_x, mouse_y):
                    current_player_score[current_player] += current_question_score
                    cell_answered[cell_selected] = True
                    # Show the answer for 2 seconds then close question screen
                    reveal_answer_text = font.render(current_answer, True, BLACK)
                    reveal_answer_text_rect = reveal_answer_text.get_rect(center=(window_size[0] // 2, window_size[1] - 250))
                    question_screen.blit(reveal_answer_text, reveal_answer_text_rect)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    running_question_screen = False
                elif rect_incorrect_button.collidepoint(mouse_x, mouse_y):
                    running_question_screen = False
        
        # Fill background of the question screen with WHITE
        question_screen.fill(WHITE)

        # Wrap the question to fit question screen
        rect_question = pygame.Rect(100, 200, window_size[0] - 100, window_size[1] // 2)
        # Split text into lines and words
        words = [word.split(' ') for word in current_question.splitlines()]
        # Calculate the width and height of a space character
        space_width, space_height = font.size(' ')
        # Set the initial position to start drawing text (top-left corner of the rect)
        x, y = rect_question.topleft
        # Get the maximum width and height for text area
        max_width, max_height = rect_question.size
        # Get the height of a line of text
        line_height = font.get_linesize()
        # Iterate over each line in the text
        for line in words:
            # Iterate over each word in the line
            for word in line:
                # Render the word to get its surface
                word_surface = font.render(word, True, BLACK)
                # Get the width and height of the rendered word
                word_width, word_height = word_surface.get_size()
                # Check if the word exceeds the maximum width of the rect
                if (x + word_width) >= max_width:
                    # Move to the next line
                    x = rect_question.left
                    y += line_height
                # Draw the word on the surface at the current position
                question_screen.blit(word_surface, (x, y))
                # Check if the last character of the word is colon
                if word and (word[-1] == ':'):
                    # Move to the next 2 line
                    x = rect_question.left
                    y += 2 * line_height
                else:
                    # Move the x position to the right by the width of the word plus a space
                    x += word_width + space_width
            # After a line is completed, move to the next line
            x = rect_question.left
            y += line_height

        # Show the timer
        time_elapsed = pygame.time.get_ticks() - timer_start
        text_timer = font.render("{}".format(max(0, (timer_limit - time_elapsed) // 1000)), True, RED)
        rect_timer = text_timer.get_rect(center=(window_size[0] - 30, window_size[1] - 700))
        question_screen.blit(text_timer, rect_timer)

        # Show correct and incorrect buttons
        rect_correct_button = pygame.Rect((window_size[0] // 4) - 75, (window_size[1] // 2) + 250, 150, 50)
        rect_incorrect_button = pygame.Rect((3 * window_size[0] // 4) - 75, (window_size [1] // 2) + 250, 150, 50)
        pygame.draw.rect(question_screen, GREEN, rect_correct_button)
        pygame.draw.rect(question_screen, RED, rect_incorrect_button)
        text_correct = font.render("Correct", True, BLACK)
        text_incorrect = font.render("Incorrect", True, WHITE)
        text_correct_rect = text_correct.get_rect(center=(rect_correct_button.center))
        text_incorrect_rect = text_incorrect.get_rect(center=(rect_incorrect_button.center))
        question_screen.blit(text_correct, text_correct_rect)
        question_screen.blit(text_incorrect, text_incorrect_rect)

        # Update display
        pygame.display.flip()

def check_win_condition(current_player_scores):
    for current_player in current_player_scores:
        if current_player_scores[current_player] >= 15:
            return True
    return False

def show_winning_screen(current_player, current_player_score, team_names):
    # Define font for rendering text
    font = pygame.font.Font(None, 50)

    # Set up question screen window
    window_size = (600, 720)
    winning_screen = pygame.display.set_mode(window_size)

    running_winning_screen = True

    while running_winning_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_winning_screen = False
        
        # Fill background of the winning screen with WHITE
        winning_screen.fill(WHITE)

        if current_player == 1:
            text_winning = font.render("{} wins with {} points!".format(team_names[current_player], current_player_score[current_player]), True, RED)
        elif current_player == 2:
            text_winning = font.render("{} wins with {} points!".format(team_names[current_player], current_player_score[current_player]), True, BLUE)
        text_winning_rect = text_winning.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
        winning_screen.blit(text_winning, text_winning_rect)

        # Update display
        pygame.display.flip()

#def count():
    #temp_player_count_1 = 0
    #temp_player_count_2 = 0

    #while :
        