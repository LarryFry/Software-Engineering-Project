Project Proposal:

We are planning on re-creating the game hand and foot. Since there are many versions of this game we have outlined the rules we are going to follow below. For our
project we are wanting to have an online poker style look and AI capability to play against, since the game really needs at least 3-4 people. Our goal is to have
an interface that will allow the player to select and view other players books and other cards they currently have down. We are looking at making different levels
of AI that will allow some variety in the game. Some other minor aspects we are planning on implementing are choosing the number of decks every game, and a
scoreboard. If possible, we would also like to implement multiplayer functionality. We will mainly focus on solely AI's until the main game is constructed, since
multiplayer will most likely need more players than will be available through pure multiplayer.


MOSCOW Breakdown - FURPS Breakdown

Must:

    •	Main Menu – Functionality
        o	Way to select number of players (3-6) and decks (possibly based on players) – Functionality
    •	Way to see what other cards players have been played – Usability
        o	Click on other players to see their cards
        o	Online Poker Style Look
        o	Your own cards will be visible when it’s your own turn
        o	View will focus on other players views when it’s their turn
    •	AI to play against – Functionality
    •	Some way to see if another player is on their hand or foot – Usability
        o	Foot will either be present at the side of the deck their on or not

Should:

    •	Arcade Style Score Board – Functionality
    •	Different AI difficulties – Functionality
    •	Implement a way to read the rules – Functionality
        o	Little question mark in the corner permanently that will open up a rules tab
    •	Grouping way to organize played cards, as they are played - Usability

Could:

    •	Good Card Models – Usability
        o	One type of card model
    •	Sound – Usability
    •	Settings options (Resolution, sound, themes, option to see current scores) - Functionality/Usability
    •	Multiplayer – Functionality
    •	Team mode - Functionality

Wont:

    •	User profiles attached to score – Functionality
    •	Time limit - Functionality



Rules for Hand n’ Foot

    • This game is generally played with 3 to 8 players with 5+ decks of cards
    • Each player will get 28 cards, 14 will be their hand and the other 14 will be their foot
    • The player cannot look at their foot until all there cards in their hand are gone
    • The goal of the game is to end up with the most points by the end of the game
    • To get points the players must create books
        ◦ Books are created by matching sets of cards
        ◦ To lay down a book the player must either lay down 3 of the same card or 2 of the same card and a wild card
        ◦ Wild cards are jokers and 2s
        ◦ Once a book is created the player can add anytime to that book on their turn
    • Each of the cards have different point values
        ◦ 50 points: Joker
        ◦ 20 points: A’s and 2’s
        ◦ 10 points: 9-k
        ◦ 5 points: 4-8
        ◦ -500 points: Red 3’s
        ◦ -300 points: Black 3’s
    • Other ways to get points
        ◦ Going out first is 200 points
        ◦ Making a dirty kanasta is 300
            ▪ This is once you have 7+ cards in your book
        ◦ Making a clean kanasta is 500
            ▪ This is when you have a book with 7+ cards in it without wilds in it
    • Starting the game
        ◦ At the beginning of each players turn they will draw 2 cards from the deck or take the top 7 cards from the pile(if less than 7 then just take what is there)
        ◦ Then the player can try to make books if they can
        ◦ If there is nothing else that they can do then they end their turn by discarding one card to the pile
    • Ending the game
        ◦ To end the game you must be all out of cards and have at least one clean kanasta
