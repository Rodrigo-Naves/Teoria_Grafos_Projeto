import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Load the background image
background = pygame.image.load("field.png")
width, height = background.get_width(), background.get_height()

# Set up the window
screen = pygame.display.set_mode((width, height))

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0,255,0)

# Define node properties
node_radius = 20
max_nodes = 11
nodes = []
edges = []

# Define buttons
button_width, button_height = 150, 50
random_walk_button = pygame.Rect(width - button_width - 10, 10, button_width, button_height)
crucial_player_button = pygame.Rect(width - button_width - 10, 70, button_width, button_height)

def draw_node(node, index):
    pygame.draw.circle(screen, BLACK, node, node_radius)
    font = pygame.font.Font(None, 24)
    text = font.render(str(index), True, WHITE)
    text_rect = text.get_rect(center=node)
    screen.blit(text, text_rect)

def draw_edges():
    for edge in edges:
        draw_edge(edge[0], edge[1], edge[2])

def draw_edge(start, end, weight):
    pygame.draw.line(screen, RED, start, end, 2)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    pygame.draw.polygon(screen, RED, [end, (end[0] - 10 * dx / (dx ** 2 + dy ** 2) ** 0.5, end[1] - 10 * dy / (dx ** 2 + dy ** 2) ** 0.5),
                                      (end[0] - 10 * dx / (dx ** 2 + dy ** 2) ** 0.5 - 10 * dy / (dx ** 2 + dy ** 2) ** 0.5, end[1] - 10 * dy / (dx ** 2 + dy ** 2) ** 0.5 + 10 * dx / (dx ** 2 + dy ** 2) ** 0.5)])
    font = pygame.font.Font(None, 24)
    text = font.render(str(round(weight, 2)), True, BLACK)
    text_rect = text.get_rect(center=((start[0] + end[0]) // 2, (start[1] + end[1]) // 2))
    screen.blit(text, text_rect)

    # Draw arrowhead
    arrow_length = 10
    angle = -math.atan2(dy, dx)
    end_x = end[0] - arrow_length * math.cos(angle)
    end_y = end[1] + arrow_length * math.sin(angle)
    pygame.draw.line(screen, RED, (end_x, end_y), end, 2)

def update_weights():
    for node in nodes:
        total_edges = sum(edge[0] == node for edge in edges)
        for edge in edges:
            if edge[0] == node:
                edge[2] = 1 / total_edges

def random_walk(steps):
    visits = {node: 0 for node in nodes}
    current_node = random.choice(nodes)
    for _ in range(steps):
        neighbors = [edge[1] for edge in edges if edge[0] == current_node]
        if neighbors:  # Check if there are available neighbors
            weights = [edge[2] for edge in edges if edge[0] == current_node]
            current_node = random.choices(neighbors, weights)[0]
            visits[current_node] += 1
    most_visited_node = max(visits, key=visits.get)
    return most_visited_node, visits[most_visited_node]


def dfs(nodes, edges, start_node, visited=None):
    if visited is None:
        visited = set()
    visited.add(start_node)

    for edge in edges:
        if start_node in edge:
            neighbor = edge[1] if edge[0] == start_node else edge[0]
            if neighbor not in visited:
                dfs(nodes, edges, neighbor, visited)

def count_components(nodes, edges):
    visited = set()
    components = 0
    for node in nodes:
        if node not in visited:
            dfs(nodes, edges, node, visited)
            components += 1
    return components

def is_crucial_player(nodes, edges):
    articulation_points = []
    initial_components = count_components(nodes, edges)

    for node in nodes:
        modified_nodes = [n for n in nodes if n != node]
        modified_edges = [edge for edge in edges if node not in edge]
        modified_components = count_components(modified_nodes, modified_edges)

        if modified_components > initial_components:
            articulation_points.append(nodes.index(node) + 1)  # Adiciona o número do nó à lista

    return articulation_points

def display_result(result):
    font = pygame.font.Font(None, 24)
    text_surface = font.render(result, True, BLACK)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    
    # Create a message box rect
    message_box_rect = pygame.Rect(0, 0, text_rect.width + 20, text_rect.height + 20)
    message_box_rect.center = (width // 2, height // 2)
    
    # Draw message box background
    pygame.draw.rect(screen, WHITE, message_box_rect)
    
    # Draw text on the message box
    screen.blit(text_surface, text_rect)
    
    # Display changes on the screen
    pygame.display.flip()
    
    # Wait for the user to close the message box
    waiting_for_close = True
    while waiting_for_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting_for_close = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if message_box_rect.collidepoint(event.pos):
                    waiting_for_close = False


# Main loop
running = True
while running:
    screen.blit(background, (0, 0))  # Draw the background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                if len(nodes) < max_nodes:
                    x, y = pygame.mouse.get_pos()
                    nodes.append((x, y))
            elif event.button == 3:  # Right mouse button clicked
                x, y = pygame.mouse.get_pos()
                clicked_node = None
                for node in nodes:
                    if pygame.math.Vector2(node).distance_to((x, y)) <= node_radius:  # Check if the click is inside a node
                        clicked_node = node
                        break
                if clicked_node is not None:
                    start_node = clicked_node
                    selected_node = None
                    while selected_node is None:
                        pygame.event.pump()
                        for sub_event in pygame.event.get():
                            if sub_event.type == pygame.MOUSEBUTTONDOWN and sub_event.button == 3:  # Right mouse button clicked again
                                x, y = pygame.mouse.get_pos()
                                for node in nodes:
                                    if pygame.math.Vector2(node).distance_to((x, y)) <= node_radius:  # Check if the click is inside a node
                                        selected_node = node
                                        break
                                if selected_node is not None:
                                    if selected_node != start_node:
                                        weight = random.random()
                                        edges.append([start_node, selected_node, float(weight)])  # Convert weight to float
                                        update_weights()  # Update weights for random walk
                                        pygame.display.flip()
                                    else:
                                        selected_node = None
                    start_node = None


    # Drawing nodes
    for i, node in enumerate(nodes, start=1):
        draw_node(node, i)

    # Drawing edges
    draw_edges()

    # Drawing buttons
    pygame.draw.rect(screen, WHITE, random_walk_button)
    font = pygame.font.Font(None, 24)
    text = font.render("Random Walk", True, BLACK)
    text_rect = text.get_rect(center=random_walk_button.center)
    screen.blit(text, text_rect)
    
    pygame.draw.rect(screen, WHITE, crucial_player_button)
    text = font.render("Crucial Player", True, BLACK)
    text_rect = text.get_rect(center=crucial_player_button.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

    # Button functionality
    mouse_pos = pygame.mouse.get_pos()
    if random_walk_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        most_visited_node, visits = random_walk(100)  # Perform a random walk for 100 steps
        result_text = f"Most visited Node: {nodes.index(most_visited_node) + 1} - with {visits} visits"
        display_result(result_text)

    if crucial_player_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        crucial_nodes = is_crucial_player(nodes, edges)
        result_text = f"{[crucial_nodes]}"
        display_result(result_text)

pygame.quit()
