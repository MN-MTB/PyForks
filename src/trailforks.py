import pandas as pd
import os
import requests
import urllib.parse
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import as_completed, ThreadPoolExecutor

class Trailforks:

    def __init__(self, region=None, username=None, trailforks_cookie=None):
        self.name = "trailforks"
        self.region = region
        self.username = username
        self.cookie = trailforks_cookie

    def uri_encode(self, string: str) -> str:
        return urllib.parse.quote(string)
    
