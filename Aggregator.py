# aggregator.py

import threading
import time
import tempfile
from Imports import gspread
from Imports import datetime
from Imports import GoogleAuth
from Imports import GoogleDrive
from Imports import tb
from Imports import tb_types
from Imports import ServiceAccountCredentials
from StoragePaths import change_paths
from StoragePaths import ID_OF_GOOGLE_DRIVER_FOLDER
from StoragePaths import NAME_TABLE_TO_ACCEPT_CODES
from StoragePaths import NAME_TABLE_TO_SAVE_LOG
from StoragePaths import NAME_TABLE_TO_SAVE_USERS
from StoragePaths import NAME_TABLE_TO_DATABASE
from Code import download_codes
from Code import Code
from Dashboard import dashboard_for_users
from Dashboard import dashboard_for_hub
from Dashboard import dashboard_for_admin
from Dashboard import dashboard_for_tex
from Database import users_database
from Database import numeral
from Database import code_database
from Database import Member
from Database import Hub
from Database import bot_status
from Database import download_database
from Database import registration_enter
from Database import write_data
from Folder import upload_photo
from GoogleAttributes import scope
from GoogleAttributes import creds
from GoogleAttributes import client
from GoogleAttributes import sheet_users
from GoogleAttributes import sheet_secret_code
from GoogleAttributes import sheet_log
from GoogleAttributes import sheet_save_data
from Logging import logging
from Logging import get_current_time
import MessageSending
from ShiftOpeningAndClosing import open_shift
from TelegramAttributes import TOKEN
import os

bot = tb.TeleBot(TOKEN)
locker = threading.Lock()