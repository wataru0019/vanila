class Monster():
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def attack(self):
        print(self.name, 'の攻撃')

new_monster = Monster('スライム', 10)
new_monster.attack()
print(new_monster.name, new_monster.hp)

class Seijika():
    def __init__(self, sex, age, name):
        self.sex = sex
        self.age = age
        self.name = name
    
    @classmethod
    def word(self):
        print('記憶にございません')
    
    def word2(self, word):
        print(f'{word}ということはつまり{word}ということです')

class Jimintou(Seijika):
    def __init__(self, sex, age, name, party):

        super().__init__(sex, age, name)
        self.party = party
    
    @classmethod
    def word3(self, word):
        print(f'{word}? 知らん。誰だそれ？')

if __name__ == '__main__':
    seijika = Seijika('men', 30, 'wataru')
    jimintou = Jimintou('men', 55, 'taro', 'Jimintou')
    seijika.word()
    seijika.word2('辛い')
    jimintou.word3('小寺')