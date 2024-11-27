from aim_game.game import game
from aim_game.rule import NumberObj

new_game = game()
obj = NumberObj()
times = 10000
sums = 0
for i in range(times):
    new_game.game_init()
    while new_game.running:
        new_game.start_a_round()
        touzi = new_game.roll(5)
        max_score ,best_way = new_game.best_score(obj,touzi)
        new_game.store(best_way,max_score,touzi)

    sums +=new_game.total_score
    print(new_game.total_score)

print(sums/times)