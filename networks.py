import conversions as conv
import functions as func
import msvcrt
import menu

# -----------------------------------------------------------------------------
#           Zmienne globalne
# -----------------------------------------------------------------------------

#klasy reprezentujące błedne wartości w adresie IPv4
class InvalidOctetsNumber(Exception):
	pass
class InvalidOctetValue(Exception):
	pass
class NetmaskDiscontinuous(Exception):
	pass

# -----------------------------------------------------------------------------
#           Funkcje obsługi sieci
# -----------------------------------------------------------------------------

def ToList(IPv4AddressDotDec):
    list = IPv4AddressDotDec.split(".")
    list2 = []
    for element in list:
        try:
            list2.append(int(element))
        except ValueError as ve:
            #print("Podana wartość nie jest liczbą. Przyjęto 0. Kod:", ve.args)
            list2.append(0)
            raise InvalidOctetValue("Oktet zawiera niedozwolone znaki: " + element,0,0)
            
    return list2
	
def ToDotDec(list):
	str2 = ""
	for i in range(len(list)):
		str2 += str(list[i])
		if i < len(list)-1:
			str2+="."
	return str2
	
# def IPv4AddressToBin(IPv4AddressDotDec):
#     if ValidateIPv4Address(IPv4AddressDotDec):
#         s = ""
#         l = ToList(IPv4AddressDotDec)
#         for el in l:
#             s += conv.DecToAny(el, 2, 8)
#         return s
#     else:
#         return 32*"0"
			

def MACToBin(MACaddress):
	bytesList = MACaddress.split('-')
	bin = ''
	for element in bytesList:
		bin += conv.Convert(element, 16, 2, 8)
	return bin

#funkcja walidująca podany na wejście adres IPv4
def ValidateIPv4Address(IPv4Address: str|list|int) -> bool:
	#jeżeli podano adres IPv4 w postaci kropkowo-dziesiętnej
	octets = []
	if type(IPv4Address) == str: 
		octets = ToList(IPv4Address)
	#jeżeli podano adres IPv4 w postaci listy oktetów
	elif type(IPv4Address) == list:
		octets = IPv4Address
	elif type(IPv4Address) == int:
		if IPv4Address <= conv.AnyToDec(32*"1",2): return True
		else: raise ValueError("Nieprawidłowa wartość dziesiętna adresu IPv4")	
	
	try:
		#sprawdzamy, czy liczba oktetów jest prawidłowa
		if len(octets) < 4:
			raise InvalidOctetsNumber("Za mało oktetów", len(octets))
		if len(octets) > 4:
			raise InvalidOctetsNumber("Za dużo oktetów", len(octets))
		#sprawdzamy, czy każdy oktet ma prawidłową wartość (między 0 a 255)
		for i in range(len(octets)):
			if octets[i] < 0 or octets[i] > 255:
				raise InvalidOctetValue("Nieprawidłowa wartość oktetu", (i + 1), octets[i])
		
		return True
	finally:
		pass
#zamienia na 32-bitową liczbę dziesiętną 
def IPv4AddressToDec(IPv4Address: str|list|int) -> int: 
	if ValidateIPv4Address(IPv4Address):
		if type(IPv4Address) == str: 
			listOfOctets = ToList(IPv4Address)
		elif type(IPv4Address) == list:
			listOfOctets = IPv4Address
		elif type (IPv4Address) == int: 
			return IPv4Address & conv.AnyToDec(32*"1",2)

		IPv4AddressDec = 0
		for i in range(len(listOfOctets)):
			IPv4AddressDec <<= 8
			IPv4AddressDec += listOfOctets[i]
		return IPv4AddressDec

#zamiana adresu IPv4 na liczbę binarną
def IPv4AddressToBin(IPv4Address):
	if ValidateIPv4Address(IPv4Address):
		return conv.DecToAny(IPv4AddressToDec(IPv4Address), 2, 32)		
	else:
		return 32*"0"

#funkcja przekształca adres IPv4 w postaci dziesiętnej na listę oktetów
def IPv4AddressToList(ipv4Address):
	#sprawdzamy, czy podany adres IPv4 już jest listą
	if type(ipv4Address) == list:
		if ValidateIPv4Address(ipv4Address):
			return ipv4Address
	
	ipv4AddressDec = IPv4AddressToDec(ipv4Address)
	
	octets = []
	for i in range(4):
		#zapisywanie ostatnich 8 bitów do zmiennej octet i dodanie jej do listy
		octet = ipv4AddressDec & 255
		octets.insert(0, octet)
		#przesuwanie liczby ipv4AddressDec o 8 bitów w prawo
		ipv4AddressDec >>= 8
	
	return octets

