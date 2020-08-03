# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from os import listdir
from os.path import isfile, join
import random
from random import shuffle

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
def index(request):
	return render(request, 'index.html', {})


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
			shuffle(word_list)
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
					return redirect('index')
			else:
				print(form.errors)
				messages.error(self.request, form.errors)
				return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

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
			messages.error(self.request, "You have successfully logined.")
			return redirect('index')
		else:
			print("logines 2")

			messages.error(self.request, "Invalid login credentials.")
			return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class Logout(generic.View):

	def get(self, *args, **kwargs):
			print("logouttt")
			logout(self.request)
			messages.error(self.request, "You have successfully logged out.")
			return redirect('Register')
