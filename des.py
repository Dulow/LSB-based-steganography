import random

ripm = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,
		  	36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]

'''def getPRGB():
	prgb = []
	img = Image.open('cfire.png')
	w, h = img.size
	pixels = img.load() 
	for i in range(w):
		for j in range(h):
			p = pixels[i,j]
			prgb.append(p[0])
			prgb.append(p[1])
			prgb.append(p[2])
	#print(prgb)
	return prgb,w,h
def SD():
	#f = open('cj.txt', 'r')
	#s = f.read()
	#s = [12, 34, 45, 53, 23, 23, 23, 54, 65, 23, 54, 32, 21, 87, 100, 65]
	#s = [72, 75, 3, 139, 185, 121, 100, 79, 29, 193, 60, 225, 136, 182, 56, 86]
	s,w,h = getPRGB()
	sb = []
	for i in s:
		ssb = str(bin(i))[2:]
		ssb = ssb.zfill(8)
		sb.append(ssb)
	mgn = int(len(sb) / 8)
	#print(mgn)
	mg = []
	for i in range(mgn):
		temmg = ''
		for j in range(8):
			temmg += sb[i*8+j]
		mg.append(temmg)
	#print(mg)
	cg = []
	for i in mg:
		temcg = D(i)
		cg.append(temcg)
	#print(cg)
	cd = []
	for i in cg: 
		for j in range(8):
			temint = i[j*8:(j+1)*8]
			#print(temint)
			cd.append(int(temint, 2))
	cd.append(s[mgn*8:])
	#print(cd)
	return cd,w,h

def cPic():
	cd,w,h = SD()
	#print(cd)
	img = Image.new('RGB', (w,h), (0, 0, 0))
	num = 0
	for i in range(w):
		for j in range(h):
			#print(num)
			img.putpixel([i,j], (cd[num], cd[num+1], cd[num+2]))
			#print(cd[num], cd[num+1], cd[num+2])
			num += 3

	pixels = img.load()
	p = pixels[0,0]
	print(p[0], p[1], p[2])
	img.save('mfire.png')
	cimg = Image.open('cpic.png')
	pixels = cimg.load()
	p = pixels[0,0]
	print(p[0], p[1], p[2])


	
	
	cdb = ''
	for i in cd:
		temmd = chr(i)
		cdb += temmd
	print(cdb)
	f = open('m.txt', 'w')
	f.write(str(cdb.encode('utf-8')))'''



def CK():	
	ik = '0011000100110010001100110011010000110101001101100011011100111000'
	#ik = input('Please input plaintext: ')
	ip1m = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,
			63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
	ip2m = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,
			41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
	rl = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
	ks = []
	ip = ''
	for i in ip1m:
		ip += ik[i-1]
	c0 = ip[0:28]
	d0 = ip[28:56]
	rlsum = 0
	for i in rl:
		rlsum += rl[i]
		cn = c0[rlsum:28] + c0[0:rlsum]
		dn = d0[rlsum:28] + d0[0:rlsum]
		kn = cn + dn
		k = ''
		for j in ip2m:
			k += kn[j-1]
		ks.append(k)

	return ks
def IP(m):
	#m = '0011000000110001001100100011001100110100001101010011011000110111'
	ipm = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
		   57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]

	ip = ''
	for i in ipm:
		ip += m[i-1]

	return ip

def E(m):	
	ip = IP(m)
	ks = CK()
	l0 = ip[0:32]
	r0 = ip[32:64]
	lf = l0
	rf = r0
	for i in ks[0:15]:
		f = F(rf, i)
		rn = XOR(lf, f)
		ln = rf
		rf = rn
		lf = ln
	rn = XOR(lf, F(rf, ks[15]))
	ln = rf
	cf = rn + ln
	c = ''
	for i in ripm:
		c += cf[i-1]
	#print('Ciphertext: ', c)

	return c

def D(c):
	ip = IP(c)
	ks = CK()
	l0 = ip[0:32]
	r0 = ip[32:64]
	lf = l0
	rf = r0
	mark = 15
	while True:
		if mark == 0:
			break
		f = F(rf, ks[mark])
		rn = XOR(lf, f)
		ln = rf
		rf = rn
		lf = ln
		mark -= 1
	rn = XOR(lf, F(rf, ks[0]))
	ln = rf
	mf = rn + ln
	m = ''
	for i in ripm:
		m += mf[i-1]
	return m



def F(rn, kn):
	s ={ 's1': [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
		 [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
		 's2': [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
		 [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
		 's3': [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
		 [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
		 's4': [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
		 [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
		 's5': [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
		 [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
		 's6': [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
		 [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
		 's7': [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
		 [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
		 's8': [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
		 [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
	}
	em = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,
		 16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
	pm = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
	e = ''
	for i in em:
		e += rn[i-1]
	ekx = XOR(e, kn)
	ekxs = []
	for i in range(8):
		tem = ekx[i*6:(i+1)*6]
		ekxs.append(tem)
	so = ''
	for i,j in zip(ekxs,s):
		x = int(i[0]+i[5], 2)
		y = int(i[1:5], 2)
		sos = str(bin(s[j][x][y]))[2:]
		so += sos.zfill(4)
	f = ''
	for i in pm:
		f += so[i-1]

	return f

def XOR(s1, s2):
	res = ''
	for i in range(len(s1)):
		res += str(int(s1[i])^int(s2[i]))
	return res

def CBCE(bits):
	Z = getZ()
	#print(len(Z))
	C = ''
	blocklen = int(len(bits)/64)
	MF = Z
	for i in range(blocklen):
		MB = bits[i*64:(i+1)*64]
		#print(XOR(MB, MF))
		CB = E(XOR(MB, MF))
		MF = CB
		C += CB
	return C, Z

def CBCD(chipertext, vi):
	Z = vi
	M = ''
	blocklen = int(len(chipertext)/64)
	CF = Z
	for i in range(blocklen):
		CB = chipertext[i*64:(i+1)*64]
		#print(D(CB))
		MB = XOR(D(CB), CF)
		CF = CB
		M += MB
	return M

def getZ():
	Z = ''
	i = 0
	for i in range(64):
		n = random.randint(0,1)
		Z += str(n)
		i += 1
	#print(Z)
	return Z

if __name__ == '__main__':
	m = '0011000000110001001100100011001100110100001101010011011000110111'
	c = CBCE(m)
	#print(c)
	mm = CBCD(c)
	#print(mm)
