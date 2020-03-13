import ctypes
import os,msvcrt
import time
import random as random
import ctypes
from ctypes import wintypes
import sys


class Image():
	
	def __init__(self, image_path):
		self.image_path = image_path
		self.image_name = self.image_path.split("\\")[-1].title()
		self.selected = False
	
	def has_image_selected(self):
		return self.selected


current_directory = os.path.dirname(os.path.realpath(__file__))

def checkIfAddressExists(path):
	system_registry = 'master.txt'
	return system_registry in os.listdir(path)


def add_gallery(gallery_name):
	directory = current_directory+"\master.txt"	#append file location into master.txt 
	files = os.listdir(current_directory)

	if "master.txt" in files:
		gallery_list = []
		with open(directory, 'r') as f_obj:
			gallery_list = f_obj.readlines()
			f_obj.close()
		with open(directory, 'w') as f:
			for i in gallery_list:
				f.write(i)
			f.write(gallery_name+"\n")
			f.close()
		print('Added', gallery_name, 'to list of galleries available')
	else:
		with open(directory, 'w') as f_obj:
			f_obj.write(gallery_name+"\n")
		print('...created master.txt file for organising gallery locations')
		print('Added', gallery_name, 'to list of galleries available')


def address_exists(address):
	return os.path.isdir(address)


def contains_images(gallery_address):
	files = os.listdir(gallery_address)
	for file in files:
		if is_image_file_extension(file):
			return True
	return False


def develop_galleries():
	while True:
		gallery_response = input('Enter gallery address: ')
		if address_exists(gallery_response.strip()) and contains_images(gallery_response.strip()):
			#add gallery
			add_gallery(gallery_response.strip())
			break
		else:
			print('Please enter an adress that exists & contains images')


def folderList(address):
	return os.listdir(address)


def listOfGalleries():
	list_of_galleries = []
	with open(current_directory+"\master.txt", 'r') as galleries:
		folders = galleries.readlines()
		for gallery in folders:
			s = gallery[:-1]
			list_of_galleries.append(s+"\\")
	return list_of_galleries


def choose_slideshow():
	#get list of addresses
	galleries = listOfGalleries()
	print('\n-----------Galleries-----------\n')
	for index in range(0, len(galleries)):
		print("["+str(index+1)+"]", galleries[index].split('\\')[-2])


	#get integer response from user
	while True:
		print('-------PLEASE CHOOSE ONE OF THE GALLERIES ABOVE-------')
		response = input('Enter index number to choose: ')
		response = response.strip()
		if not (response.isalpha()):
			if not ( int(response)-1 > len(galleries) or int(response)-1 < 0):
				choosen_gallery_address = galleries[int(response) - 1]
				return choosen_gallery_address
			else:
				print('Please choose within the range provided', 1,"<->",len(galleries))
		else:
			print('please only enter numbers')


def choose_play_time():
	while True:
		response = input('Enter play time of each wallpaper: ')
		response = response.strip()
		if not response.isalpha():
			return int(response)*60


def play_slideshow(gallery, transistion_time):
	user_response = ''
	current_time = time.time()
	print('Press [q] to quit\n[n] to skip current wallpaper.\nPress [b] to return back to menu')
	while True and user_response.strip() != 'q':
		user_response = str(msvcrt.getwch()).strip().lower()
		if user_response == 'n' or  time.time() - current_time > transistion_time:
			current_time = change_image(gallery)
			print('Press [q] to quit\n[n] to skip current wallpaper.\nPress [b] to Back to Menu')
		elif user_response == 'q':
			return 'Stop'
		elif user_response == 'c':
			return 'Change Library'
		elif user_response =='a':
			return 'Add gallery'


used = []

def is_image_file_extension(filepath):
	file_extension = filepath.split(".")[-1].strip().lower()
	if file_extension in 'jpeg,png,jpg,bmp':
		return True

def random_mizer(address, pictures_used):
	print('used', used)
	images = folderList(address)
	new_images = []
	for image in images:
		if image not in used and is_image_file_extension(image):
			new_images.append(image)
	if len(new_images) == 0:	#all images used
		del used [:]
		for image in images:
			if is_image_file_extension(image):
				new_images.append(i)
	pictures_used.append(new_images.pop())
	
	#TODO add shuffle functionality after all images used.
	return pictures_used[-1]


def change_image(gallery):
	wallpaper_bmp = random_mizer(gallery, used)
	drive = gallery
	image = wallpaper_bmp
	image_path = os.path.join(drive, image)

	SPI_SETDESKWALLPAPER  = 0x0014
	SPIF_UPDATEINIFILE    = 0x0001
	SPIF_SENDWININICHANGE = 0x0002

	user32 = ctypes.WinDLL('user32')
	SystemParametersInfo = user32.SystemParametersInfoW
	SystemParametersInfo.argtypes = ctypes.c_uint,ctypes.c_uint,ctypes.c_void_p,ctypes.c_uint
	SystemParametersInfo.restype = wintypes.BOOL
	print(SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE))
	now = time.time()
	return now


def run_program():
	gallery = choose_slideshow()
	time = choose_play_time()
	reply = play_slideshow(gallery, time)
	return reply


def menu():
	options = ['slideshow', 'Add Gallery', 'Quit']
	for option in range(0, len(options)):
		print("["+str(option+1)+"]",options[option])
	choice = 1
	while True:
		print('Choose an option by enter')
		response = input('Enter index: ')
		if not response.isalpha():
			if not (int(response) - 1 > len(options) or int(response)-1 <0):
				choice = int(response)-1
				break
	if choice == 1:
		develop_galleries()
		return True
	elif choice == 0:
		return True
	elif choice == 2:
		return False


def updateMaster():
	galleries = listOfGalleries()
	noneValidAddress = False
	listOfValidAddresses = []
	for gallery in galleries:
		if not os.path.isdir(gallery):
			noneValidAddress = True
		else:
			listOfValidAddresses.append(gallery)
	if(noneValidAddress):
		with open(current_directory+"\master.txt", 'w') as f:
			for i in  listOfValidAddresses:
				f.write(i+"\n")



def system():
	new_system = checkIfAddressExists(current_directory)
	if new_system == False:
		print('developing address...')
		develop_galleries()
	else:
		updateMaster()
	returned = menu()
	if not returned == False:
		user_response = run_program()
		if user_response == 'Change Library':
			#loop over again
			system()


system()
