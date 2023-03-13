import pandas as pd
# from sqlalchemy import creare_engine
# from datetime import datetime
# import mysql.connector
import random
import itertools
import numpy as np
import os

fpath = os.path.join(os.path.split(os.path.dirname(__file__))[0], "project_data\\")

df = pd.read_csv(fpath + 'MOCK_DATA.csv')



