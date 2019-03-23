import requests
import base64
import os

from json import loads
from requests import Response

from sanic import Sanic
from sanic.response import json
from sanic.log import logger
from sanic_cors import CORS

from parser import InstagramScrap

class ParsingServer(Sanic):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Potentially we would want to limit not only IP but also origin to be
    # google datastudio, TODO figure out proper origins
    CORS(self)
    self.add_route(self.index, '/')
    self.add_route(self.parse_followers, '/api/parse-followers/<username>', methods=['POST'])

  async def index(self, request):
    return json({'message': 'Welcome to the internet, let me be your guide'})

  async def parse_followers(self, request):
    user_data = request.json
    bot = InstagramScrap(user_data['username'], user_data['password'])

    bot.auth()
    followers = bot.get_user_followers(user_data['username'], 20)
    followers_dict = {}

    for follower in followers:
      followers_dict[follower] = bot.get_followers_count(follower)
      
    return json(followers_dict)

env = os.environ.get("APP_ENV", "dev")
logger.info('Starting application in {env} mode')
app = ParsingServer()