# funkcja przekształca adres IPv4 na format kropkowo-dziesiętny
def GetIPv4AddressDotDec(IPv4Address):
	return ToDotDec(IPv4AddressToList(IPv4Address))

# Walidacja maski podsieci
def ValidateIPv4Netmask(IPv4Netmask):
	if ValidateIPv4Address(IPv4Netmask):
		#walidacja ciągłości maski podsieci. 
		#Maska podsieci składa się z sekwencji binarnych jedynek i następujących po nich zer.
		#jeśli w masce wystąpi sekwencja 01, maska jest nieciągła
		netmaskBin = IPv4AddressToBin(IPv4Netmask)
		
		try:
			#znajdź sekwencję 01 w masce podsieci
			#jeśli sekwencja 01 zostanie znaleziona, rzuć wyjątek NetmaskDiscontinuous
			#jeśli sekwencja 01 nie zostanie znaleziona, metoda index() rzuca wyjątek ValueError
			#przechwytujemy ten wyjątek i zwracamy True, co oznacza, że maska jest prawidłowa
			index = netmaskBin.index("01")
			
			if index >= 0:
				raise NetmaskDiscontinuous("Brak ciągłości maski na bicie", index + 1)
		except ValueError as ve:
			if ve.args[0] == "substring not found":
				return True
		#return True

# Obliczanie długości prefixu (liczba binarnych 1 w masce)
def GetIPv4NetmaskPrefixLength(IPv4Netmask: str|list|int) -> int:
	if ValidateIPv4Netmask(IPv4Netmask):
		netmaskDec = IPv4AddressToDec(IPv4Netmask)
		
		bit=0
		prefixLength = 32		
		while bit == 0 and prefixLength > 0:
			bit = netmaskDec & 1
			if bit == 0:
				prefixLength -= 1
			netmaskDec >>= 1
		return prefixLength
	
def GetIPv4NetmaskFromPrefixLength(prefixLength: int) -> int:
	if prefixLength >0 and prefixLength <=32:
		netmaskBin = prefixLength*"1" + (32 - prefixLength)*"0"
		return conv.AnyToDec(netmaskBin, 2)
	else:
		raise ValueError("Nieprawidłowa długość prefixu maski podsieci")
		

# Funkcja zwraca informacje na temat adresacji IPv4 sieci, do której należy podany adres i maska podsieci
def NetworkInfo(IPv4Address: str|list|int, IPv4Netmask: str|list|int) -> dict:	
	
	addressDec = IPv4AddressToDec(IPv4Address)
	netmaskDec = IPv4AddressToDec(IPv4Netmask)

	# obliczanie adresu sieci jako iloczynu logicznego adresu IP i maski podsieci
	networkAddressDec = addressDec & netmaskDec
	
	#obliczanie adresu rozgłoszeniowego
	broadcastAddressDec = int(networkAddressDec | (~netmaskDec + (1 << 32)))
	
	#obliczanie adresów użytecznych
	firstHostAddressDec = networkAddressDec + 1
	lastHostAddressDec = broadcastAddressDec - 1
	
	# Obliczanie długości prefixu (liczba binarnych 1 w masce)
	
	prefixLength = GetIPv4NetmaskPrefixLength(IPv4Netmask)
			
		
	# budowanie słownika
	network = {}
	network['networkAddress'] = IPv4AddressToList(networkAddressDec)
	network['netmask'] = IPv4AddressToList(netmaskDec)
	network['prefixLength'] = prefixLength
	network['firstAddress'] = IPv4AddressToList(firstHostAddressDec)
	network['lastAddress'] = IPv4AddressToList(lastHostAddressDec)
	network['broadcastAddress'] = IPv4AddressToList(broadcastAddressDec)
	network['hostsNumber'] = (broadcastAddressDec - networkAddressDec - 1)

	return network

