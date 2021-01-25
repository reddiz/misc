import numpy as np
from PIL import Image

def encode(src, msg, stg, clor):
	img = Image.open(src)
	rgb = np.array(list(img.getdata()))
	w, h = img.size
	
	if img.mode == "RGB":
		n, m = 3, 0
	if img.mode == "RGBA":
		n, m = 4, 1
	
	total_pixels = rgb.size // n
	biner = ''.join([format(ord(i), "08b") for i in msg])
	req_size = len(biner)
	#print rgb
	
	if req_size < total_pixels:
		print "padding message binary..."
		for i in range(total_pixels - req_size):
			biner += "0"
		print "done, message length: %d" % len(biner)
	else:
		print "Error! Please provide bigger image or reduce message!"

	limit = 0
	count = 0
	
	print "encoding image..."
	for p in range(total_pixels):
		for q in range (0, 3):
			if limit < req_size:
					if clor == q:
						rgb[p][q] = rgb[p][q] ^ int(biner[limit])
						limit += 1
					else:
						rgb[p][q] = rgb[p][q] ^ 1
	print "message encoded successfully"
	print "creating and saving stego image..."
	#print rgb
	rgb = rgb.reshape(h, w, n)
	im = Image.fromarray(rgb.astype("uint8"), img.mode)
	im.save(stg)
	print "done."

def decode(src1, src2):
	img1 = Image.open(src1)
	img2 = Image.open(src2)
	rgb1 = np.array(list(img1.getdata()))
	rgb2 = np.array(list(img2.getdata()))
	
	if img1.mode == img2.mode:
		if img1.mode == "RGB":
			n, m = 3, 0
		if img1.mode == "RGBA":
			n, m = 4, 1
	
	tp1 = rgb1.size // n
	tp2 = rgb2.size // n
	if tp1 == tp2:
		total_pixel = tp1
	
	#hidden = ""
	r = g = b = ""
	for p in range(total_pixel):
		for q in range(0, 3):	
			#hidden += (bin(rgb1[p][q] ^ rgb2[p][q]))[2:]
			if q == 0:
				r += (bin(rgb1[p][q] ^ rgb2[p][q]))[2:]
			if q == 1:
				g += (bin(rgb1[p][q] ^ rgb2[p][q]))[2:]
			if q == 2:
				b += (bin(rgb1[p][q] ^ rgb2[p][q]))[2:]
	
	#hidden = [hidden[i:i+8] for i in range(0, len(hidden), 8)]
	r = [r[i:i+8] for i in range(0, len(r), 8)]
	g = [g[i:i+8] for i in range(0, len(g), 8)]
	b = [b[i:i+8] for i in range(0, len(b), 8)]

	#message = ""
	mr = mg = mb = ""
	for i in r:
		mr += chr(int(i, 2))
	for j in g:
		mg += chr(int(j, 2))
	for b in g:
		mb += chr(int(b, 2))
	#print message
	f = open("tes_png.txt", "a")
	f.write("this is message in red\n" + mr + "\n")
	f.write("this is message in green\n" + mg + "\n")
	f.write("this is message in blue\n" + mb + "\n")
	f.close()

#encode("ori1.jpg", "Halo! Selamat mengerjakan UAS!", "stego_tes.jpg", 0)
decode("74-data1.jpg", "gambar1pesan.tiff")

"""
standard one component xor encode
if req_size > total_pixels:
		print "Error! Please provide bigger image or reduce message!"
	else:
		limit = 0
		for p in range(total_pixels):
			for q in range(m,n):
				if limit < req_size:
					if clor == q:
						rgb[p][q] = rgb[p][q] ^ int(biner[limit])
						limit += 1
					else:
						pass			
				else:
					break
					
					when turned into JPG, even though the changes should be stopped after the message has 
					been fully iterated, some RGB values are still changing due to the lossy nature of JPG.
					
"""