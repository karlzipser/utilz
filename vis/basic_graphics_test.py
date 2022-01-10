"""#,bga
python3 k3/misc/basic_graphics_test.py
#,bgb"""

from utilz.vis import *

clear_screen()
cr('r')
cg('g')
cb('b')
clp('testing','`rgb','various','`ybu','colors','`m')

raw_enter()

a = z55(rndn(64,64,3))
img_path = opjD('temp.jpg')
imsave(img_path,a)
b = imread(img_path)

mi(b)
mci(b,scale=4)

raw_enter();CA()

os.system('rm '+img_path)

hist(rndn(10000))
spause()
raw_enter();CA()

xy = rndn(1000,2)
pts_plot(xy)
plt_square()
spause()
raw_enter();CA()
#,a
print('cv2 test')
for k in range(3):
	print(k)
	for i in range(0,100,1):
		m = z55(rndn(100,100,3))
		m = m // 2
		m[i,:,:] = (255,0,0)
		j = (k+1)*i
		while j >= 100:
			j = j - 99
		m[:,j,:] = (0,255,0)
		#m[i,i,:] = 255
		d = 1000//30
		#if i == 50:
		#	d = 1000
		mci(m,delay=d,scale=4,)
		#time.sleep(1/15)

raw_enter()
CA()
#,b

#EOF

