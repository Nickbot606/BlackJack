import table
import players


if __name__ == "__main__":
    t = table.debugTable()
    p1 = players.human.human()
    p2 = players.Player.Player(1000,"Stanley 2")
    t.addPlayer(p1)
    t.addPlayer(p2)
    print("")
    for i in range(0,2):
        print("Round "+str(i))
        t.round()

