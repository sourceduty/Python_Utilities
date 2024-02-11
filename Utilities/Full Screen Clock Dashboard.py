# Full Screen Clock Dashboard
# Copyright (c) 2023, Sourceduty

# This software is free and open-source; anyone can redistribute it and/or modify it.

import pygame
import sys
from datetime import datetime, timedelta

# Initialize pygame
pygame.init()

# Set display dimensions
screen_width = 1920
screen_height = 1080

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Set fonts
time_font = pygame.font.SysFont(None, 200)
date_font = pygame.font.SysFont(None, 100)
meter_font = pygame.font.SysFont(None, 50)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME) # Remove window frame
pygame.display.set_caption("Dashboard Display")

# Adjust display position to compensate for window caption bar
screen_pos = screen.get_rect().move(0, 25)  # Adjust the position to remove the caption bar

clock = pygame.time.Clock()

# Get start time
start_time = datetime.now()

# Main loop
while True:
    screen.fill(BLACK)  # Fill the screen with black

    # Get current time and date
    current_time = datetime.now().strftime("%I:%M:%S %p")  # 12-hour clock with AM/PM
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Calculate total running time
    elapsed_time = datetime.now() - start_time

    # Render time text
    time_text = time_font.render(current_time, True, WHITE)
    time_text_rect = time_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

    # Render date text
    date_text = date_font.render(current_date, True, WHITE)
    date_text_rect = date_text.get_rect(center=(screen_width // 2, screen_height // 2))

    # Render total running time meter
    meter_text = meter_font.render("Running Time: {}".format(str(elapsed_time)), True, GREY)
    meter_text_rect = meter_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

    # Blit the text onto the screen
    screen.blit(time_text, time_text_rect)
    screen.blit(date_text, date_text_rect)
    screen.blit(meter_text, meter_text_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the display
    pygame.display.update(screen_pos)

    # Cap the frame rate
    clock.tick(60)
