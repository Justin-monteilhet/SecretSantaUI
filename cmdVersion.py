from typing import Callable
from random import choice


def get_input(s:str, check:Callable=None, error:str=None) -> str:
    if all((check, error)):
        i = input(s).strip()
        while not check(i):
            print(error)
            i = input(s).strip()
        return i

    return input(s).strip()

def get_int_input(s:str, error:str='Veuillez entrer un nombre.') -> int:
    user_input = get_input(s)
    while not user_input.isdigit():
        print(error)
        user_input = get_input(s)

    return int(user_input)

def get_names():
    players = list()
    nb = get_int_input('Nombre de joueurs : ')
    for i in range(nb):
        name = get_input(f'Joueur {i+1} : ', check=lambda s:not s in players or not s, error='Ce joueur existe déjà.')
        players.append(name.title())

    return players

def list_to_couples(s:list):
    binomes = {}
    left_players = s.copy()
    for i,p in enumerate(s):
        remove_player = set()
        if i == len(s)-2 and s[i+1] in left_players:
            chosen = s[i+1]
        else:
            available_players = tuple(set(left_players) - {p,} - remove_player)
            chosen = choice(available_players)

        binomes[p] = chosen
        left_players.remove(chosen)

    return binomes

def main_cmd():
    players = get_names()
    binomes = list_to_couples(players)

    print(binomes)

if __name__ == '__main__':
    main_cmd()