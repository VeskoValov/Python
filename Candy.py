import math
import functools

class Candy:
    def __init__(self, mass, uranium):
        self.mass = mass
        self.uranium = uranium

    @property
    def get_uranium_quantity(self):
        return self.mass * self.uranium

    @property
    def get_mass(self):
        return self.mass

    def __lt__(self, other_candy):
        return self.mass < other_candy.mass

    def __gt__(self, other_candy):
        return self.mass > other_candy.mass


class Person:
    def __init__(self, position):
        self.position = position

    @property
    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def distance(self, other_person):
        return math.sqrt(pow((other_person.position[0] - self.position[0]), 2) +
                         pow((other_person.position[1] - self.position[1]), 2))

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __str__(self):
        return f"This person lives at {self.position}."

    def __repr__(self):
        return f"Person {self.position}."


class Kid(Person):
    def __init__(self, position, initiative):
        super().__init__(position)
        self.initiative = initiative
        self.candy_bag = []
        self._visited_hosts = []

    @property
    def get_initiative(self):
        return self.initiative

    @property
    def visited_hosts(self):
        return self._visited_hosts

    @visited_hosts.setter
    def visited_hosts(self, host):
        self._visited_hosts.append(host)

    def add_candy(self, candy):
        self.candy_bag.append(candy)

    def __str__(self):
        return f"Kid lives at: {self.position} and its initiative is {self.initiative}."

    def __repr__(self):
        return f"Kid({self.position}, {self.initiative})"

    def __lt__(self, other_kid):
        return self.initiative < other_kid.initiative

    def __gt__(self, other_kid):
        return self.initiative > other_kid.initiative

    @property
    def is_critical(self):
        uran = 0
        for _, candy in enumerate(self.candy_bag):
            uran += candy.get_uranium_quantity

        if uran > 20:
            return True
        else:
            return False


class Host(Person):
    def __init__(self, position, candies):
        super().__init__(position)
        self.candies = candies

    def remove_candy(self, f):
        list_of_candies = []
        for _, candy in enumerate(self.candies):
            list_of_candies.append(Candy(candy[0], candy[1]))
        if list_of_candies:
            self.candies.sort(key=lambda x: x[0])
            self.candies.pop()
            return f(list_of_candies)


class FluxCapacitor:
    def __init__(self, participants):
        self.participants = participants

    @property
    def get_victim(self):
        host_list = []
        kid_list = []
        victims = []
        for person in self.participants:
            if type(person) == Host:
                host_list.append(person)
            else:
                kid_list.append(person)
        kid_list.sort(reverse=True)
        current_host = host_list[0]
        while len(kid_list[-1].visited_hosts) != len(host_list) and not victims:
            for kid in kid_list:
                distance = math.inf
                for host in host_list:
                    if distance > kid.distance(host) and host not in kid.visited_hosts:
                        distance = kid.distance(host)
                        current_host = host
                    elif distance == kid.distance(host) and host not in kid.visited_hosts:
                        if current_host.position[0] > host.position[0]:
                            distance = kid.distance(host)
                            current_host = host
                        elif current_host.position[0] == host.position[0] and current_host.positon[1] > host.position[
                            1]:
                            distance = kid.distance(host)
                            current_host = host

                kid.visited_hosts.append(current_host)
                if not current_host.candies:
                    continue
                kid.add_candy(current_host.remove_candy(max))
                if kid.is_critical:
                    victims.append(kid)

        if victims:
            return victims


"""
kid1 = Kid((0, 0), 1)
kid2 = Kid((0, 2), 2)
kid3 = Kid((3, 10), 3)
kid4 = Kid((4, 0), 4)
kid5 = Kid((0, 3), 5)
host1 = Host((0, 4), [(2, 1.0), (10, 0.5)])
host2 = Host((3, 4), [(21, 1.0), (10, 0.5)])
flux_capacitor = FluxCapacitor({kid1, kid2, kid3, kid4, kid5, host1, host2})
print(flux_capacitor.get_victim)
"""


def plus_one(digits: list[int]) -> list[int]:
    l = [x for x in digits]
    l[-1] += 1
    count = 0
    while l[-1] == 10:
        l.pop()
        if not l:
            l.append(1)
            count += 1
            break
        l[-1] += 1
        count += 1

    return l + [0] * count


def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False


def find_words(words: list[str]) -> list[str]:
    first_row = set("qwertyuiop")
    second_row = set("asdfghjkl")
    third_row = set("zxcvbnm")
    result = []
    for word in words:
        letter_set = set(word.lower())
        if letter_set <= first_row or letter_set <= second_row or letter_set <= third_row:
            result.append(word)

    return result


def array_rank_transform(arr: list[int] | list[int]) -> list[int]:
    tuple_list = sorted(enumerate(arr), key=lambda x: x[1])
    rank = 0
    prev_num = 'NaN'
    rank_list = []
    for i, num in tuple_list:
        if prev_num != num:
            prev_num = num
            rank += 1
        rank_list.append((i, rank))

    rank_list.sort()

    return [rank for _, rank in rank_list]


print(array_rank_transform([40, 10, 20, 30]))
