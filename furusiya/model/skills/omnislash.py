from game import Game


class OmniSlash:
    @staticmethod
    def process(player, rehit_percent, delta_coords):
        should_re_hit = Game.random.randint(0, 100) <= rehit_percent
        if should_re_hit:
            player.move_or_attack(*delta_coords)
