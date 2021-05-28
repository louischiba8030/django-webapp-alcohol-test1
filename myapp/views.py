from django.shortcuts import render
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pandas as pd
import itertools

def get_alsum(xid):
	al_sum = data_df.loc[data_df['ID'] == xid, '手指消毒使用料(単位：ml)'].astype(int).sum()

	return al_sum

def gspread_al_read():
	api_scope = ['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']

	credentials_path = 'rock-strength-315100-d5df0ec350b2.json'
	credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, api_scope)
	gspread_client = gspread.authorize(credentials)

	ss_key = '1FkghGfcnL8ipY20Hl9K73z77RP4frHmmN4k9fxbMKoQ'
	wb = gspread_client.open_by_key(ss_key)
	wsh = wb.worksheet('職員id一覧')
	data_sh = wb.worksheet('抽出データ_2021年5月')

	# Rename columns
	df = pd.DataFrame(wsh.get_all_values())
	df.columns = list(df.loc[0, :])
	df.drop(0, inplace=True)
	df.reset_index(inplace=True)
	df.drop('index', axis=1, inplace=True)

	# Extract data
	xloc = '外来'
	df = df.query('所属部署 == @xloc').iloc[:, [0, 1, 2, 4]]

	## Rename columns
	data_df = pd.DataFrame(data_sh.get_all_values())
	# Remove Row "1"
	data_df = data_df.drop(data_df.index[[0]])
	# Get Row (2) = New Column names
	new_columns = list(itertools.chain.from_iterable(data_df[:1].values.tolist()))
	new_columns[1:3] = ["ID", "氏名"]
	data_df.columns = new_columns
	data_df = data_df.drop(data_df.index[[0]])

	# Append 'E' column: '手指消毒使用量合計'
	#毒使用量合計'] = df.iloc[:, 0].values.tolist()
	id_list = df.iloc[:, 0].values.tolist()
	alsum_values = map(lambda x: get_alsum(x), id_list)
	df['手指消毒使用量'] = list(alsum_values)

	context = {
		'al_table': df.to_html()
	}

	return render(request, 'myapp/index.html', context)
