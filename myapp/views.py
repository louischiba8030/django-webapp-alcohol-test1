# 検温一覧の職員idリストから、'外来'の職員のidだけを抽出する
# Ryo Chiba
#
# Last update: 2021/05/28 (Fri.)
# Date: 2021/05/28 (Fri.)

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from . import forms
#from app.forms import SampleChoiceForm
from django.template import loader

import re
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pandas as pd
import itertools
import json

def get_alsum(data_df, xid):
	al_sum = data_df.loc[data_df['ID'] == xid, '手指消毒使用料(単位：ml)'].astype(int).sum()

	return al_sum

def index(request):
	template = loader.get_template('myapp/index.html')
	context = {}
	return HttpResponse(template.render(context, request))
	#return render(request, "myapp/index.html")

def ajax_test(request):
	# 部署選択プルダウンの値を取得
	x_choice = request.POST.get('xlocc', None)
	print("#DEBUG#")

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
	df = df.query('所属部署 == @x_choice').iloc[:, [0, 1, 2, 4]]

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
	alsum_values = map(lambda x: get_alsum(data_df, x), id_list)
	df['手指消毒使用量'] = list(alsum_values)
	
	# Choice
	#choices = forms.SampleChoiceForm()

	context = {
		'al_table': df.to_html(),
		#'choices': choices,
		#'location': x_choice,
	}

	#return render(request, 'myapp/index.html', context)
	data = {"data": df.to_dict(orient='records')}
	#json_data = json.dumps(data)
	print("json_data: ", data)
	#data = {'data': df.to_json(orient='values', force_ascii=False)}
	return JsonResponse(data)
	#response = HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
	#print("res: ", response)
	#return response
