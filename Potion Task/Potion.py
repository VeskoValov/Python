def depleted(effect, count=1):

    def inner(*args, **kwargs):
        nonlocal count
        if count > 0:
            while count > 0:
                effect(*args, **kwargs)
                count -= 1
        else:
            raise TypeError('Effect is depleted!')

    return inner


class Potion:
    def __init__(self, effects: dict[str, callable], duration: float):
        self.effects = effects
        self.duration = duration
        self.intensities = {}
        for name, effect in zip(effects.keys(), effects.values()):
            self.__setattr__(name, depleted(effect))
            self.intensities[name] = 1

    def __add__(self, other):
        for name, effect in zip(other.effects.keys(), other.effects.values()):
            if name in self.__dict__:
                self.intensities[name] += 1
            else:
                self.intensities[name] = 1
            self.__setattr__(name, depleted(effect, self.intensities[name]))
        return self


class Target:
    def __init__(self):
        self.fire_dmg_resistance = 0
        self.water_dmg_resistance = 0
        self.earth_dmg_resistance = 0
        self.air_dmg_resistance = 0
        self.bludgeoning_dmg_resistance = 0
        self.slashing_dmg_resistance = 0
        self.piercing_dmg_resistance = 0
        self.size = 5

    @property
    def get_status(self):
        return self.size




def elemental_dmg_immunity(target):
    target.fire_dmg_resistance = 1.0
    target.water_dmg_resistance = 1.0
    target.earth_dmg_resistance = 1.0
    target.air_dmg_resistance = 1.0


def physical_dmg_immunity(target):
    target.bludgeoning_dmg_resistance = 1.0
    target.slashing_dmg_resistance = 1.0
    target.piercing_dmg_resistance = 1.0


immunity_potion = Potion({'make_elemental_immune': elemental_dmg_immunity,
                          'make_physical_immune': physical_dmg_immunity},
                         duration=1)

effect = {'grow': lambda target: setattr(target, 'size', target.size*2)}

grow_potion = Potion(effect, duration=2)

mixed = grow_potion + grow_potion + grow_potion + immunity_potion + immunity_potion + immunity_potion
d = {'1': 1}
d['1'] += 1
target = Target()

mixed.grow(target)
print(target.size)
