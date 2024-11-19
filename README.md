### A description of a bot using the library of icons for the SteamPay Store API:

- Tsigned to interact with the SteamPay store API.- Overall, the bot enhances the user experience by bringing the SteamPay store services directly to Telegram users through a seamless and interactive interface.he bot is designed to interact with the SteamPay store API.
- It is written in Python and utilizes the aiogram library for Telegram bot development.
- The bot allows users to perform various actions related to the SteamPay store, such as:
- Retrieve game information.
- Check for game sales and discounts.
- Facilitate game purchases through the SteamPay store.
- Users can interact with the bot through Telegram, making it convenient to access SteamPay store services.
- The use of the aiogram library ensures efficient handling of Telegram bot functionalities within the Python environment.
- Overall, the bot enhances the user experience by bringing the SteamPay store services directly to Telegram users through a seamless and interactive interface.

Python bot for interacting with the API of online stores. Offers product information, sales tracking, and an integrated interface in Telegram

<img src="Telegram_bot_Game_Store.jpg" width="300">

### Libraries are needed

`bot_game.py`

```python
from aiogram import Bot, types, Dispatcher, Router
import aiogram.utils.markdown as fmt
from game_api import Api_data
from keyboards import button
from config import TOKEN
from aiogram.filters import Command

# FSMContext, MemoryStorage, State, StatesGroup are needed to pass a list from one function to another
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

import asyncio
import logging
import sys
```
This code is used to create a Telegram bot using the Aiogram library. It initializes the bot, the dispatcher, and implements a class for handling states (for example, stages of user interaction).

### Here are the explanations for each block:

```python
# Initializing a bot using a token
bot = Bot(token=TOKEN)
# Use MemoryStorage to store user states in memory (without using a database)
storage = MemoryStorage()

# Initializing the Dispatcher for event processing
dp = Dispatcher(storage=storage)

# Initialization of the router (Router), which allows you to separate the logic of event processing
router = Router()
# Add a router to the manager
dp.include_router(router)

# Defining a state class used to handle multi-step user interactions
class Form(StatesGroup):
    # Create a state “waiting_for_list” - to wait for the user to enter a list or other data
    waiting_for_list = State()

```

### Explanation:

```python
bot = Bot(token=TOKEN)
```
- Creates a bot object using an access token issued by Telegram to work with the API.

```python
storage = MemoryStorage()
```
- Indicates that the application's memory will be used to store user states (for example, at what stage of interaction the user is). This is useful for simple bots, but for larger ones, you can use, for example, Redis or a database.

```python
dp = Dispatcher(storage=storage)
```
- Initializes the dispatcher that manages events and messages. It uses MemoryStorage for state management.

```python
router = Router()
```
- Creates a router that allows you to divide event processing in the bot into logical parts (for example, for different commands or message types).

```python
dp.include_router(router)
```
- Connects a router to the dispatcher, allowing events to be processed through the router.

```python
class Form(StatesGroup)
```
- Creates a class for working with state groups, which allows you to manage multi-step user interaction scenarios (for example, when a bot requests a sequence of responses from a user).

```python
waiting_for_list = State()
```
- Defines a specific state that will be active when the bot is waiting for, for example, a list or other data from the user.


- This code is part of a Telegram bot written with the Aiogram library. It is responsible for processing commands and messages from the user, as well as displaying a list of games in a scrolling menu.

### Here is an explanation of each part of the code:

```python
# introduction
@dp.message(Command(commands=["start"]))
async def start_bot(message: types.Message):
    await message.answer('Enter the name of the game')
```

```python
@dp.message(Command(commands=[“start”])):
```
- This is a decorator that associates a function with the /start command. When the user enters the /start command, this function will be called.

```python
async def start_bot(message: types.Message):
```
- An asynchronous function called with the /start command. It takes a message object containing information about the message from the user.

```python
    await message.answer('Enter the name of the game')
```
- Sends a response to the user with the text “Enter the name of the game”. The bot is waiting for the user to enter the name of the game.

```python
# this function will display a scrolling menu of games
@dp.message()
async def bot_send_message(message: types.Message, state: FSMContext):
```

```python
@dp.message():
```
- This is a decorator that handles all messages that the user sends, not necessarily commands. The function will be called on any text message.

```python
async def bot_send_message(message: types.Message, state: FSMContext):
```
- This is an asynchronous function that processes user messages and manages user states via FSMContext.

```python
    # is a replacement for the global function
    # to add data to the process_callback_button1 function

    my_list = Api_data(message.text)
```

```python
my_list = Api_data(message.text)
```
- The Api_data function takes the user's text message (game name) and probably calls the API to get a list of matching games. my_list is the list of games that will be used for display.

