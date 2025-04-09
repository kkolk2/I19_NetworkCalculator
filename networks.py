import convertions as conv

#klasy reprezentujące błedne wartości w adresie IPv4
class InvalidOctetsNumber(Exception):
	pass
class InvalidOctetValue(Exception):
	pass

	
def ToList(addressDotDec):
    list = addressDotDec.split(".")
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
	
def AddressToBin(address):
    if ValidateIPv4Address(address):
        s = ""
        l = ToList(address)
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
def ValidateIPv4Address(IPv4Address):
	octets = ToList(IPv4Address)
	
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
def IPv4AddressToDec(IPv4Address):
	if ValidateIPv4Address(IPv4Address):
		listOfOctets = ToList(IPv4Address)
		result = 0
		for i in range(len(listOfOctets)):
			result <<= 8
			result += listOfOctets[i]
		return result


def ValidateIPv4Netmask(IPv4Netmask):
	if ValidateIPv4Address(IPv4Netmask):
		#walidacja ciągłości maski podsieci
		pass