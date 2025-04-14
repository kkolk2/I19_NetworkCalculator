
def DecToAny(value, destBase, digits):
	#sprawdzenie, czy wartość wejściowa jest obiektem pustym
	if value is None:
		print('Brak wartości wejściowej')
		return 0
		
	result = ''		
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

#sprawdza, czy liczba zapisana w podanym systemie liczbowym zawiera prawidłowe cyfry
def IsValid(strVal, srcBase):
	for i in range(len(strVal)):
		digits = 0
		letters = srcBase - 10
		if letters >= 0:
			digits = 10
		else:
			digits = srcBase
			letters = 0

		if not ((ord('0') <= ord(strVal[i]) < (ord('0') + digits)) \
		or (ord('A') <= ord(strVal[i]) < (ord('A') + letters))):
			return False
		""" if srcBase <= 10:
			if not (ord('0') <= ord(strVal[i]) < (ord('0') + srcBase)):
				return False
		elif srcBase <= 36:
			if not ((ord('0') <= ord(strVal[i]) <= (ord('9'))) \
			or (ord('A') <= ord(strVal[i]) < (ord('A') + srcBase - 10))):
				return False """
			
	return True	
			

def AnyToDec(strVal, srcBase):
	#sprawdzenie, czy wartość wejściowa = None
	if strVal == None:
		print("Nie podano wartości wejściowej.")
		return None
	#sprawdzenie, czy podana wartość zawiera dozwolone cyfry w podanym systemie liczbowym
	#w przeciwnym wypadku zwraca None
	if IsValid(strVal, srcBase):		
		dec = 0	
		
		for i in range(len(strVal)):
			if strVal[i].isdigit():
				dec += int(strVal[i]) * srcBase ** (len(strVal) - i - 1)
			elif ord('A') <= ord(strVal[i]) <= ord('Z'):
				dec += int(ord(strVal[i]) - ord('A') + 10) * srcBase ** (len(strVal) - i - 1)
		return dec
	else:
		print("Podana wartość wejściowa zawiera cyfry nie występujące w {} systemie liczbowym.".format(srcBase))
		return None
			
def Convert(strVal, srcBase, destBase, digits):
	
	return DecToAny(str(AnyToDec(strVal, srcBase)), destBase, digits)
