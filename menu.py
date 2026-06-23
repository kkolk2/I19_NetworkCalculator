import msvcrt
import os
#funkcje do obsługi menu tekstowego

#funkcja wyświetla opcje menu
def DisplayMenu(name, listOfOptions: list , isSubmenu = False):
	print (name + ":\n")
	i = 0
	while  i < len(listOfOptions):
		print (f"{i + 1}. {listOfOptions[i]}")
		i += 1
	
	if isSubmenu: print (f"{i + 1}. Powrót")
	else: print (f"{i + 1}. Koniec")
	print ()
		
def Validate(options: list, userInput):
	try:
		if 0 <= int(userInput - 1) <= len(options):
			return True	
		return False
	finally:
		pass
	
#pobiera  opcje w postaci listy
#return: wybrana opcja w postaci krotki (element 1 - index wybranej opcji, element 2 - treść wybranej opcji)
def Menu(name, options: list, isSubmenu = False) -> tuple:
	os.system('cls' if os.name == 'nt' else 'clear')
	if len(options) > 0:
		isCorrect = False
		userInput = None
		while isCorrect == False:
			#wyświetl menu	
			DisplayMenu(name, options, isSubmenu)	
			try:
				#pobrać wybraną opcję od użytkownika		
				userInput = int(input("Wybierz opcję: "))
				#walidacja wybranej opcji
				isCorrect = Validate(options, userInput)
			except ValueError:
				print("Wprowadzono nieprawidłową opcję. Spróbuj jeszcze raz.")
				msvcrt.getch()
			#czyszczenie ekranu
			os.system('cls' if os.name == 'nt' else 'clear')
		return (userInput - 1, options[userInput - 1] if userInput -1 < len(options) else 'Koniec')
	return None

if __name__ == '__main__':	
	options = ['aaa','bbb','ccc']
	print(Menu("Menu testowe", options))


	
	

