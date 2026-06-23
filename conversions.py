
import msvcrt
import menu

def DecToAny(value, destBase, digits):
	#sprawdzenie, czy wartość wejściowa jest obiektem pustym
	if value is None:
		print('Brak wartości wejściowej')
		return 0	
	
	result = ''
	
	value = int(value)
	#sprawdzenie, czy value <0
	if value < 0:
		print('Obsługiwane sa tylko liczby dodatnie.')
		return None
	
	while value > 0:        
		digit = value % destBase
		if digit < 10:
			result = chr(ord('0') + digit) + result
		else:
			result = chr(ord('A') + (digit - 10)) + result
		value = value // destBase
	#sprawdzenie, czy podaną liczbę można przedstawić na określonej liczbie cyfr	
	#jeżeli nie, zwracamy None	  
	if len(result) > digits:
		print('Podanej liczby nie można przedstawić w tym systemie liczbowym na wymaganej ilości cyfr.')
		return None
	return result.zfill(digits)

def IsValid(strVal, srcBase):
	for i in range(len(strVal)):
		if srcBase <= 10:
			if not (ord('0') <= ord(strVal[i]) < (ord('0') + srcBase)):
				return False
		elif srcBase <= 36:
			if not ((ord('0') <= ord(strVal[i]) <= (ord('9'))) \
			or (ord('A') <= ord(strVal[i]) < (ord('A') + srcBase - 10))):
				return False
	return True	
			

def AnyToDec(strVal, srcBase):
	#sprawdzenie, czy wartość wejściowa = None
	#sprawdzenie, czy podana wartość zawiera dozwolone cyfry w podanym systemie liczbowym
	#w przeciwnym wypadku zwraca None
	
	dec = 0	
	for i in range(len(strVal)):
		if strVal[i].isdigit():
			dec += int(strVal[i]) * srcBase ** (len(strVal) - i - 1)
		elif ord('A') <= ord(strVal[i].upper()) <= ord('Z'):
			dec += int(ord(strVal[i]) - ord('A') + 10) * srcBase ** (len(strVal) - i - 1)
	return dec	
			
def Convert(strVal, srcBase, destBase, digits):
	
	return DecToAny(str(AnyToDec(strVal, srcBase)), destBase, digits)

def DecToAnyMenuOption():
	l = int(input ("Podaj liczbę dziesiętną: "))
	p = int(input ("Podaj docelowy system liczbowy: "))
	digits = int(input ("Podaj liczbę cyfr: "))
	res = DecToAny(l,p,digits)
	print (res)
	
def AnyToDecMenuOption():
	l = input ("Podaj liczbę: ")
	p = int(input ("Podaj żródłowy system liczbowy: "))			
	res = AnyToDec(l,p)
	print (res)

def ConversionsMenu():
	menuItems = ['Konwersja liczby z systemu dziesiętnego na dowolny',
	'Konwersja liczby z dowolnego systemu liczbowego na dziesiętny']
	result = (-1,None)
	while result[0] != len(menuItems):
		result = menu.Menu("Przeliczenia między systemami liczbowymi", menuItems, True)

		match result[0]:
			case 0:
				DecToAnyMenuOption()
				msvcrt.getch()
			case 1:
				AnyToDecMenuOption()
				msvcrt.getch()
		
