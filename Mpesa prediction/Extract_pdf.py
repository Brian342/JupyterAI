import pandas as pd
import numpy as np
import PyPDF2
import pikepdf
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from tabula.io import read_pdf
from dateutil import parser
from sqlalchemy import create_engine
import mysql.connector