```python
    # save the list of games
    await state.set_state(Form.waiting_for_list)
    await state.update_data(my_list=my_list)
```

```python
await state.set_state(Form.waiting_for_list)
```
- Sets the bot to the state of waiting for the game list. This state is used to handle subsequent interactions with the user.

```python
await state.update_data(my_list=my_list)
```
- Updates the state data by saving the list of games to my_list. This will allow the bot to continue working with this list.

```python
index = len(my_list)
```
- The index variable stores the number of games in the list to be used later to indicate the current position in the list.

```python
    try:
        await message.answer(
            fmt.text(
                'ㅤ',
                fmt.hide_link(my_list[0][1])
                ),
            parse_mode="HTML",
            reply_markup=button(my_list[0][1], f"1/{index}")
            )
```

```python
fmt.text('ㅤ', fmt.hide_link(my_list[0][1]))
```
- Creates a message with a hidden link to the first game in the list my_list[0][1]. The fmt.hide_link() function is used to hide the URL when displaying text.

```python
await message.answer(..., reply_markup=button(my_list[0][1], f “1/{index}”))
```
- Sends a message to the user with HTML markup (e.g., a hidden link) and attaches buttons to it to navigate the list of games using the button() function. The text on the button shows the position in the list (for example, “1/10”).


```python
    except IndexError:
        await message.answer('Game not found')
```

```python
except IndexError:
```
- If a function tries to access a list item that does not exist (for example, if the list is empty), an IndexError will be thrown. In this case, the bot will send the message “Game not found”.

### Summary:
This code processes a message from the user, gets the list of games via the Api_data function, stores it in a state, and then displays the first game in the list along with a navigation button. If the list is empty or an error occurs, the bot notifies the user that the game was not found.


### Now let's create an inline button

This code is responsible for processing callback requests (button presses) in the Telegram bot, as well as for navigating the list of games using the “back” and “NEXT” buttons. It allows the user to navigate through the list of games by changing the displayed game.

```python
# button
@router.callback_query(lambda c: c.data in ['back', 'NEXT'])
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
```

```python
@router.callback_query(lambda c: c.data in ['back', 'NEXT']):
```
- This is a decorator that binds a function to callback queries from buttons where the data value is either 'back' or 'NEXT'. This data is passed when the corresponding button is clicked.

```python
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
```
- An asynchronous function that processes user callback requests and works with the current state of the bot via FSMContext.

```python
await callback_query.answer():
```
- Called so that Telegram knows that the callback request has been processed, even if no response is sent to the user.


```python
    user_data = await state.get_data()
    my_list = user_data.get('my_list')
```

```python
user_data = await state.get_data():
```
- Gets the saved state data for the current user. This is the data that was saved earlier (for example, a list of games).

```python
my_list = user_data.get('my_list')
```
- Gets the list of games from the saved data.

```python
    index = len(my_list)
```
- Stores the number of games in the list to know how many items are available for navigation.

```python
    async def bot_keyboards():
        # 'callback_query.message.edit_text' is needed to change the displayed game in the list to the next game in the list 
        await callback_query.message.edit_text(
            fmt.text(
                'ㅤ',
                fmt.hide_link(my_list[0][1])
                ),
            parse_mode="HTML",
            reply_markup=button(my_list[0][1], f"{my_list[0][0]}/{index}")
            )
```

```python
async def bot_keyboards():
```
- This is an internal function that updates the message with the new game. It is used to change the text and buttons in an already sent message.

```python
callback_query.message.edit_text(...)
```
- Updates the message text (changes the displayed game). The hidden URL of the game remains unchanged, and the game index changes to reflect the new position in the list.

```python
reply_markup=button(...)
```
- Adds new buttons to interact with the menu, updating the current user interface.


```python
    if callback_query.data == 'NEXT':
        # this code adds a game from the beginning of the list to the end and adds a game from the end of the list to the beginning
        my_list.append(my_list[0])
        my_list.remove(my_list[0])
        await bot_keyboards()
```

```python
if callback_query.data == 'NEXT':
```
- If the “NEXT” button is clicked, this code block will be executed.

```python
my_list.append(my_list[0])
```
- The first item in the list is moved to the end of the list and then removed from its original position. Thus, the game that was next becomes the first.

```python
await bot_keyboards()
```
- Calls the internal bot_keyboards() function to update the displayed game.

```python
    if callback_query.data == 'back':
        # this code works the other way around
        my_list.insert(0, my_list[-1])
        my_list.pop(index)
        await bot_keyboards()
```

```python
if callback_query.data == 'back':
```
- If the “back” button is pressed, this code block will be executed.

