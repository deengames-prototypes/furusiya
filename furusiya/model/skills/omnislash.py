from game import Game


class OmniSlash:
    @staticmethod
    def process(player, target, conf):
        # do guaranteed hits
        for _ in range(conf.guaranteedHits):
            if Game.fighter_system.has(target):
                Game.fighter_system.get(player).attack(target)
            else:
                return  # it's dead already!

        # do lucky hits
        while True:
            should_re_hit = Game.random.randint(0, 100) <= conf.probabilityOfAnotherHit
            if should_re_hit and Game.fighter_system.has(target):
                Game.fighter_system.get(player).attack(target)
            else:
                return

