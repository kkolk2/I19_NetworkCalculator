import conversions as conv

#klasy reprezentujące błedne wartości w adresie IPv4
class InvalidOctetsNumber(Exception):
	pass
class InvalidOctetValue(Exception):
	pass
class NetmaskDiscontinuous(Exception):
	pass

class IPv4Address():

	def __init__(self, address):
		self.address = self._IPv4AddressToDec(address)
		
		pass

	def __ToList(self, IPv4AddressDotDec):
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
	
	def __ToDotDec(self, list):
		str2 = ""
		for i in range(len(list)):
			str2 += str(list[i])
			if i < len(list)-1:
				str2+="."
		return str2

	#funkcja walidująca podany na wejście adres IPv4
	def _ValidateIPv4Address(self, IPv4Address):
		#jeżeli podano adres IPv4 w postaci kropkowo-dziesiętnej
		octets = []
		if type(IPv4Address) == str: 
			octets = self.__ToList(IPv4Address)
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
	def _IPv4AddressToDec(self, IPv4Address):
		if self._ValidateIPv4Address(IPv4Address):
			if type(IPv4Address) == str: 
				listOfOctets = self.__ToList(IPv4Address)
			elif type(IPv4Address) == list:
				listOfOctets = IPv4Address
			elif type (IPv4Address) == int: 
				return IPv4Address & conv.AnyToDec(32*"1",2)			
			IPv4AddressDec = 0
			for i in range(len(listOfOctets)):
				IPv4AddressDec <<= 8
				IPv4AddressDec += listOfOctets[i]			
			return IPv4AddressDec
	
	#zwraca reprezentację dziesiętną adresu
	def GetDec(self):
		return self.address
	
	#zamiana adresu IPv4 na liczbę binarną
	def GetBin(self):
		return conv.DecToAny(self.address, 2, 32)		
		

	#funkcja przekształca adres IPv4 w postaci dziesiętnej na listę oktetów
	def GetList(self):			
		octets = []
		ipv4AddressDec = self.address
		for i in range(4):
			
			#zapisywanie ostatnich 8 bitów do zmiennej octet i dodanie jej do listy
			octet = ipv4AddressDec & 255
			octets.insert(0, octet)
			#przesuwanie liczby ipv4AddressDec o 8 bitów w prawo
			ipv4AddressDec >>= 8
		
		return octets
	
	

	# funkcja przekształca adres IPv4 na format kropkowo-dziesiętny
	def GetDotDec(self):
		return self.__ToDotDec(self.GetList())
	
	#reprezentacja łańcuchowa
	def __str__(self):
		return f"{self.GetDotDec()}"


class IPv4Netmask(IPv4Address):
	
	def __init__(self, netmask):
		if self.__ValidateIPv4Netmask(netmask):
			super().__init__(netmask)


	# Walidacja maski podsieci
	def __ValidateIPv4Netmask(self, IPv4Netmask):
		if super()._ValidateIPv4Address(IPv4Netmask):
			#walidacja ciągłości maski podsieci. 
			#Maska podsieci składa się z sekwencji binarnych jedynek i następujących po nich zer.
			#jeśli w masce wystąpi sekwencja 01, maska jest nieciągła
			netmaskBin = conv.DecToAny(super()._IPv4AddressToDec(IPv4Netmask), 2, 32)
			
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
			

	# Obliczanie długości prefixu (liczba binarnych 1 w masce)
	def GetPrefixLength(self) -> int:
		
		netmaskDec = self.address		
		bit=0
		prefixLength = 32		
		while bit == 0:
			bit = netmaskDec & 1
			if bit == 0:
				prefixLength -= 1
			netmaskDec >>= 1
		return prefixLength
	
	def SetIPv4NetmaskFromPrefixLength(self, prefixLength: int) -> int:
		if prefixLength > 0 and prefixLength <= 32:
			netmaskBin = prefixLength*"1" + (32 - prefixLength)*"0"
			self.address = conv.AnyToDec(netmaskBin, 2)
		else:
			raise ValueError("Nieprawidłowa długość prefixu maski podsieci")
		
