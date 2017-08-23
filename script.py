import ctypes
import os,msvcrt
import time
import random as random
import ctypes
from ctypes import wintypes

print('Only bmp, jpg, and png files used.')
print('Do not add double \\\\ only keep it like so \\')
temp = input('Enter location of Wallpapers!: ')
number_of_goes = '0'
while  number_of_goes.isalpha() or int(number_of_goes) < 1:
	number_of_goes = input('Please enter the wait time before the wallpaper changes\nIn minutes: ')

iterate = int(number_of_goes)
string = ''
i = 0
while i < len(temp):
	if temp[i] != temp[-1] and (temp[i] == "\\" and temp[i+1] != "\\"):
		string+="\\"
	else:
		string+=temp[i]
	i+=1
if string[-1] != "\\":
	string+="\\"
print('Current Directory is: |'+string+'|')


wallpaper_folder = string

my_pics = []

def check_again():
	temp_files = os.listdir(wallpaper_folder)
	del my_pics [:]
	for i in temp_files:
		if i[-3:] == 'bmp' or i[-3:] == 'jpg' or i[-3:] == 'png':
			my_pics.append(i)
	print(my_pics)



used = []
def random_mizer():
	check_again()
	print(my_pics)
	size = len(my_pics)
	use = ''
	found = False
	if len(used) == len(my_pics):
		print('---')
		del used[:]
	while found == False:
		if my_pics[random.randint(0,size-1)] not in used:
			use = my_pics[random.randint(0,size-1)]
			used.append(use)
			found = True

	return use

twenty_five = iterate*60
now = time.time()
print(now)
while True:
	result= False
	test_a = time.time()
	if msvcrt.kbhit():
		inp = msvcrt.getch()
		if inp != '':
			result = True
	elif time.time() - test_a > 5:
		print(':p')
	if time.time() - now> twenty_five or result == True:
		wallpaper_bmp = random_mizer()
		print('Current picture: '+wallpaper_bmp)
		drive = wallpaper_folder
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
		print('End')
		now = time.time()
		print('Press any key to skip wallpaper\nif not then do not press anything.')
