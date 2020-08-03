# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from os import listdir
from os.path import isfile, join
import random

from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from . forms import RegisterForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from . models import UserProfile
from django.contrib.auth.models import User


# path = "C:/Users/Mohit/Downloads/ForKritika/SoundFiles/"
path = "D:\Downloads\mysite (4)\mysite\static\SoundFiles"
vowels = [["0053", "he", "i", "he"], ["0054", "hih", "capital_i", "hid", "I"], ["0055","hay", "e", "hay"] , ["0057", "heh", "ԑ", "head"],
["0056","hah", "ᴂ", "had"], ["0059","haw", "a", "pot"], ["0058","huh", "ᴧ", "cut"], ["0063","hoe", "o", "hoe"], ["0060", "hu", "Ʊ", "hood", "ᶷ"], ["0061","who", "u", "who"]]


# Create your views here.

def get_words_count(request):
	words_count = request.GET.get('words_count')
	if words_count is None:
		return 0;
	return int(words_count)

def get_correct_count(request):
	correct_count = request.GET.get('correct_count')
	if correct_count is None:
		return 0;
	return int(correct_count)

def get_words_so_far(request):
	words_so_far = request.GET.get('words_so_far')
	if(words_so_far is None):
		return []
	words_so_far = words_so_far.split(",")
	words_so_far = [a.strip() for a in words_so_far]
	words_so_far = [x for x in words_so_far if x!='']
	if(len(words_so_far)>=len(get_words())):
		words_so_far = []
	return words_so_far


def index(request):
	print(request.user.is_authenticated, request.user)
	words_count = get_words_count(request)
	# print(words_count)
	correct_count = get_correct_count(request)
	words_so_far = get_words_so_far(request)
	if words_count == 20:
		return render(request, 'leaderboard.html', {'count': str(correct_count)})

	data = getword(words_so_far)
	data1 = get_files()
	# print(data1)
	words_so_far.append(data['word'])
	data["vowels"] =  vowels
	data["words_so_far"] =  words_so_far
	data['words_count'] = words_count
	data['correct_count'] = correct_count
	return render(request, 'index.html', data)

def getword(words_so_far):
	words = get_words()
	words = [f for f in words if f not in words_so_far ]
	word = random.choice(words)
	file_name = random.choice(get_sounds_for_word(word))
	responseData = {
		'word': word,
		'file_name': file_name
	}
	return responseData


def get_files():
	# print (listdir(path))
	files =  [f for f in listdir(path)]
	# print (type(files[0]))
	files = [f for f in files if ".mp3" in f]
	return files

def get_words():
	files = get_files();
	return list(set([file.split("_")[-1] for file in files]))

def get_sounds_for_word(word):
	files = get_files();
	filtered_files = [file for file in files if word in file]
	return filtered_files


class AjaxGetSoundFiles(generic.View):

	def post(self, *args, **kwargs):
		print("post", self.request.POST)
		word_list = self.request.POST.getlist('word_list')
		word_count = self.request.POST.get('word_count')
		return_dict = {'code': 1, 'status': 'success', 'response': {}}
		print("word_list", word_list)
		if not word_list:
			soundfiles = random.sample(listdir(path), int(word_count))
			sound_data = {}
			for i in soundfiles:
				# print (settings.STATIC_ROOT+'/static/SoundFiles/'+i)
				for n in vowels:
					if i.split('.')[0].split('_')[1] in n:
						sound_data[settings.STATIC_ROOT+'static/SoundFiles/'+i] = n
			return_dict['response'] = sound_data
			return JsonResponse(return_dict)
		else:
			soundfiles = listdir(path)
			soundfiles.remove('.DS_Store')
			print("soundfiles", soundfiles)
			sound_data = {}
			word_cnt = 0
			custom_vowel_list = []
			vowel_counter = 0
			# print(word_cnt, "word_cnt")
			for w in word_list:
				for q in vowels:
					if w in q:
						custom_vowel_list.append(q)
			print(custom_vowel_list, "custom")
			cust_vowel_cnt = len(custom_vowel_list)
			list_word_cnt = 0
			for i in soundfiles:
				# if word_cnt > int(word_count):
				# 	break
				if list_word_cnt == int(word_count):
					break
				print(custom_vowel_list[vowel_counter], "custom_vowel_list[vowel_counter]", i.split('.')[0].split('_')[1], "i.split('.')[0].split('_')[1]")
				# print(sound_data, "sound_data")
				if i.split('.')[0].split('_')[1] not in custom_vowel_list[vowel_counter]:continue
				sound_data[settings.STATIC_ROOT+'static/SoundFiles/'+i] = custom_vowel_list[vowel_counter]
				list_word_cnt += 1
				if vowel_counter == cust_vowel_cnt - 1:
					vowel_counter = 0
				else:
					print("else", vowel_counter, int(word_count) - 1)
					vowel_counter += 1
			return_dict['response'] = sound_data
			print(sound_data, "sound_data")
			return JsonResponse(return_dict)


class Register(generic.View):

	def get(self, *args, **kwargs):
		template = 'register.html'
		return render(self.request, template, {})

	def post(self, *args, **kwargs):
		if self.request.POST.get('password') != self.request.POST.get('conf_password'):
			messages.error(self.request, "Password and Confirm Password should be same")
			return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
		else:
			username = self.request.POST.get("username")
			password = self.request.POST.get("password")
			country = self.request.POST.get("country")
			language = self.request.POST.get("language")
			email = self.request.POST.get("email")
			print(password, "password")
			form = RegisterForm(self.request.POST)
			if form.is_valid():
				# user = form.save()
				user = User.objects.create_user(username=username, password=password, email=email)
				profile = UserProfile(user=user, country=country, first_language=language)
				profile.save()
				user = authenticate(username=username, password=password)
				if user is not None:
					# print("logines 1", user)
					login(self.request, user)
					messages.error(self.request, "Your registratin was successfull")
					# return redirect('index')
			else:
				print(form.errors)
				messages.error(self.request, "Your registratin was successfull")
			return redirect('index')


class Login(generic.View):

	def post(self, *args, **kwargs):
		print("logines")
		username = self.request.POST.get("username")
		password = self.request.POST.get("password")
		print(username, password)
		user = authenticate(username=username, password=password)
		if user is not None:
			print("logines 1", user)

			login(self.request, user)
			return redirect('index')
		else:
			print("logines 2")

			messages.error(self.request, "Invalid login credentials.")
			return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class Logout(generic.View):

	def get(self, *args, **kwargs):
			print("logouttt")
			logout(self.request)
			# messages.error(self.request, "Invalid login credentials.")
			return redirect('Register')
