let canvas;
let context;
let width;
let main;
let size;
let interval_id;

let score_box;
let level_box;
let health_bar;
let score;
let level;
let grid;
let grid_size = 27;
let monsters = [];

let player = {
    x : 13,
    y : 13,
    health : 100,
    move_up : false,
    move_down :  false,
    move_left : false,
    move_right : false,
    silver_key : false,
    gold_key : false,
    sprite : 0,
}
let monster = {
    x : 3,
    y : 2,
    damage : 5,
    move_up : false,
    move_down :  true,
    move_left : false,
    move_right : false,
}

let sprites;
let audio;

document.addEventListener('DOMContentLoaded', init, false);

function init() {
    canvas = document.querySelector('canvas');
    context = canvas.getContext('2d');
    level_box = document.getElementById('level');
    score_box = document.getElementById('score');
    health_bar = document.getElementById('health');
    main = document.querySelector('main');
    width = 0.75 * Math.min(window.innerWidth, window.innerHeight);
    canvas.height = canvas.width = width;
    audio = document.querySelector('audio');
    grid = new_grid();
    sprites = new Image();
    sprites.src = 'media/sprites.png';
    size = width / grid_size;
    level = 1;
    score = 0;
    update_score(0)
    change_level();
    interval_id = window.setInterval(draw, 100);
    window.addEventListener('keydown', activate, false);
    window.addEventListener('keyup', deactivate, false);
}

function draw() {
    context.clearRect(0, 0, width, width);
    build();
    move(player);
    move(monster);
    damage(monster);
}

