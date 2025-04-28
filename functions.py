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

#funkcja wyszukuje ciąg znaków w tekście metodą sekwencyjną
#wartość zwracana: int - index znaku, od którego zaczyna się pierwsze wystąpienie szukanej wartości
#gdy wartość nie zostanie znaleziona, rzuca wyjątek ValueError z komunikatem "substring not found"
def Search(inputText: str, substring: str) -> int:

	len_it = len(inputText)
	len_s = len(substring)
	if len_it >= len_s:
		for index in range(len_it - len_s + 1):
			if inputText[index] == substring[0]:
				correct = True
				checkingIndex = index + 1
				i = 0
				while correct == True and (checkingIndex - index) < len_s:
					if inputText[checkingIndex] == substring[checkingIndex - index]:
						checkingIndex += 1
					else:
						correct = False
				if correct == True: 
					return index
		raise ValueError("substring not found")
	else:
		raise ValueError("searching substring is longer than input text")

#print(Search("Ala ma kota", ""))

