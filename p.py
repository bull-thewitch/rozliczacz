from payoff import Payoff
import sys

x = Payoff()   #tworzę obiekt
x.load_from_file(sys.argv[1])   #parametr[1] to nazwa pliku, który ma być wczytany. Uruchamiam przez terminal "python 3 a.py o.csv"
# x.load_from_file("/Users/aga/rozliczenia/o.csv")   # mozna to te uruchomić bez sys.argv (wtedy nie przekazuje tego jako parametr)
x.calculate()
print(x)




