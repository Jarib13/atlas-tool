import cv2
import sys
import argparse
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
from colorama import Fore, Back, Style

def main():
	parser = argparse.ArgumentParser(description='dogmetes')
	parser.add_argument('--cool', action='store_const', const=True, default=False)
	parser.add_argument('-i', '--input', required=True)
	parser.add_argument('-o', '--output', required=True)
	parser.add_argument('-w', '--width')
	parser.add_argument('-p', '--padding')
	parser.add_argument('-t', '--tilesize', required=True)
	parser.add_argument('-s', '--split_height')
	parser.add_argument('-l', '--split_tilesize')

	args = parser.parse_args(sys.argv[1:])


	input_file = Image.open(args.input)
	input = np.array(input_file)

	input_width = input.shape[0]
	input_height = input.shape[1]
	output_width = input_width
	output_height = input_height


	tile_size = int(args.tilesize)
	tiles_width = int(input_width/tile_size)
	tiles_height = int(input_height/tile_size)


	padding = int(tile_size / tiles_width)

	if args.padding != None:
		padding = int(args.padding)

	halfpad = int(padding / 2)

	output = np.zeros(input.shape, dtype=np.uint8)


	truncated = False

	os.system('color')
	print(Fore.LIGHTCYAN_EX + 'Padding atlas \'{image}\' with {padding} pixels per tile'.format(image=args.input, padding=padding) + Fore.RESET)


	repeat = halfpad

	if args.split_height != None:
		tiles_height = int(args.split_height)

	for tx in range(tiles_width):
		for ty in range(tiles_height):
			x = tx * tile_size
			y = ty * tile_size

			x2 = halfpad + tx * (tile_size + padding)
			y2 = halfpad + ty * (tile_size + padding)

			if (x2+tile_size < output_width and y2+tile_size < output_height):
				#copy tile
				output[y2:y2+tile_size,x2:x2+tile_size,:] = input[y:y+tile_size,x:x+tile_size,:]

				#copy edge and repeat 
				output[y2:y2+tile_size,x2+tile_size:x2+tile_size+repeat] = np.repeat(input[y:y+tile_size,x+tile_size-1:x+tile_size], repeat, axis=1)
				output[y2+tile_size:y2+tile_size+repeat,x2:x2+tile_size] = np.repeat(input[y+tile_size-1:y+tile_size,x:x+tile_size], repeat, axis=0)
				output[y2:y2+tile_size,x2-repeat:x2] = np.repeat(input[y:y+tile_size,x:x+1], repeat, axis=1)
				output[y2-repeat:y2,x2:x2+tile_size] = np.repeat(input[y:y+1,x:x+tile_size], repeat, axis=0)

				#copy corner and repeat^2
				output[y2-repeat:y2,x2+tile_size:x2+tile_size+repeat] = np.repeat(input[y:y+1,x+tile_size-1:x+tile_size], repeat*repeat, axis=0).reshape(repeat, repeat, -1)
				output[y2+tile_size:y2+tile_size+repeat,x2-repeat:x2] = np.repeat(input[y+tile_size-1:y+tile_size,x:x+1], repeat*repeat, axis=0).reshape(repeat, repeat, -1)
				output[y2-repeat:y2,x2-repeat:x2] = np.repeat(input[y:y+1,x:x+1], repeat*repeat, axis=0).reshape(repeat, repeat, -1)
				output[y2+tile_size:y2+tile_size+repeat,x2+tile_size:x2+tile_size+repeat] = np.repeat(input[y+tile_size-1:y+tile_size,x+tile_size-1:x+tile_size], repeat*repeat, axis=0).reshape(repeat, repeat, -1)

			else:
				truncated = True


	#post split

	if args.split_height != None:
		#split_height_pixel_offset = halfpad + int(args.split_height-1) * (tile_size + padding) + tile_size + halfpad
		split_height_pixel_offset = int(args.split_height) * (tile_size + padding)
		print(Fore.LIGHTCYAN_EX + 'Split atlas at {height} px'.format(height=split_height_pixel_offset) + Fore.RESET)
		split_height_pixel_offset_input = int(args.split_height) * (tile_size)

		tile_size = int(args.split_tilesize)
		tiles_width = int(input_width/tile_size)
		tiles_height = int((input_height - split_height_pixel_offset) / tile_size)

		for tx in range(tiles_width):
			for ty in range(tiles_height):
				x = tx * tile_size
				y = ty * tile_size + split_height_pixel_offset_input

				x2 = halfpad + tx * (tile_size + padding)
				y2 = halfpad + ty * (tile_size + padding) + split_height_pixel_offset

				if (x2+tile_size < output_width and y2+tile_size < output_height):
					#copy tile
					output[y2:y2+tile_size,x2:x2+tile_size,:] = input[y:y+tile_size,x:x+tile_size,:]

					#copy edge and repeat 
					output[y2:y2+tile_size,x2+tile_size:x2+tile_size+repeat] = np.repeat(input[y:y+tile_size,x+tile_size-1:x+tile_size], repeat, axis=1)
					output[y2+tile_size:y2+tile_size+repeat,x2:x2+tile_size] = np.repeat(input[y+tile_size-1:y+tile_size,x:x+tile_size], repeat, axis=0)
					output[y2:y2+tile_size,x2-repeat:x2] = np.repeat(input[y:y+tile_size,x:x+1], repeat, axis=1)
					output[y2-repeat:y2,x2:x2+tile_size] = np.repeat(input[y:y+1,x:x+tile_size], repeat, axis=0)

					#copy corner and repeat^2
					output[y2-repeat:y2,x2+tile_size:x2+tile_size+repeat] = np.repeat(input[y:y+1,x+tile_size-1:x+tile_size], repeat*repeat, axis=0).reshape(repeat, repeat, -1)
					output[y2+tile_size:y2+tile_size+repeat,x2-repeat:x2] = np.repeat(input[y+tile_size-1:y+tile_size,x:x+1], repeat*repeat, axis=0).reshape(repeat, repeat, -1)
					output[y2-repeat:y2,x2-repeat:x2] = np.repeat(input[y:y+1,x:x+1], repeat*repeat, axis=0).reshape(repeat, repeat, -1)
					output[y2+tile_size:y2+tile_size+repeat,x2+tile_size:x2+tile_size+repeat] = np.repeat(input[y+tile_size-1:y+tile_size,x+tile_size-1:x+tile_size], repeat*repeat, axis=0).reshape(repeat, repeat, -1)

				else:
					truncated = True

	output_file = Image.fromarray(output)
	output_file.save(args.output)

	if truncated:
		print(Fore.LIGHTMAGENTA_EX + 'WARNING: output truncated' + Fore.RESET)



main()