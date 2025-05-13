ht = "Rani menemukan sebuah catatan kecil di dalam laci yang terkunci. Catatan itu bertuliskan, '************************************************************************************************************************************************************************************************************************************************'."
ct = "naccani lie,aebnuaaem aaamg jni n.eun ikae,m  aj.amaakk {niaannahnanbaicrtbnaauk ar kiu hJimknaasualak elacnuJmiddaa cnpeukhhknniaaea'  tl   tsabk gnatisuae.iy  ekaja Ruhkaynat' nu wJune mmea iaabjpky}ma d utr uista gerp adRilrk  m  hinaimg.iikm hnagnr tbltsnu,dag tgeetdaea akcmeny k tjaiC  eugd tgamsa ltCuk aadannu,enwb aasgn nans"

init = ht[:90]
print(init)

blocks = ["", "", "", "", "", "", "", "", "", ""]
print(len(blocks))

for i in range(0, 90):
	blocks[i % 10] += ht[i]
print(blocks)

key = []
for i, block in enumerate(blocks):
	print(ct.index(block))
	key.append(ct.index(block))
print(key)

pt = ["A"] * len(ct)
for i, k in enumerate(key):
	for j in range(34):
		try:
			pt[j*10 + i] = ct[k+j]
		except:
			continue
print(''.join(pt))