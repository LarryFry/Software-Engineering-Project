'''Imports'''
import pygame, sys
from pygame.locals import *
import random
import time

from importlib import reload
import game_classes;

reload(game_classes)

target_fps = 60
title = "FPS Timer Demo"

'''Rules state'''


def Rules():
    # Reset screen
    screen.fill(pygame.Color("grey"))
    pygame.display.flip()

    back_button = game_classes.Button_Hover("BACK", (0, 0), screen, "topleft")

    # Rules Loop
    done = False
    while not done:
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()

        back_button.check_hover(screen)

        rules_dis = "Rules for Hand n’ Foot \n• This game is generally played with 3 to 8 players with 5+ decks of cards \n• Each player will get 28 cards, 14 will be their hand and the other 14 will be their foot \n• The player cannot look at their foot until all there cards in their hand are gone \n• The goal of the game is to end up with the most points by the end of the game \n• To get points the players must create books \n    ◦ Books are created by matching sets of cards \n    ◦ To lay down a book the player must either lay down 3 of the same card or 2 of the same card and a wild card \n    ◦ Wild cards are jokers and 2s \n    ◦ Once a book is created the player can add anytime to that book on their turn \n• Each of the cards have different point values \n    ◦ 50 points: Joker \n    ◦ 20 points: A’s and 2’s \n    ◦ 10 points: 9-k \n    ◦ 5 points: 4-8 \n    ◦ -500 points: Red 3’s \n    ◦ -300 points: Black 3’s \n• Other ways to get points \n    ◦ Going out first is 200 points \n    ◦ Making a dirty kanasta is 300 \n    ▪ This is once you have 7+ cards in your book \n    ◦ Making a clean kanasta is 500 \n        ▪ This is when you have a book with 7+ cards in it without wilds in it \n• Starting the game \n      ◦ At the beginning of each players turn they will draw 2 cards from the deck or take the top 7 cards from the pile(if less than 7 then just take what is there) \n    ◦ Then the player can try to make books if they can \n    ◦ If there is nothing else that they can do then they end their turn by discarding one card to the pile \n• Ending the game \n   ◦ To end the game you must be all out of cards and have at least one clean kanasta"
        o = 0
        for line in rules_dis.splitlines():
            font = pygame.font.SysFont("timesnewroman", 15, '')
            txt = font.render(line, True, (0, 0, 0))
            screen.blit(txt, (60 - txt.get_width() // 15, 40 - txt.get_height() // 2 + o))
            o += 15

        if back_button.rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            done = True

        pygame.display.flip()
        pygame.display.update()


'''Game state'''

def GameMode():
    # Reset screen
    screen.fill(pygame.Color("forestgreen"))
    pygame.display.flip()

    # Buttons for menu
    menu_space = pygame.draw.rect(screen, pygame.Color("grey"), [0, 480, 960, 60])
    canasta_button = game_classes.Button_Hover("Canasta", (80, 510), screen, "center")
    draw_button = game_classes.Button_Hover("Draw 2", (240, 510), screen, "center")
    pile_button = game_classes.Button_Hover("Take pile", (400, 510), screen, "center")
    discard_button = game_classes.Button_Hover("Discard", (560, 510), screen, "center")
    rules_button = game_classes.Button_Hover("Rules", (720, 510), screen, "center")
    quit_button = game_classes.Button_Hover("QUIT", (880, 510), screen, "center")

    # Buttons to see other players
    pygame.draw.circle(screen, pygame.Color("grey"), [100, 0], 100)
    pygame.draw.circle(screen, pygame.Color("grey"), [480, 0], 100)
    pygame.draw.circle(screen, pygame.Color("grey"), [860, 0], 100)

    player2_button = game_classes.Button_Hover("Player 1", (100, 0), screen, "midtop")
    player3_button = game_classes.Button_Hover("Player 2", (480, 0), screen, "midtop")
    player4_button = game_classes.Button_Hover("Player 3", (860, 0), screen, "midtop")

    font = pygame.font.Font(None, 40)
    player1_display = font.render("H", True, pygame.Color("black"))
    screen.blit(player1_display, player1_display.get_rect(center=(100, 60)))
    player2_display = font.render("H", True, pygame.Color("black"))
    screen.blit(player2_display, player2_display.get_rect(center=(480, 60)))
    player3_display = font.render("H", True, pygame.Color("black"))
    screen.blit(player3_display, player3_display.get_rect(center=(860, 60)))

    # GameMode Loop
    done = False
    canasta_on_screen = False
    i = 0
    deck = game_classes.Deck()
    deck.shuffle()

    # Creating players
    player1 = game_classes.Player(deck)
    player2 = game_classes.Player(deck)
    player3 = game_classes.Player(deck)
    player4 = game_classes.Player(deck)

    # Starting positions for the players cards
    hf_x_start, hf_y_start, x_overlap_dist = 80, 370, 30
    card_height, card_width = 90, 60
    display_hand(player1)

    #  Starting positions for thr canastas cards
    c_x_start, c_y_start, y_shift = 25, 150, 15

    #  Drawing the starting deck card back
    card = pygame.image.load("res/img/cards/red_back.png").convert()
    card = pygame.transform.scale(card, (card_width, card_height))
    screen.blit(card, [640, 25])

    # Where the pile will be drawn when it is created
    screen.blit(card, [260, 25])

    prev_time = time.time()
    while not done:
        click = pygame.mouse.get_pressed()
        pygame.time.wait(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # Checks for clicking on cards in the hand and if it detects it, will toggle the selected attribute of the card and re-draw the hand
                if (pos[1] < (hf_y_start + card_height)) and (pos[1] > hf_y_start):
                    if (pos[0] > hf_x_start) and (pos[0] < (x_overlap_dist * len(player1.get_hand())) + hf_x_start + x_overlap_dist):
                        card_pos = pos[0] - hf_x_start
                        card_pos = int(card_pos / x_overlap_dist)
                        if card_pos > len(player1.get_hand())-1:
                            card_pos -= 1
                        player1.get_hand()[card_pos].toggle_selected()
                        display_hand(player1)
                # Checks for clicking on canasta's, and if it detects it, will attempt to add any selected cards to that canasta
                if (pos[0] > c_x_start and pos[0] < card_width * len(player1.get_canastas()) + c_x_start and pos[1] > c_y_start):
                    index = int((pos[0] - c_x_start)/card_width)
                    # Statement checks whether the stack has been squished or not
                    if (len(player1.get_canastas()) * y_shift + 60 > 200):
                        y_shift = (200 - 60) / (len(player1.get_canastas()))
                    # Checks that the mouse button up was detected on a y position that has cards on it, and if so, attempts to add cards
                    if (pos[1] < (len(player1.get_canastas()[index])-1) * y_shift + c_y_start + card_height):
                        player1.add_to_canasta(index)
                        display_canasta(player1)
                        display_hand(player1)
                        y_shift = 15


        # Check for hover for menu
        canasta_button.check_hover(screen)
        draw_button.check_hover(screen)
        pile_button.check_hover(screen)
        discard_button.check_hover(screen)
        rules_button.check_hover(screen)
        quit_button.check_hover(screen)

        player2_button.check_hover(screen)
        # Check hover for players
        if player2_button.hovered == True and i == 0:
            # print ("hover 1")
            # player1_hand = False
            # pygame.draw.circle(screen, pygame.Color("grey"), [100, 0], 100)
            overlay = pygame.Rect(10, 10, (card_width*len(player2.hand)/2) + x_overlap_dist + 40, card_height + 40)
            overlay.center = (screen.get_width()/2, (screen.get_height()/2) - 50)
            pygame.draw.rect(screen, pygame.Color("grey"), overlay)
            display_on_hover(player2, overlay)
            pygame.display.flip()
            reset_overlay = pygame.Rect(10, 10, (card_width*len(player2.hand)/2) + x_overlap_dist + 40, card_height + 40)
            reset_overlay.center = (screen.get_width()/2, (screen.get_height()/2) - 50)
            player2_button = game_classes.Button_Hover("Player 1", (100, 0), screen, "midtop")
            player2_button.check_hover(screen)
            i += 1
        elif player2_button.hovered == False and canasta_on_screen and i > 0:
            i = 0
            pygame.draw.rect(screen, pygame.Color("gold"), (20, 140, 920, 200))
            display_canasta(player1)
        elif player2_button.hovered == False and not canasta_on_screen:
            i = 0
            reset_overlay = pygame.Rect(10, 10, (card_width*len(player2.hand)/2) + x_overlap_dist + 40, card_height + 40)
            reset_overlay.center = (screen.get_width()/2, (screen.get_height()/2) - 50)
            pygame.draw.rect(screen, pygame.Color("forestgreen"), reset_overlay)

        player3_button.check_hover(screen)
        if player3_button.hovered == True:
            # print ("hover 2")
            pass
        player4_button.check_hover(screen)
        if player4_button.hovered == True:
            # print ("hover 3")
            pass

        # See if button was clicked in the menu
        # call make_canasta(cards) with the cards being an array of selected cards
        if canasta_button.rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            selected_cards = player1.get_selected_cards()
            if player1.make_canasta(selected_cards):
                canasta_on_screen = True
                for pos in range(len(selected_cards)):
                    player1.remove_card(selected_cards[pos])
            print (player1.get_canastas())
            display_canasta(player1)
            display_hand(player1)
            canasta_on_screen = True

        if draw_button.rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            print("draw 2")
            player1.add_card(deck.get_card())
            player1.add_card(deck.get_card())
            display_hand(player1)

        if pile_button.rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            # print("pile")
            pass

        if discard_button.rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            print("discard")
            temp_discard_deck = player1.get_selected_cards()
            if (len(temp_discard_deck) != 1):  # Unclear discard
                print(temp_discard_deck)
                print("Incorrect number of cards")
            else:  # Clear Discard
                print(temp_discard_deck)
                print("Correct number of cards")
                player1.remove_card(temp_discard_deck[0])
            player2.take_turn()
            display_hand(player1)

        if rules_button.rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            # print("rules")
            pass

        if quit_button.rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            done = True

        # Check if players are in hand or foot
        if not player1.on_hand():
            player1_display = font.render("F", True, pygame.Color("black"))
            screen.blit(player1_display, player1_display.get_rect(center=(100, 60)))
        if not player2.on_hand():
            player2_display = font.render("F", True, pygame.Color("black"))
            screen.blit(player2_display, player2_display.get_rect(center=(100, 60)))
        if not player3.on_hand():
            player3_display = font.render("F", True, pygame.Color("black"))
            screen.blit(player3_display, player3_display.get_rect(center=(100, 60)))


        pygame.display.flip()
        pygame.display.update()

        curr_time = time.time()  # so now we have time after processing
        diff = curr_time - prev_time  # frame took this much time to process and render
        delay = max(1.0 / target_fps - diff,
                    0)  # if we finished early, wait the remaining time to desired fps, else wait 0 ms!
        time.sleep(delay)
        fps = 1.0 / (delay + diff)  # fps is based on total time ("processing" diff time + "wasted" delay time)
        prev_time = curr_time
        pygame.display.set_caption("{0}: {1:.2f}".format(title, fps))

# Displays a players hand in the lower section of the screen
def display_hand(player):
    x_start, y_start, x_overlap_dist = 80, 370, 30
    card_height, card_width = 90, 60
    x_shift = x_start

    pygame.draw.rect(screen, pygame.Color("forestgreen"), (
        x_start-70, y_start - 10, x_overlap_dist * ((len(player.hand))+10) + x_overlap_dist, card_height + 10))

    # Display card back to represent that the the player is on their hand
    if player.on_hand():
        card = pygame.image.load("res/img/cards/red_back.png").convert()
        card = pygame.transform.scale(card, (card_width, card_height))
        screen.blit(card, [x_shift-70, y_start])

    # Goes through every card in the hand and displays it
    # Displays selected cards slightly raised
    for item in player.get_hand():
        card_name = "res/img/cards/" + item.get_name().lower() + ".png"
        card_name = card_name.replace(" ", "_")
        card = pygame.image.load(card_name).convert()
        card = pygame.transform.scale(card, (card_width, card_height))
        if (item.is_selected() == False):
            screen.blit(card, [x_shift, y_start])
        else:
            screen.blit(card, [x_shift, y_start - 10])
        x_shift = x_shift + x_overlap_dist

# Displays a players canasta's in the middle of the screen
def display_canasta(player):
    card_height, card_width, start_x, start_y, y_shift, x_shift = 90, 60, 25, 140, 15, 60
    y_temp = start_y
    pygame.draw.rect(screen, pygame.Color("forestgreen"), (20, 130, 920, 215))
    for can in player.get_canastas():
        y_shift = 15
        # Will adjust the y-distance between cards of a canasta when too many are present, effectively squishing them
        if (len(can)*y_shift + 60 > 200):
            y_shift = (200-60)/(len(can))
        for card in can:
            card_name = "res/img/cards/" + card.get_name().lower() + ".png"
            card_name = card_name.replace(" ", "_")
            card_img = pygame.image.load(card_name).convert()
            card_img = pygame.transform.scale(card_img, (card_width, card_height))
            screen.blit(card_img, [start_x, y_temp])
            y_temp = y_temp + y_shift
        start_x = start_x + x_shift
        y_temp = start_y

def display_on_hover(player, rect):
    x_start, y_start, x_overlap_dist = rect.left + 20, rect.top + 20, 30
    card_height, card_width = 90, 60
    x_shift = x_start

    #Display card back to represent that the the player is on their hand
    for item in player.get_hand():
        card_name = "res/img/cards/" + item.get_name().lower() + ".png"
        card_name = card_name.replace(" ", "_")
        card = pygame.image.load(card_name).convert()
        card = pygame.transform.scale(card, (card_width, card_height))
        screen.blit(card, [x_shift, y_start])
        x_shift = x_shift + x_overlap_dist


'''Options state'''

def Options():
    # Reset screen
    screen.fill(pygame.Color("grey"))
    pygame.display.flip()

    back_button = game_classes.Button_Hover("BACK", (0, 0), screen, "topleft")

    # Options Loop
    done = False
    while not done:
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()

        back_button.check_hover(screen)

        if back_button.rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            done = True

        pygame.display.flip()
        pygame.display.update()


'''Main and automatically starts at main menu'''
if __name__ == "__main__":
    # Initialize game
    pygame.init()
    pygame.font.Font(None, 40)

    # Get resolution and make screen
    infoObject = pygame.display.Info()

    # width, height = int(infoObject.current_w/4), int(infoObject.current_h/4)
    width, height = 960, 540

    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Hand and Foot')
    print("Width", width, "\nHeight", height)
    # print (infoObject.current_w, infoObject.current_h)

    x1, x2 = width / 5, width / 1.4
    y = height / 2
    menu_options = [game_classes.Button_Hover("PLAY", (x1, y), screen, "topleft"),
                    game_classes.Button_Hover("RULES", (x1, y + 50), screen, "topleft"),
                    game_classes.Button_Hover("OPTIONS", (x2, y), screen, "topleft"),
                    game_classes.Button_Hover("QUIT", (x2, y + 50), screen, "topleft")]

    # Main menu loop
    done = False
    while not done:
        # Set background
        background = pygame.image.load("res/img/back.jpg")
        # background = pygame.image.load("res/img/back(resized).jpg")
        background = pygame.transform.scale(background, (width, height))
        screen.blit(background, [0, 0])

        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # menu_options
        for cycle_menu in menu_options:
            cycle_menu.check_hover(screen)

        if menu_options[0].rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            GameMode()
        elif menu_options[1].rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            Rules()
        elif menu_options[2].rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            Options()
        elif menu_options[3].rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
            done = True

        pygame.display.update()

    # Exit
    pygame.quit()
    sys.exit()
