import Aggregator

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Aggregator.ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = Aggregator.gspread.authorize(creds)

sheet_users = client.open(Aggregator.NAME_TABLE_TO_SAVE_USERS[0]).sheet1
sheet_log = client.open(Aggregator.NAME_TABLE_TO_SAVE_LOG[0]).sheet1
sheet_save_data = client.open_by_key(Aggregator.NAME_TABLE_TO_DATABASE[0]).sheet1
sheet_secret_code = client.open(Aggregator.NAME_TABLE_TO_ACCEPT_CODES[0]).sheet1
