import os
import requests
import sys
from bs4 import BeautifulSoup
import getopt
import urllib2
import random
import re
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import time

proxyUser = os.environ['PROXY_USER']
proxyPass = os.environ['PROXY_PASS']
