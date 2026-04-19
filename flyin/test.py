string = "ABCD"
# lower the string
lowered = string.lower()


#Revers the stringl
length= len(string)
reversed = ""
reversed += lowered[length-1]
reversed += lowered[length-2]
reversed += lowered[length-3]
reversed += lowered[length-4]
print(reversed)