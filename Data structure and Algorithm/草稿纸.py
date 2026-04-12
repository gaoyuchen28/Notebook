# Tower of Hanoi
def Hanoi(n, fromTower, withTower, toTower):
    if n == 0:
        return
    Hanoi(n-1, fromTower, toTower, withTower)
    print("Disk ", n, "moved from ", fromTower,"to ",toTower)
    Hanoi(n-1, withTower, fromTower, toTower)

n=3
Hanoi(n, 'A','B','C')