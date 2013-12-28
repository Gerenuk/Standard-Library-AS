from helper import CycleCaller


class A:
    def f(self, x):
        print("A", x)

a = CycleCaller(5, A())
for i in range(50):
    a.f(i)