#funkcja dzieli sieć na równe podsieci
def Subnetting(IPv4Address: str|list|int, IPv4Netmask: str|list|int, names: list) -> dict:
	
	addressDec = IPv4AddressToDec(IPv4Address)
	netmaskDec = IPv4AddressToDec(IPv4Netmask)
	networksNumber = len(names)
	
	#upewniamy się, że podany adres jest adresem sieci
	addressDec = addressDec & netmaskDec
	
	#obliczamy liczbę bitów, o którą należy przesunąć maskę w prawo
	# 2^n >= N, gdzie n - liczba bitów o którą należy przesunąć maskę, N - liczba sieci do podziału
	n = 0	
	while 2 ** n < networksNumber:
		n += 1
	
	#obliczanie nowej maski podsieci
	subnetsNetmask = netmaskDec
	
	for i in range(n):
		subnetsNetmask >>= 1
		subnetsNetmask += (1 << 31)
	#Obliczanie informacji dla poszczególnych podsieci
	subnetsDict = {}
	address = addressDec
	for i in range(networksNumber):
		subnetsDictTemp = NetworkInfo( address, subnetsNetmask)
		subnetsDict[names[i]] = subnetsDictTemp
		address = IPv4AddressToDec(subnetsDictTemp['broadcastAddress']) + 1
		
	return subnetsDict
	

def NestedSubnetting (IPv4Address: str|list|int, IPv4Netmask: str|list|int) -> dict:
	#addressDotDec = GetIPv4AddressDotDec(IPv4AddressToDec(IPv4Address))
	names = ["SUBNET1", "SUBNET2"]
	result = {}
	
	
	if GetIPv4NetmaskPrefixLength(IPv4Netmask) <= 29:
		subnets = Subnetting(IPv4Address, IPv4Netmask, names)
		print (subnets)
		#for k, v in subnets.items():
			
			
			#TODO: dokończyć
		
	
	
	
	return result
	

# funkcja sortuje podany na wejście słownik wg liczby hostów
def SubnetsSort(networks: dict, method: int, reverse = False) -> list:
	templist = list(networks.items())
#print(templist)
#sortowanie bąbelkowe
	if method == 0:  
		for maxElement in range(len(templist)- 1, 1,-1):
			for index in range(maxElement):
			#kierunek sortowania
				condition = False
				if reverse == True:
					condition = templist[index][1]['hostsNumber'] < templist[index + 1][1]['hostsNumber']
				else:
					condition = templist[index][1]['hostsNumber'] > templist[index + 1][1]['hostsNumber']
				if condition == True:
					temp = templist[index]
					templist[index] = templist[index + 1]
					templist[index + 1] = temp
	 
	return templist

# -----------------------------------------------------------------------------
#           Obsługa menu IPv4Networks
# -----------------------------------------------------------------------------

def IPv4NetworksMenu():
	menuItems = ['Informacje o sieci na podstawie IP i maski',
	'Podział sieci na równe podsieci', 'Podział sieci z dostosowaniem maski podsieci (VLSM)']
	result = menu.Menu("Działania na adresach IPv4", menuItems, True)

	match result[0]:
		case 0:
			NetworkInfoMenuOption()
			msvcrt.getch()
		case 1:			
			SubnettingMenuOption()
			msvcrt.getch()
		case 2:
			print ("W budowie...")
			msvcrt.getch()

def NetworkInfoMenuOption():
	IPv4Address = input('Podaj adres IPv4: ')
	IPv4Netmask = input('Podaj maskę podsieci: ')
	res = NetworkInfo(IPv4Address, IPv4Netmask)
	print ("Oto szczególowe informacje na temat tej podsieci:")
	print (res)

def SubnettingMenuOption():
	IPv4Address = input('Podaj adres sieci IPv4: ')
	IPv4Netmask = input('Podaj maskę podsieci: ')
	networksNumber = int(input('Na ile sieci dzielimy? '))
	names = []
	for i in range(networksNumber):
		name = input('Podaj nazwę sieci nr ' + str(i) + ': ')
		names.append(name)
	res = Subnetting(IPv4Address, IPv4Netmask, names)
	print ("Sieci po podziale wyglądają następująco:")
	print (res)


	

	
 
if __name__ == '__main__':
	networks = {
		"LAN1": {  
		"hostsNumber": 35
		},
		"LAN2": {
		"hostsNumber": 12
		},
		"LAN3": {
		"hostsNumber": 20
		},
	}

	NestedSubnetting('192.168.1.0', '255.255.255.0')