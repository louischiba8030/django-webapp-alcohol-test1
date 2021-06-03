# 検温一覧の職員idリストから、'外来'の職員のidだけを抽出する
# Ryo Chiba
#
# Last update: 2021/06/03 (Thu.)

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
#from . import forms
#from app.forms import SampleChoiceForm
from django.template import loader

#import re
#from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pandas as pd
import itertools
import json
import datetime as dt

def index(request):
	template = loader.get_template('myapp2/index.html')

	df = get_gspread()
	context = {
		'msg' : 'Hellooo!',
		'al3f_table': df.to_html(),
	}

	return HttpResponse(template.render(context, request))

def get_gspread():
	api_scope = ['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']

	credentials_path = 'rock-strength-315100-d5df0ec350b2.json'
	credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, api_scope)
	gspread_client = gspread.authorize(credentials)

	ss_key = '1FkghGfcnL8ipY20Hl9K73z77RP4frHmmN4k9fxbMKoQ'
	wb = gspread_client.open_by_key(ss_key)
	data_sh = wb.worksheet('フォームの回答 1')

	# Get all values
	df = pd.DataFrame(data_sh.get_all_values())
	# Rename columns
	df.columns = ['タイムスタンプ', 'ID', '氏名', '手指消毒使用量']
	# Remove header
	df.drop([0], inplace=True)
	# Convert object to datetime
	df['タイムスタンプ'] = pd.to_datetime(df['タイムスタンプ'])
	print(df.dtypes)

	# Date range - 2021/05/01 ~ 2021/05/31
	#df = df[(df['タイムスタンプ'] >= dt.datetime(2021,5,1)) & (df['タイムスタンプ'] <= dt.datetime(2021,5,31))]
	df = df[df['タイムスタンプ'].dt.month == 5]

	return df