```python
my_list.insert(0, my_list[-1])
```
- The last item in the list is moved to the first position and then deleted from its original location (last index).

```python
await bot_keyboards()
```
- Updates the displayed game after reordering the items in the list.


```python
async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
```
- This code starts the Telegram bot

```python
main()
```
- is an asynchronous function that starts “polling” so that the bot can receive and process messages in real time.

```python
if __name__ == “__main__”:
```
- this code block is executed if the script is run directly, not imported.

```python
logging.basicConfig(...)
```
- configures logging to display information messages to the console.

```python
asyncio.run(main())
```
- runs the asynchronous main() function.


### Now we will search for games through the api

`game_api.py`
```python
import requests
from googleapiclient.discovery import build
```
- requests: is used to send HTTP requests to websites, in particular to interact with the Steampay API to get information about games.
- googleapiclient.discovery.build: this is a function that creates a client to interact with the Google Custom Search API, which allows you to make search queries through Google.

```python
api_key = 'GIzaSyCAczneS201lYQnPUSZ-JlPRVqes0vCgvI'
cse_id = '151621wbf1a704a45'
```
- api_key: This is your key to access the Google Custom Search API, which allows you to perform searches on Google through the programmatic interface.
- cse_id: This is the ID of your customized search engine (Custom Search Engine), which can be created on the Programmable Search Engine website. It is used to narrow down search results.

```python
def Api_data(query):
    found_games = []
```
- The Api_data(query) function takes an input parameter query, which is a keyword that the user enters to search for a game.
- found_games: a list where all found games are saved. Each element of the list contains the index and URL of the game.

```python
    service = build('customsearch', 'v1', developerKey=api_key)
    result = service.cse().list(q=query, cx=cse_id).execute()
```
- service: creates a service object using build() that configures interaction with the Google Custom Search API. For this, the api_key API key is used.
- result: using the service object, the list() method is called, which takes the query keyword and the search engine ID cse_id. This executes a query to Google and returns the search results, which are stored in the result variable.

```python
    index_game = 1
    for item in result['items']:
        response = requests.get(f'https://steampay.com/api/search?query={item["title"]}')

        response_json = response.json()
```
- index_game = 1: this is a variable for indexing the games found, starting from 1, not 0, to make it more convenient for the user.
- The loop goes through each item in the Google search results result['items'], where each item represents a found page or resource.
- For each result, an additional request is made to the Steampay API via requests.get(), where a game with the same name as the one found on Google is searched.

```python
        for item_2 in response_json['products']:
            found_games.append([index_game, f"{item_2['url']}"])
            index_game += 1
```
- response_json: the Steampay API response is converted to JSON format using .json().
- Then, within each Steampay result, a loop goes through the found products (response_json['products']).
	- Each found product (game) is added to the found_games list, where:
	- index_game - the index of the game in the list.
- item_2['url'] - URL of the game's page in Steampay.
- index_game += 1 increases the index by 1 for each game found.

```python
    return found_games
```
- The function returns a list of found_games, where each element contains the index and URL of the game that was found through the Steampay API.


### This code implements a keyword search using the Google Custom Search API, and then adds to that requests to the Steampay API to get data about the games found. It returns a list of games with their indexes and URLs that can be used in a bot or other program.


### Now let's create inline buttons

`keyboards.py`
```python
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
```
- aiogram.types: contains data types used in Aiogram to work with messages, buttons, keyboards, etc.
- InlineKeyboardBuilder: a tool to simplify the creation of inline keyboards (i.e. buttons that are placed in messages and can perform actions when pressed).

```python
def button(url: str, availability_0_0: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
```
- button(url: str, availability_0_0: str): the function takes two arguments:
	- url is the URL to which one of the keyboard buttons leads.
	- availability_0_0 - the text for the center button that displays some information, such as product status or availability.
- builder = InlineKeyboardBuilder(): creates a builder object that helps to build an inline keyboard.

```python
builder.row(
    types.InlineKeyboardButton(text='◀', callback_data='back'),
    types.InlineKeyboardButton(text=availability_0_0, callback_data='AVAILABILITY'),
    types.InlineKeyboardButton(text='▶', callback_data='NEXT')
)
```
- builder.row(): adds a row with three buttons to the inline keyboard:
1. ◀ is the back button. When pressed, it sends an event with callback_data='back'.
2. availability_0_0 - the center button with the text passed through the availability_0_0 argument. It sends an event with callback_data='AVAILABILITY', which can be processed by the bot.
3. ▶ - button to move forward. Sends an event with callback_data='NEXT'.

```python
builder.row(
    types.InlineKeyboardButton(text='Reference', url=url)
)
```
- The second line of the keyboard contains a single Reference button, which is a hyperlink and opens the URL passed through the url argument.

