function ElementCreator(targetId) {
    this.target = document.getElementById(targetId);
}

ElementCreator.prototype.createElement = function(element, text, color){
    const newElement = document.createElement(element);
    newElement.textContent = text;
    newElement.style.color = color;
    this.target.insertAdjacentElement('beforebegin', newElement);
}

ElementCreator.prototype.addText = function(text){
    this.target.textContent =text;
}

const creator = new ElementCreator('target');

function Pokemon(name, type, skill, cry = 'Meow') {
    this.name = name;
    this.type = type;
    this.skill = skill;
    this.cry = function(){
        console.log(cry);
    }
}

const pikachu = new Pokemon(
    'pikachu',
    'electric',
    [
        {name: 'Thunderbolt', power: 90},
        {name: 'Quick Attack', power: 40},
        {name: 'Iron Tail', power: 100},
        {name: 'Thunder', power: 110}
    ],
    'Pika!'
)

console.log(pikachu)
console.log(pikachu.skill[0]['name'])

document.addEventListener('DOMContentLoaded', function(){
    creator.createElement('h1', 'Hello, World!', 'red');
    creator.createElement('p', 'This is a paragraph.', 'blue');
    creator.createElement('p', pikachu.name, 'green');
    creator.createElement('p', pikachu.type, 'purple');
    for(let i = 0; i < pikachu.skill.length; i++){
        creator.createElement('p',`${pikachu.skill[i]['name']}: ${pikachu.skill[i]['power']}`, 'black');
    }
    pikachu.cry();
})

