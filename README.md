# Random Chess Bot Version 2
This is version 2 of random chess bot.

Version 2 is more efficient than version 1 by implementing the following:
- Implemented class inheritance.
- Added validation to eliminate moves that would put the player in check.
- Ditched `pyautogui` in favor of `selenium` web browser.
- Web scraping help accomplished with `beautifulsoup`.
- Added login validation and cookie saving & loading.
- By implementing `rich`, the whole thing can be viewed and played in a terminal.

# Running with docker
```
docker build -t chess-bot .
docker run -it -v C:/Users/User/.chess_login:/app/src/logins --name chess-bot chess-bot
docker start -ai chess-bot
```

## Random Chess Bot Version 1
[Link to version 1 of random chess bot](https://github.com/Jampamane/Random_Chess_1.0)

=== "Tab 1"
    Markdown **content**.

    Multiple paragraphs.

=== "Tab 2"
    More Markdown **content**.

    - list item a
    - list item b
