len = float(input("Lengte: "))
gew = float(input("Gewicht: "))
# print("Je BMI is: ", round((gew * 100 * 100) / (len * len), 2))
bmi= (round((gew * 100 * 100) / (len * len), 2))
#bmi = 100 ** 2 * gew / len ** 2
if bmi < 18:
    melding = "te laag"
elif bmi <= 25:
    melding = "gezond"
else :
    melding = "oepsi"
print ("Je BMI is:", bmi, "en dat is", melding)