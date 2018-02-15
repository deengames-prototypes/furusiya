import random


class OmniSlash:
    @staticmethod
    def process(player, rehit_percent, delta_coords):
        should_re_hit = random.randint(0, 100) <= rehit_percent
        if should_re_hit:
            player.move_or_attack(*delta_coords)