function build() {
    for (let i = 0; i < grid_size; i += 1) {
        for (let j = 0; j < grid_size; j += 1) {
            let value = grid[j][i];
            if (value === 1) {
               // wall
               context.drawImage(sprites, 0, 0, 16, 16, size*i, size*j, size, size)
           } else if (value === 0) {
               // floor
               context.drawImage(sprites, 16, 0, 16, 16, size*i, size*j, size, size)
           } else if (value === 5) {
                // player
                context.drawImage(sprites, player.sprite, 48, 16, 16, size*i, size*j, size, size)
            } else if (value === 4) {
                // skeleton
                context.drawImage(sprites, 0, 64, 16, 16, size*i, size*j, size, size)
            } else if (value === 3 || value === 2) {
                // keys
                context.drawImage(sprites, 0, 32, 16, 16, size*i, size*j, size, size)
            } else if (value === 8) {
                // coins
                context.drawImage(sprites, 16, 32, 16, 16, size*i, size*j, size, size)
            } else if (value === 10) {
                // scroll
                context.drawImage(sprites, 16, 64, 16, 16, size*i, size*j, size, size)
            } else if (value === 6) {
                if (player.silver_key) {
                    // open the door
                    context.drawImage(sprites, 16, 16, 16, 16, size*i, size*j, size, size)
                    grid[j][i] = 7
                } else {
                    // closed door
                    context.drawImage(sprites, 0, 16, 16, 16, size*i, size*j, size, size)
                }
            } else if (value === 9) {
                if (player.gold_key) {
                    // open the door
                    context.drawImage(sprites, 16, 16, 16, 16, size*i, size*j, size, size)
                    grid[j][i] = 7
                } else {
                    //second closed door
                    context.drawImage(sprites, 0, 16, 16, 16, size*i, size*j, size, size)
                }
            } else if (value === 7) {
                // open door
                context.drawImage(sprites, 16, 16, 16, 16, size*i, size*j, size, size)
            }
        }
    }
}
function move(character) {
    if (character.move_up) {
        let nextx = character.x
        let nexty = character.y-1
        let next = grid[nexty][nextx];
        if (next !== 1 && next !== 6 && next !== 9) {
            check_around(next, nextx, nexty);
            grid[character.y][character.x] = 0;
            character.y -= 1;
        } else if (character !== player) {
            character.move_up = false;
            character.move_down = true;
        }
    } else if (character.move_down) {
        let nextx = character.x;
        let nexty = character.y+1;
        let next = grid[nexty][nextx];
        if (next !== 1 && next !== 6 && next !== 9) {
            check_around(next, nextx, nexty);
            grid[character.y][character.x] = 0;
            character.y += 1;
        } else if (character !== player) {
            character.move_down = false;
            character.move_up = true;
        }
    } else if (character.move_left) {
        let nextx = character.x-1;
        let nexty = character.y;
        let next = grid[nexty][nextx];
        if (next !== 1 && next !== 6 && next !== 9) {
            check_around(next, nextx, nexty);
            grid[character.y][character.x] = 0;
            character.x -= 1;
        } else if (character !== player) {
            character.move_left = false;
            character.move_right = true;
        }
    } else if (character.move_right) {
        let nextx = character.x+1;
        let nexty = character.y;
        let next = grid[nexty][nextx];
        if (next !== 1 && next !== 6 && next !== 9) {
            check_around(next, nextx, nexty);
            grid[character.y][character.x] = 0;
            character.x += 1;
        } else if (character !== player) {
            character.move_right = false;
            character.move_left = true;
        }
    }
    if (character === player) {
        // if (next !== 7) {
            grid[character.y][character.x] = 5
        // }
    } else {
        grid[character.y][character.x] = 4
    }
}
function check_around(next_pos) {
    if (next_pos === 10) {
        // scroll
        update_score(player.health);
        player.move_down = false;
        player.move_up = false;
        player.move_left = false;
        player.move_right = false;
        window.alert('You would have WON!\nScore: ' + score)
        audio.pause();
        stop();
    } else if (next_pos === 2) {
        // key 1
        player.silver_key = true;
        update_score(5);
    } else if (next_pos === 3) {
        // key 2
        player.gold_key = true;
        update_score(10);
    } else if (next_pos === 8) {
        // coin
        update_score(25);
    }
}
function damage(character) {
    for (let y = player.y-1; y < player.y+2; y += 1) {
        for (let x = player.x-1; x < player.x+2; x += 1) {
            if (grid[y][x] === 4) {
                if (player.health-character.damage < 0) {
                    health_bar.value = 0;
                    window.alert('GAME OVER\nScore: ' + score);
                    stop();
                } else {
                    player.health -= character.damage;
                    health_bar.value = player.health;
                }
            }
        }
    }
}
function change_level() {
    grid = new_grid();
    monster.x = 3;
    monster.y = 2;
    monster.damage = 10;
    monster.move_up = false;
    monster.move_down = true;
    monster.move_left = false;
    monster.move_right = false;
    grid[monster.y][monster.x] = 4;
    player.x = 13;
    player.y = 13;
    player.health = 100;
    player.sprite = 0;
    player.silver_key = false;
    player.gold_key = false;
    player.move_up = false;
    player.move_down = false;
    player.move_left = false;
    player.move_right = false;
    grid[player.y][player.x] = 5;
    health_bar.value = player.health
}
function update_score(value) {
    score += value;
    score_box.innerHTML = score;
}
function stop() {
    clearInterval(interval_id);
    window.removeEventListener('keydown', activate);
    window.removeEventListener('keyup', deactivate);
    init();
}
function activate(event) {
    if (!player.move_left && !player.move_up && !player.move_right && !player.move_down) {
        audio.play();
    }
    let KeyCode = event.keyCode;
    if (KeyCode === 37) {
        player.move_left = true;
        player.sprite = 0;
    } else if (KeyCode === 38) {
        player.move_up = true;
    } else if (KeyCode === 39) {
        player.move_right = true;
        player.sprite = 16;
    } else if (KeyCode === 40) {
        player.move_down = true;
    }
}
function deactivate(event) {
    let KeyCode = event.keyCode;
    if (KeyCode === 37) {
        player.move_left = false;
    } else if (KeyCode === 38) {
        player.move_up = false;
    } else if (KeyCode === 39) {
        player.move_right = false;
    } else if (KeyCode === 40) {
        player.move_down = false;
    }
}
function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
function new_grid() {
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],
      [1, 1, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],
      [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 3, 1, 1],
      [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],
      [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
      [1, 1, 0, 0, 0, 6, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 9, 0, 10, 1],
      [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
      [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 8, 0, 0, 1, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 0, 8, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 8, 0, 1, 0, 8, 0, 1, 1],
      [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 8, 0, 0, 1, 1, 1],
      [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
}
