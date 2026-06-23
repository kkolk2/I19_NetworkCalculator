
import conversions as conv
import networks as nets
import functions as f
import menu
import msvcrt 

mainMenu = ['Przeliczenia systemów liczbowych',
		'Przeliczenia adresów IPv4',
		'Przeliczenia adresów IPv6' ]

try:	
	mainMenuResult = (-1,None)
	while mainMenuResult[0] != 3:
		mainMenuResult = menu.Menu("Menu główne", mainMenu)

		match mainMenuResult[0]:
			case 0:
				conv.ConversionsMenu()
			case 1:
				nets.IPv4NetworksMenu()
			case 2:
				print('W budowie...')
				msvcrt.getch()	
	
except nets.NetmaskDiscontinuous as nd:
	print ('Błąd!', nd.args[0], nd.args[1])
	

