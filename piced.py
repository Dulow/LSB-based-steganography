from PIL import Image
import numpy as np
import strtobit
import hashlib
import hmac
import des

def hideText(img, text):
	imgarr = np.array(img)
	text = addPad(text)
	bits = strtobit.strTobit(text)
	#print(bits)
	bits, vi = des.CBCE(bits)
	#print(bits)
	rows, cols, dims = imgarr.shape
	for i in range(len(bits)):
		bvlu = imgarr[int(i/cols), i%cols, 2]
		bbit = bin(bvlu)[2:].zfill(8)
		bcha = bbit[0:7] + bits[i]
		bcha = int(bcha, 2)
		imgarr[int(i/cols), i%cols, 2] = bcha

	mhmac = calHmac(text)
	#print(mhmac)
	bitslen = len(bits)
	for i in range(len(mhmac)):
		bvlu = imgarr[int((bitslen+i)/cols), (bitslen+i)%cols, 2]
		bbit = bin(bvlu)[2:].zfill(8)
		bcha = bbit[0:7] + mhmac[i]
		bcha = int(bcha, 2)
		imgarr[int((bitslen+i)/cols), (bitslen+i)%cols, 2] = bcha

	mhmaclen = len(mhmac)
	for i in range(len(vi)):
		bvlu = imgarr[int((bitslen+mhmaclen+i)/cols), (bitslen+mhmaclen+i)%cols, 2]
		bbit = bin(bvlu)[2:].zfill(8)
		bcha = bbit[0:7] + vi[i]
		bcha = int(bcha, 2)
		imgarr[int((bitslen+mhmaclen+i)/cols), (bitslen+mhmaclen+i)%cols, 2] = bcha

	img = Image.fromarray(imgarr)
	img.save('encrypt.png')

def calHmac(text):
	text = text.encode('utf-8')
	key = b'secret'
	h = hmac.new(key, text, digestmod = hashlib.sha256)
	hmhmac = h.hexdigest()
	#print(hmhmac)
	mhmac = bin(int(hmhmac, 16))[2:]
	mhmac = mhmac.zfill(256)
	return mhmac

def displayText(img, chiperlen):
	imgarr = np.array(img)
	rows, cols, dims = imgarr.shape
	chiperbits = ''
	for i in range(chiperlen):
		bvlu = imgarr[int(i/cols), i%cols, 2]
		bbit = bin(bvlu)[2:].zfill(8)
		bl = bbit[7]
		chiperbits += bl
	vi = ''
	for i in range(64):
		bvlu = imgarr[int((i+chiperlen+256)/cols), (i+chiperlen+256)%cols, 2]
		bbit = bin(bvlu)[2:].zfill(8)
		bl = bbit[7]
		vi += bl
	chiperbits = des.CBCD(chiperbits, vi)
	#print(chiperbits)
	chipertext = strtobit.bitTostr(chiperbits)
	#print(chipertext)
	#print(vi)
	if verifyHmac(chipertext, chiperlen, imgarr):

		return chipertext
	return 'ERROR'

def verifyHmac(chipertext, chiperlen, imgarr):
	rows, cols, dims = imgarr.shape
	verhmac = calHmac(chipertext)
	mhmac = ''
	for i in range(256):
		bvlu = imgarr[int((chiperlen+i)/cols), (chiperlen+i)%cols, 2]
		bbit = bin(bvlu)[2:].zfill(8)
		bl = bbit[7]
		mhmac += bl
	if mhmac == verhmac:
		return True
	return False

def addPad(text):
	while len(text)%8 != 0:
		text += ' '
	return text


if __name__ == '__main__':
	img = Image.open('heart.png')
	#strs = input('Please input text: ')
	strs = open('text.txt').read()
	hideText(img, strs)
	eimg = Image.open('encrypt.png')
	if len(strs)%8 != 0:
		slen = int(len(strs)/8+1) * 64
	else:
		slen = len(strs) * 8
	chipertext = displayText(eimg, slen)
	print(chipertext)