class IPv4Network():
	
	def __init__(self, address, netmask):
		self.address = IPv4Address(address)		
		self.netmask = IPv4Netmask(netmask)
		#obliczenie adresu sieci, na wypadek, gdyby podano adres hosta
		self.address.address &= self.netmask.address
		
	def __str__(self):
		return f"{self.address}/{self.netmask.GetPrefixLength()}"
	# Funkcja zwraca informacje na temat adresacji IPv4 sieci, do której należy podany adres i maska podsieci
	def GetNetworkInfo(self) -> dict:	
		
		
		# obliczanie adresu sieci jako iloczynu logicznego adresu IP i maski podsieci
		networkAddress = IPv4Address(self.address.GetDec() & self.netmask.GetDec())
		
		broadcastAddress = IPv4Address(int(networkAddress.GetDec() | (~self.netmask.GetDec() + (1 << 32))))
		
		firstHostAddress = IPv4Address(networkAddress.GetDec() + 1)
		lastHostAddress = IPv4Address(broadcastAddress.GetDec() - 1)
		
		# Obliczanie długości prefixu (liczba binarnych 1 w masce)
		prefixLength = self.netmask.GetPrefixLength()		
		# budowanie słownika
		network = {}
		network['networkAddress'] = networkAddress.GetList()
		network['netmask'] = self.netmask.GetList()
		network['prefixLength'] = prefixLength
		network['firstAddress'] = firstHostAddress.GetList()
		network['lastAddress'] = lastHostAddress.GetList()
		network['broadcastAddress'] = broadcastAddress.GetList()
		network['hostsNumber'] = (broadcastAddress.GetDec() - networkAddress.GetDec() - 1)

		return network

if __name__ == '__main__':
	net = IPv4Network('192.168.15.10','255.255.252.0')
	print(net)
	print(net.GetNetworkInfo())

#TODO: przerobić wszystko poniżej

# # funkcja parsuje adres IPv4 w formacie address/prefix i zwraca w postaci słownika
# def ParseIPv4Address(IPv4AddressAndPrefix: str) -> dict:
# 	#rozdzielenie części adresu i prefixa maski podsieci
# 	partsList = IPv4AddressAndPrefix.replace(" ","").split("/")
	
# 	paramsDict = {'Address': IPv4AddressToList(partsList[0])}	
# 	if len(partsList) >= 2:
# 		paramsDict['PrefixLength'] = int(partsList[1])
		
# 		paramsDict['Netmask'] = ToList(GetIPv4AddressDotDec(GetIPv4NetmaskFromPrefixLength(int(partsList[1]))))
		
# 	return 	paramsDict



# # Podział sieci na podsieci
# def IPv4Subnetting(IPv4Network, IPv4Netmask, numberOfSubnets: int) -> list:
		
# 	ValidateIPv4Address(IPv4Network)
# 	ipv4NetworkDec = IPv4AddressToDec(IPv4Network)

# 	ValidateIPv4Netmask(IPv4Netmask)
# 	ipv4NetmaskDec = IPv4AddressToDec(IPv4Netmask)

# 	#obliczanie adresu sieci, na wypadek, gdyby użytkownik podał adres hosta
# 	ipv4NetworkDec = ipv4NetworkDec & ipv4NetmaskDec
	
# 	targetNetmask = ipv4NetmaskDec

# 	#obliczanie maski docelowej
# 	offset = 0
# 	while (2 ** offset) < numberOfSubnets:
# 		targetNetmask >>=1
# 		targetNetmask += (1 << 31)
# 		offset += 1

# 	#obliczanie adresów sieciowych
	
# 	subnets = []
# 	#obliczenie liczby bitów w części hosta
# 	hostsBitsNumber = 32 - GetIPv4NetmaskPrefixLength(targetNetmask)
# 	for i in range(numberOfSubnets):
# 		#dodanie informacji o podsieci do listy
# 		subnets.append(NetworkInfo(ipv4NetworkDec, targetNetmask))
# 		#obliczenie adresu następnej podsieci 
# 		ipv4NetworkDec += (1 << hostsBitsNumber)
	
# 	return subnets


# # funkcja sortuje podany na wejście słownik wg liczby hostów
# def SubnetsSort(networks: dict, method: int, reverse = False) -> list:
# 	templist = list(networks.items())
# 	print(templist)
# 	#sortowanie bąbelkowe
# 	if method == 0:		
# 		for maxElement in range(len(templist)-1,1,-1):
# 			for index in range(maxElement):
# 				#kierunek sortowania
# 				condition = False
# 				if reverse == True:
# 					condition = templist[index][1]['hostsNumber'] < templist[index + 1][1]['hostsNumber']
# 				else:
# 					condition = templist[index][1]['hostsNumber'] > templist[index + 1][1]['hostsNumber']
# 				if condition == True:
# 					temp = templist[index]
# 					templist[index] = templist[index + 1]
# 					templist[index + 1] = temp
	
# 	return templist
# '''
# TODO: 
# 	- rozdział adresu w formacie x.x.x.x/y na adres IP i maskę podsieci (w postaci słownika)
# 	- podział na równe podsieci 
# 	- przetestować wszystko

# '''
# #

# if __name__ == "__main__":
# 	networks = {
# 		"LAN1": {		
# 			"hostsNumber": 35
# 			},
# 		"LAN2": {
# 			"hostsNumber": 12
# 			},
# 		"LAN3": {
# 			"hostsNumber": 20
# 			},
# 	}

# 	print (SubnetsSort(networks,0,True))

# def MACToBin(MACaddress):
# 	bytesList = MACaddress.split('-')
# 	bin = ''
# 	for element in bytesList:
# 		bin += conv.Convert(element, 16, 2, 8)
# 	return bin