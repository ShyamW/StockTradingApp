from Models.Model import *

a = BankWithdrawals(person_id=1, amount=333.3)
db.session.add(a)
db.session.commit()

z = BankWithdrawals.query.all()
print(z)


