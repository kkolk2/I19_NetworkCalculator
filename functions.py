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