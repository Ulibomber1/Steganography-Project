from PIL import Image
import Tkinter
import binascii
import numpy as np

##########
#Tkinter GUI
##########

#Root Window
root = Tkinter.Tk()
root.wm_title('Steganography Hider/Retreiver')

#Model
global filenameStr
filenameStr = Tkinter.StringVar()
filenameStr.set('')
global messageStr
messageStr = Tkinter.StringVar()
messageStr.set('')


#View
filenameEntry = Tkinter.Entry(root)
filenameEntry.grid(row=2, column=0, columnspan=2)
messageEntry = Tkinter.Text(root)
messageEntry.grid(row=1,column=0)


#Controller

#Message Hider
def hide():  
        filename = filenameEntry.get()
        message = messageEntry.get()        
	img = Image.open(filename)
	binary = str2bin(message) + '1111111111111110'
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		datas = img.getdata()
		print 'Before'
		print list (datas[1]),list (datas[2]),list (datas[3]),list (datas[4]),list (datas[5]),list (datas[6]),list (datas[7]),list (datas[8]),list (datas[9]),list (datas[10])
		newData = []
		digit = 0
		temp = ''
		
		'''#rgb2hex feedback
		print 'rgb2hex Before:'
                print '(',r,',',g,',',b,')'
                print 'rgb2hex After:'
                print '#{:02x}{:02x}{:02x}'.format(r, g, b)
                
                #hex2rgb feedback
                print 'hex2rgb Before:'
                print hexcode
                print 'Hex2rgb step1:'
                print hexcode[1:].decode('hex')
                print 'hex2rgb step2:'
                print map(ord, hexcode[1:].decode('hex'))
                print 'hex2rgb final:'
                print tuple(map(ord, hexcode[1:].decode('hex')))'''
                
		for item in datas:
	            rgb2hexfdbk = 0
		    hex2rgbfdbk = 0
                    if (digit < len(binary)):
			newpix = encode(rgb2hex(item[0],item[1],item[2]),binary[digit])
			if newpix == None:
				newData.append(item)
			else:
				r, g, b = hex2rgb(newpix)
				newData.append((r,g,b,255))
				digit += 1
                    else:
				newData.append(item)	
		img.putdata(newData)
		img.save(filename, "PNG")
		print 'RGB After'
		print list (datas[1]),list (datas[2]),list (datas[3]),list (datas[4]),list (datas[5]),list (datas[6]),list (datas[7]),list (datas[8]),list (datas[9]),list (datas[10])
		print 'Some times none the of the first ten RGB values are not changed also can been seen better on black images'
		return "Completed!"
			
	return "Incorrect Image Mode, Couldn't Hide"

#Message Retrieval						
def retr(filename):
	img = Image.open(filename)
	binary = ''
	
	if img.mode in ('RGBA'): 
		img = img.convert('RGBA')
		datas = img.getdata()
		
		for item in datas:
			digit = decode(rgb2hex(item[0],item[1],item[2]))
			if digit == None:
				pass
			else:
				binary = binary + digit
				if (binary[-16:] == '1111111111111110'):
					print "Success"
					return bin2str(binary[:-16])

		return bin2str(binary)
	return "Incorrect Image Mode, Couldn't Retrieve"


hide_button = Tkinter.Button(root, command=hide,text='Hide')
hide_button.grid(row=0, column=1)
retr_button = Tkinter.Button(root, command=retr,text='Retr')
retr_button.grid(row=1, column=1)


##########
#Functions
##########

def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(hexcode):
    
    return tuple(map(ord, hexcode[1:].decode('hex'))) 

#Returns hexadecimal value of the user's string.
def str2bin(message):
    print 'str2bin before:'
    print message
    print 'str2bin step1:'
    print binascii.hexlify(message)
    print 'str2bin step2:'
    print int(binascii.hexlify(message), 16)
    binary = bin(int(binascii.hexlify(message), 16))
    print 'str2bin Final:'
    print binary 
    return binary[2:]

def bin2str(binary):
    print 'bin2str Before:'
    print binary
    print 'bin2str step1:'
    print int('0b'+binary,2)
    message = binascii.unhexlify('%x' % (int('0b'+binary,2)))
    print 'bin2str Final:'
    print message
    return message

def encode(hexcode, digit):
	if hexcode[-1] in ('0','1', '2', '3', '4', '5'):
		hexcode = hexcode[:-1] + digit
		return hexcode
	else:
		return None

def decode(hexcode):
	if hexcode[-1] in ('0', '1'):
		return hexcode[-1]
	else:
		return None


#Main Loop
root.mainloop()