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

def ajax_datatable(request):
	fd = {'xmonth': request.POST.get('xmonth'),
		'xloc_choice': request.POST.get('xloc_choice')
		}

	print("xmonth: ", fd['xmonth'])
	print("xloc: ", fd['xloc_choice'])

	# xmonth, xlocに合致する範囲のデータを抽出する
	# 
	# gspread -> df読み込み

	df = get_gspread()
	wsh_name = '抽出データ_' + fd['xmonth']
	print("wsh_name: ", wsh_name)

	context = {}
	return JsonResponse(context)

def ajax_post(request):
	form_data = {'xmonth': request.POST.getlist("xmonth"),
		'xloc_choice': request.POST.get('xloc_choice')
		}
	
	context = {"data": form_data}
	return JsonResponse(context)

def index(request):
	template = loader.get_template('myapp2/index.html')

	context = {
		'msg' : 'Hellooo!',
		#'al3f_table': df.to_html(),
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
	data_sh = wb.worksheet('抽出データ_2021年5月')

	# Get all values
	df = pd.DataFrame(data_sh.get_all_values())
	# remove rows[0, 1]
	df.drop([0, 1], inplace=True)
	# Rename columns
	df.columns = ['日付', 'ID', '氏名', '手指消毒使用量', '部署']
	df['日付'] = pd.to_datetime(df['日付'])

	#
	return df
