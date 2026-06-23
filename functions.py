#pobieranie liczby. Zwraca liczbę w formacie int
def InputNumber(message):
	number = 0
	while True:
		try:
			number = int(input(message))
			break
			
		except ValueError as verr:
			print("Podana wartość nie jest liczbą. Wprowadź jeszcze raz. Kod:", verr.args)
	return number
	
#print(InputNumber("Podaj liczbe: "))

#funkcja wyszukuje podłańcuch w łańcuchu
#wartość zwracana: int - index znaku, od którego zaczyna sie poszukiwana sekwencja
#jeśli nie zostanie znaleziona - wyjątek ValueError("substring not found")
def Search(inputText: str, substring: str) -> int:
	
	#rozmiary łańcuchów
	len_it = len(inputText)
	len_s = len(substring)
	
	if len_it >= len_s:
		for index in range(len_it - len_s + 1):
			if inputText[index] == substring[0]:
				correct = True
				checkingIndex = index + 1
				while correct and (checkingIndex - index) < len_s:
					if inputText[checkingIndex] == substring[checkingIndex - index]:
						checkingIndex += 1
					else:
						correct = False
				if correct:
					return index
		raise ValueError("substring not found")
	else:
		raise ValueError("substring is longer than input text")
		
def Power(a, b):
	result = 1
	while b > 0:
		if b%2:
			result *= a
		a *= a
		b //= 2
	return result
	
	