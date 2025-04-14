import convertions as conv

#klasy reprezentujące błedne wartości w adresie IPv4
class InvalidOctetsNumber(Exception):
	pass
class InvalidOctetValue(Exception):
	pass
class NetmaskDiscontinuous(Exception):
	pass

	
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
	
def IPv4AddressToBin(IPv4AddressDotDec):
    if ValidateIPv4Address(IPv4AddressDotDec):
        s = ""
        l = ToList(IPv4AddressDotDec)
        for el in l:
            s += conv.DecToAny(el, 2, 8)
        return s
    else:
        return 32*"0"
			

def MACToBin(MACaddress):
	bytesList = MACaddress.split('-')
	bin = ''
	for element in bytesList:
		bin += conv.Convert(element, 16, 2, 8)
	return bin

#funkcja walidująca podany na wejście adres IPv4
def ValidateIPv4Address(IPv4AddressDotDec):
	octets = ToList(IPv4AddressDotDec)
	
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
def IPv4AddressToDec(IPv4AddressDotDec):
	if ValidateIPv4Address(IPv4AddressDotDec):
		listOfOctets = ToList(IPv4AddressDotDec)
		result = 0
		for i in range(len(listOfOctets)):
			result <<= 8
			result += listOfOctets[i]
		return result

# Walidacja maski podsieci
def ValidateIPv4Netmask(IPv4NetmaskDotDec):
	if ValidateIPv4Address(IPv4NetmaskDotDec):
		#walidacja ciągłości maski podsieci. 
		#Maska podsieci składa się z sekwencji binarnych jedynek i następujących po nich zer.
		#jeśli w masce wystąpi sekwencja 01, maska jest nieciągła
		netmaskBin = IPv4AddressToBin(IPv4NetmaskDotDec)
		
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
#funkcja przekształca adres IPv4 w postaci dziesiętnej na listę oktetów
def IPv4AddressDecToList(ipv4AddressDec):
	octets = []
	for i in range(4):
		#zapisywanie ostatnich 8 bitów do zmiennej octet i dodanie jej do listy
		octet = ipv4AddressDec & 255
		octets.insert(0,octet)
		#przesuwanie liczby ipv4AddressDec o 8 bitów w prawo
		ipv4AddressDec >>= 8
	return octets

# Funkcja zwraca informacje na temat adresacji IPv4 sieci, do której należy podany adres i maska podsieci
def NetworkInfo(IPv4AddressDotDec, IPv4NetmaskDotDec):
	
	ValidateIPv4Address(IPv4AddressDotDec)
	ValidateIPv4Netmask(IPv4NetmaskDotDec)
	addressDec = IPv4AddressToDec(IPv4AddressDotDec)
	netmaskDec = IPv4AddressToDec(IPv4NetmaskDotDec)

	# obliczanie adresu sieci jako iloczynu logicznego adresu IP i maski podsieci
	networkAddressDec = addressDec & netmaskDec
	
	broadcastAddressDec = int(networkAddressDec | (~netmaskDec + (1 << 32)))
	
	firstHostAddressDec = networkAddressDec + 1
	lastHostAddressDec = broadcastAddressDec - 1
	
	# Obliczanie długości prefixu (liczba binarnych 1 w masce)
	bit=0
	prefixLength = 32
	nm = netmaskDec
	while bit == 0:
		bit = nm & 1
		if bit == 0:
			prefixLength -= 1
		nm >>= 1		
		
	# budowanie słownika
	network = {}
	network['networkAddress'] = IPv4AddressDecToList(networkAddressDec)
	network['netmask'] = IPv4AddressDecToList(netmaskDec)
	network['prefixLength'] = prefixLength
	network['firstAddress'] = IPv4AddressDecToList(firstHostAddressDec)
	network['lastAddress'] = IPv4AddressDecToList(lastHostAddressDec)
	network['broadcastAddress'] = IPv4AddressDecToList(broadcastAddressDec)
	network['hostsNumber'] = (broadcastAddressDec - networkAddressDec - 1)

	return network


# Obliczanie adresu rozgłoszeniowego

