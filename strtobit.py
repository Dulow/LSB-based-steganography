def strTobit(s):
	bits = ''
	for i in s:
		asc = ord(i)
		nbin = bin(asc)[2:]
		stabit = nbin.zfill(8)
		bits += stabit
	return bits

def bitTostr(b):
	strs = ''
	for i in range(int(len(b)/8)):
		temint = b[i*8:(i+1)*8]
		strs += chr(int(temint, 2))
	return strs
