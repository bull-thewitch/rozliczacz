class Payoff:
    
    def __init__(self):
        self.expenses = {}   # {wydatek: {osoba: kwota}}
        self.beneficiaries = {}   # {co: kto korzysta} 
        self.people = {}
        self.transfers = {}

    def load_from_file(self, fname, clear = False):
        if clear:
            self.expenses.clear()   
            self.beneficiaries.clear()   
            self.people.clear()
        try:
            with open(fname, "r") as f:
                for x in f:
                    z = x.strip().split(",")


                    if len(z) == 3 or len(z) == 2:
                        self.people[z[1]] = 0.0
                        if len(z) == 3:
                            if z[0] in self.expenses:   #sprawdzam czy w self.expenses istnieje klucz z[0]
                                self.expenses[z[0]][z[1]] = float(z[2])   #jeśli struktura {{}} istnieje to mogę do niej dodać kolejny element
                            else:
                                self.expenses[z[0]] = {z[1]: float(z[2])}    # else: tworzę podstrukturę
                        else:
                            if not z[0] in self.beneficiaries:
                                self.beneficiaries[z[0]] = set()
                            self.beneficiaries[z[0]].add(z[1])
                                
        except:
            return False

        return True
    
    def calculate(self):
        for k, v in self.expenses.items():
            if not k in self.beneficiaries:
                print(f"Brak informacji o konsumentach dla wydatku {k}.")
                return False
            sum = 0.0
            for l, w in v.items():
                sum += w
            
            avg = sum / len(self.beneficiaries[k])

            for l, w in v.items():
                self.people[l] -= w
            
            for l in self.beneficiaries[k]:
                self.people[l] += avg
        self.compute_transfers()
        return True

    def add_transfer(self, f, t, a):   #from, to, amount
        if f in self.transfers:
            self.transfers[f][t] = a
        else:
            self.transfers[f] = {t : a}

    def compute_transfers(self):
        credit = []
        debit = []

        for k, v in self.people.items():
            if v > 0:
                debit.append({k: v})
            elif v < 0:
                credit.append({k: -v})
        
        self.transfers.clear()

        cc = 0
        cd = 0

        while cc < len(credit) and cd < len(debit):
            c_dict = credit[cc]
            c_keys = c_dict.keys()
            c_list = list(c_keys)
            c_key = c_list[0]
            #c_key = list(credit[cc].keys())[0]

            d_dict = debit[cd]
            d_keys = d_dict.keys()
            d_list = list(d_keys)
            d_key = d_list[0]
            #d_key = list(debit[cd].keys())[0]

            c = credit[cc][c_key]   #pobieram wartość spod klucza c_key
            d = debit[cd][d_key]
            if c == d:
                self.add_transfer(d_key, c_key, c)
                cc += 1
                cd += 1
            elif c > d:
                self.add_transfer(d_key, c_key, d)
                credit[cc][c_key] -= d
                cd += 1
            else:   #c < d
                self.add_transfer(d_key, c_key, c)
                debit[cd][d_key] -= c
                cc += 1

    def save_to_file(self, fname):
        try:
            with open(fname, "w") as f:
                for k, v in self.expenses.items():
                    for l, w in v.items():
                        f.write(f"{k},{l},{w}\n")
                for k, v in self.beneficiaries.items():
                    for x in v:
                        f.write(f"{k},{x}\n")
        except:
            return False

        return True

    def __str__(self):
        res = ""
        for k, v in self.transfers.items():
            for m, n in v.items():
                res = res + f"{k} przelewa {m} kwotę {n}.\n"
        return res.strip()

# for k, v in x.transfers.items():
#     for m, n in v.items():
#         print(f"{k} przelewa {m} kwotę {n}.")