```python
return builder.as_markup()
```
- builder.as_markup(): the as_markup() method converts the built keyboard into a format that can be used as an inline keyboard in Telegram messages.

### and now add the token to the config.py file

`config.py`
```python
TOKEN = '8114200429:KAGpXZEN7IE4cS3YS5fOa0WpWvFH5W8Hatv'
```

### All ready code

`bot_game.py`
```python
from aiogram import Bot, types, Dispatcher, Router
import aiogram.utils.markdown as fmt
from game_api import Api_data
from keyboards import button
from config import TOKEN
from aiogram.filters import Command

# FSMContext, MemoryStorage, State, StatesGroup are needed to pass a list from one function to another
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

import asyncio
import logging
import sys

bot = Bot(token=TOKEN)
storage = MemoryStorage()

dp = Dispatcher(storage=storage)

router = Router()
dp.include_router(router)

class Form(StatesGroup):
    waiting_for_list = State()

# introduction
@dp.message(Command(commands=["start"]))
async def start_bot(message: types.Message):
    await message.answer('Enter the name of the game')

# this function will display a scrolling menu of games
@dp.message()
async def bot_send_message(message: types.Message, state: FSMContext):

    # is a replacement for the global function
    # to add data to the process_callback_button1 function

    my_list = Api_data(message.text)
    
    # save the list of games
    await state.set_state(Form.waiting_for_list)
    await state.update_data(my_list=my_list)

    index = len(my_list)

    try:
        await message.answer(
            fmt.text(
                'ㅤ',
                fmt.hide_link(my_list[0][1])
                ),
            parse_mode="HTML",
            reply_markup=button(my_list[0][1], f"1/{index}")
            )

    except IndexError:
        await message.answer('Game not found')

# button
@router.callback_query(lambda c: c.data in ['back', 'NEXT'])
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_data = await state.get_data()
    my_list = user_data.get('my_list')

    index = len(my_list)

    async def bot_keyboards():
        # 'callback_query.message.edit_text' is needed to change the displayed game in the list to the next game in the list 
        await callback_query.message.edit_text(
            fmt.text(
                'ㅤ',
                fmt.hide_link(my_list[0][1])
                ),
            parse_mode="HTML",
            reply_markup=button(my_list[0][1], f"{my_list[0][0]}/{index}")
            )

    if callback_query.data == 'NEXT':
        # this code adds a game from the beginning of the list to the end and adds a game from the end of the list to the beginning
        my_list.append(my_list[0])
        my_list.remove(my_list[0])
        await bot_keyboards()

    if callback_query.data == 'back':
        # this code works the other way around
        my_list.insert(0, my_list[-1])
        my_list.pop(index)
        await bot_keyboards()


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
```

`game_api.py`
```python
# this code performs a keyword search
# The googleapiclient library will help us create a search engine
# requests library is needed for our api

import requests
from googleapiclient.discovery import build


# here you can get api https://developers.google.com/custom-search/v1/introduction
# click on the "Get a Key" button
api_key = 'GIzaSyCAczneS201lYQnPUSZ-JlPRVqes0vCgvI'

# here you can get cse_id https://programmablesearchengine.google.com/
cse_id = '151621wbf1a704a45'

def Api_data(query):
    # found_games is a variable with a list in which the found games will be stored
    found_games = []

    # the service and result variables will scale keywords
    service = build('customsearch', 'v1', developerKey=api_key)
    result = service.cse().list(q=query, cx=cse_id).execute()


    # the index_game variable is needed to index games from 1 instead of 0
    # python counts from 0, not from 1
    # so every game found will be indexed
    # this is necessary for beauty and for the bot user to see which game is on the list

    index_game = 1
    for item in result['items']:
        # the response variable contains the api
        # in this bot I used the game store api "steampay"
        response = requests.get(f'https://steampay.com/api/search?query={item["title"]}')

        response_json = response.json()

        for item_2 in response_json['products']:
            # add all found games to the list
            found_games.append([index_game, f"{item_2['url']}"])

            index_game += 1

    return found_games
```

`keyboards.py`
```python
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def button(url: str, availability_0_0: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='◀', callback_data='back'),
        types.InlineKeyboardButton(text=availability_0_0, callback_data='AVAILABILITY'),
        types.InlineKeyboardButton(text='▶', callback_data='NEXT')
    ).row(
        types.InlineKeyboardButton(text='Reference', url=url)
    )
    return builder.as_markup()
```

`config.py`
```python
TOKEN = '8114200429:KAGpXZEN7IE4cS3YS5fOa0WpWvFH5W8Hatv'
```