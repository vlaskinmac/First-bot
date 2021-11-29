# First-bot

**Notifications about the status of completed work.**


This script is written as part of the task of the courses [Devman](https://dvmn.org).


## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Python Version

Python 3.6 and newer.

### Installing

To install the software, you need to install the dependency packages from the file: **requirements.txt**.

Perform the command:

```

pip3 install -r requirements.txt

```

## Getting API key

**API key Devman**

- To get the API key. You need to follow the link: [Devman](https://dvmn.org).
- Enter the API key in the HTTP header:

```python
headers = {'Authorization': 'Your API key'}

```

**API key Telegram bot**

- Go to Telegram. 
- Call the system bot by typing in the search: [@BotFather](https://telegram.me/BotFather) 
- Enter the command:
```
/token
```


### Connecting the API key

You need to create a `.env` file and write all sensitive data into it, like this:

```python
API_KEY_DEVMAN="772a05d39ec46fdac5be4ac7be45f3"
API_KEY_BOT="2127492642:AAFC4-Ey3WTtFNCcSzbDN7Z7y1ePaw8IbTU"
CHAT_ID=-1001647060957
```

## Launch code


```python
$ python my_bot.py 
```



## Authors

**vlaskinmac**  - [GitHub-vlaskinmac](https://github.com/vlaskinmac/)
