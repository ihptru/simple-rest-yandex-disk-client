#!/usr/bin/python3
import random
import string
import sys
import os
import re
import urllib.request
import requests
import time

from src.YandexDiskException import YandexDiskException
from src.YandexDiskRestClient import YandexDiskRestClient

class MakeBackup:
	def __init__(self):
		token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa_change_it"
		self.client = YandexDiskRestClient(token)

	def get_disk_metadata(self):
		try:
			disk = self.client.get_disk_metadata()
			print("total space of disk = " + str(disk.total_space))
			print("used spase of disk = " + str(disk.used_space))
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")

	def creating_of_folder(self, dirname):
		try:
			self.client.create_folder(dirname)
			print(dirname + "/ was created on Yandex.Disc")
		except YandexDiskException as exp:
			#print(exp)
			#print("--- Skipping step ---")
			pass

	def get_meta_of_element(self, element_path):
		try:
			element = self.client.get_content_of_folder(element_path)
			#print("Name of an element is " + element.name)
			return True
		except YandexDiskException as exp:
			return False

	def remove_folder_or_file(self, element_path):
		try:
			self.client.remove_folder_or_file(element_path)
			print(element_path + " was successfully removed.")
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")

	def copy_folder_or_file(self, element_path, into_path):
		try:
			self.client.copy_folder_or_file(element_path, into_path)
			print(
				"Element " + element_path + " was copied to " + into_path)
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")

	def move_folder_or_file(self, element_path, into_path):
		try:
			self.client.move_folder_or_file(element_path, into_path)
			print(
				"Element " + element_path + " was moved to " + into_path)
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")

	def get_download_link_to_file(self, element_path):
		try:
			link = self.client.get_download_link_to_file(element_path)
			print("Download link to the file "+element_path+" is " + link["href"])
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")

	def get_published_files(self):
		try:
			files = self.client.get_published_elements()
			print("There are " + str(len(files)) + " published files.")
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")

	def get_public_link_to_folder_or_file(self, element_path):
		try:
			public_link = self.client.get_public_link_to_folder_or_file(element_path)
			print("Public link to the file "+element_path+" is " + public_link)
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")

	def unpublish_folder_or_file(self, element_path):
		try:
			self.client.unpublish_folder_or_file(element_path)
			print("From this point on, there is no a public link to " + element_path)
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")

	def get_list_of_all_files(self):
		try:
			files = self.client.get_list_of_all_files()
			print("There are " + str(len(files)) + " files in this Yandex.Disk")
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")

	def upload_file_from_url(self, url, element_path):
		try:
			self.client.upload_file_from_url(url, element_path)
			print("\n----------------------")
			print("File " + url + " was uploaded to " + element_path)
			print("----------------------")
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")

	def upload_file(self, path_from, element_path):
		try:
			self.client.upload_file(path_from, element_path)
			print("\n----------------------")
			print("Local file " + path_from + " was uploaded to " + element_path + " on Yandex.Disc")
			print("----------------------")
		except YandexDiskException as exp:
			print(exp)
			print("--- Skipping step ---")


def main():

	yandex = MakeBackup()
	print("----------------------")
	yandex.get_disk_metadata()
	print("----------------------\n")


	# Local Backup
	yandex.creating_of_folder('/backups')
	yandex.creating_of_folder('/backups/ruweb')
	
	_data = os.listdir('/backups/data/fetch-site-backups.ihptru.net/www/ruweb/')
	for _file in _data:

		if not yandex.get_meta_of_element('/backups/ruweb/' + _file):	# File does not exist on Yandex.Disc

			yandex.upload_file_from_url('http://fetch-site-backups.ihptru.net/ruweb/' + _file, '/backups/ruweb/' + _file)
			time.sleep(600)

		else:
			print("\n----------------------")
			print("File " + _file + " exists on Yandex.Disc. Skipping...")
			print("----------------------")
		
		os.remove('/backups/data/fetch-site-backups.ihptru.net/www/ruweb/' + _file)
		print("\n----------------------")
		print("Removed /backups/data/fetch-site-backups.ihptru.net/www/ruweb/" + _file + " from Local Disc")
		print("----------------------")



	# Download backups from remote site and upload them to Yandex.Disc

	yandex.creating_of_folder('/backups')
	yandex.creating_of_folder('/backups/baxxster')
	yandex.creating_of_folder('/backups/baxxster/openra')

	data = urllib.request.urlopen('http://fetch-site-backups.openra.net').read().decode('utf-8')
	
	regex = re.compile('href="(.*?)"')
	remote_files =regex.findall(data)

	for remote_f in remote_files:
		if remote_f == '../':
			continue

		print("\n\n\n**********************")
		print("**********************")

		if not yandex.get_meta_of_element('/backups/baxxster/openra/' + remote_f):

			response = urllib.request.urlopen('http://fetch-site-backups.openra.net/' + remote_f)
			CHUNK = 16 * 1024
			with open("/backups/data/fetch-site-backups.ihptru.net/www/baxxster/" + remote_f, 'wb') as f:
				while True:
					chunk = response.read(CHUNK)
					if not chunk: break
					f.write(chunk)

			print("\n----------------------")
			print("Downloaded remote file to /backups/data/fetch-site-backups.ihptru.net/www/baxxster/" + remote_f)
			print("----------------------")

			time.sleep(5)
			yandex.upload_file_from_url('http://fetch-site-backups.ihptru.net/baxxster/' + remote_f, '/backups/baxxster/openra/' + remote_f)
			time.sleep(600)

			os.remove('/backups/data/fetch-site-backups.ihptru.net/www/baxxster/' + remote_f)
			print("\n----------------------")
			print("Removed /backups/data/fetch-site-backups.ihptru.net/www/baxxster/" + remote_f + " from Local Disc")
			print("----------------------")

		else:
			print("\n----------------------")
			print("File " + remote_f + " exists on Yandex.Disc. Skipping...")
			print("----------------------")




if __name__ == "__main__":
	main()