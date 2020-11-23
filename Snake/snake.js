let storage;
let canvas;
let context;
let width;
let interval_id;

let score_box;
let table;
let tabledata;

let body;
let grid_size = 25;
let grid;
let size;
let half_size;
let snake_size;
let length;
let move_up;
let move_down;
let move_left;
let move_right;

let snake = {
    x : 0,
    y : 0,
    colour : '#ebe9e9',
}
let apple = {
    x : 0,
    y : 0,
    value : 4,
    life : 0,
}

document.addEventListener('DOMContentLoaded', init, false);

function init() {
    storage = window.localStorage;
    canvas = document.querySelector('canvas');
    score_box = document.querySelector('#score');
    table = document.querySelectorAll('#high-score tr');
    tabledata = document.querySelector('#high-score tbody');
    context = canvas.getContext('2d');
    width = 0.95 * Math.min(window.innerWidth, window.innerHeight);
    canvas.height = canvas.width = width;
    size = width / grid_size;
    half_size = size / 2;
    snake_size = size * 0.75;
    leaderboard();
    newGrid();
    snake.x = getRandomNumber(2, 22);
    snake.y = getRandomNumber(2, 22);
    snake.colour = '#ebe9e9';
    apple.x = getRandomNumber(3, 21);
    apple.y = getRandomNumber(3, 21);
    apple.value = 4;
    apple.life = 0;
    body = [];
    length = 1;
    updateScore();
    move_up = false;
    move_down = false;
    move_left = false;
    move_right = false;
    grid[apple.y][apple.x] = 2;
    interval_id = window.setInterval(draw, 100);
    window.addEventListener('keydown', activate, false);
}

function draw() {
    context.clearRect(0, 0, width, width);
    if (move_up) {
        snake.y -= 1;
    } else if (move_down) {
        snake.y += 1;
    } else if (move_left) {
        snake.x -= 1;
    } else if (move_right) {
        snake.x += 1;
    }
    if (collision()) {
        stop();
    }
    checkApple();
    if (move_up || move_down || move_left || move_right) {
        body.push([snake.x, snake.y]);
        grid[snake.y][snake.x] = 1;
    }
    if (body.length > length) {
        let tail = body.shift();
        grid[tail[1]][tail[0]] = 0;
    }
    drawSnake();
}
function collision() {
    if ((snake.x < 0) || (snake.x > grid_size-1) ||
    (snake.y < 0) || (snake.y > grid_size-1)) {
        return true;
    } else if ((grid[snake.y][snake.x] === 1) &&
    (move_up || move_down || move_left || move_right)) {
        return true;
    }
    return false;
}
function stop() {
    window.alert('Game Over :(\nScore: ' + length);
    clearInterval(interval_id);
    window.removeEventListener('keydown', activate);
    add_to_leaderboard();
    init();
}
function add_to_leaderboard() {
    if (length > 1) {
        if (storage.length >= 5) {
            let key = storage.key(4);
            storage.removeItem(key);
        }
        let cur_date = new Date().toLocaleString();
        storage.setItem(length, cur_date);
    }
}
function leaderboard() {
    let clear = document.querySelectorAll("tr + tr");
    for (let i = 0; i < clear.length; i += 1) {
        tabledata.removeChild(tabledata.lastChild);
    }
    if (storage.length > 0) {
        for (let i = 0; i < storage.length; i += 1) {
            let score_value = storage.key(i);
            let date = storage.getItem(score_value);
            createRow(score_value, date);
        }
    } else /*if (table.length < 2)*/ {
        createRow('None', '---');
    }
}
function createRow(col1, col2) {
    let row = document.createElement('tr');
    let data1 = document.createElement('td');
    data1.innerHTML = col1;
    let data2 = document.createElement('td');
    data2.innerHTML = col2;
    row.appendChild(data1);
    row.appendChild(data2);
    tabledata.appendChild(row);
}
function drawSnake() {
    context.fillStyle = snake.colour;
    context.beginPath();
    context.arc(((snake.x*size)+half_size), ((snake.y*size)+half_size), snake_size*0.5, 0, (2*Math.PI));
    context.fill();
    if (length > 1) {
        context.beginPath();
        context.strokeStyle = snake.colour;
        context.lineJoin = 'round';
        context.lineWidth = snake_size;
        context.moveTo((snake.x*size)+half_size, (snake.y*size)+half_size);
        for (let i = body.length-2; i >= 0; i--) {
            let segment = body[i]
            context.lineTo((segment[0]*size)+half_size, (segment[1]*size)+half_size);
        }
        context.stroke();
        context.beginPath();
        context.arc(((body[0][0]*size)+half_size), ((body[0][1]*size)+half_size), snake_size*0.5, 0, (2*Math.PI));
        context.fill();
    }
}
function checkApple() {
    if (apple.life === 1) {
        newApple()
    } else if (grid[snake.y][snake.x] === 2) {
        context.fillStyle = snake.colour;
        context.beginPath();
        context.arc(((snake.x*size)+half_size), ((snake.y*size)+half_size), size*0.7, 0, (2*Math.PI));
        context.fill();
        length += apple.value;
        updateScore();
        newApple();
    }
    if (apple.value > 3) {
        apple.life--;
        if (apple.life % 2 === 0) {
            context.fillStyle = 'rgba(255, 0, 110, 0.25)';
        } else {
            context.fillStyle = 'rgb(255, 0, 110)';
        }
    } else {
        context.fillStyle = '#FFA100';
    }
    context.beginPath();
    context.arc(((apple.x*size)+half_size), ((apple.y*size)+half_size), size*0.4, 0, (2*Math.PI));
    context.fill();
}
function newApple() {
    grid[apple.y][apple.x] = 0;
    apple.x = getRandomNumber(0, grid_size-1);
    apple.y = getRandomNumber(0, grid_size-1);
    while (grid[apple.y][apple.x] === 1) {
        apple.x = getRandomNumber(0, grid_size-1);
        apple.y = getRandomNumber(0, grid_size-1);
    }
    let random = getRandomNumber(1, 5);
    if (random === 5) {
        apple.life = getRandomNumber(20, 45);
        apple.value = 10;
    } else {
        apple.life = 0;
        apple.value = getRandomNumber(1, 3);
    }
    grid[apple.y][apple.x] = 2;
}
function updateScore() {
    score_box.innerHTML = length;
}
function newGrid() {
    grid = []
    for (let i = 0; i < grid_size; i += 1) {
        let new_line = [];
        for (let i = 0; i < grid_size; i += 1) {
            new_line.push(0);
        }
        grid.push(new_line);
    }
}
function activate(event) {
    let KeyCode = event.keyCode;
    if (KeyCode === 37 && !move_right) {
        move_left = true;
        move_up = false;
        move_down = false;
        move_right = false;
    } else if (KeyCode === 38 && !move_down) {
        move_up = true;
        move_down = false;
        move_left = false;
        move_right = false;
    } else if (KeyCode === 39 && !move_left) {
        move_right = true;
        move_up = false;
        move_down = false;
        move_left = false;
    } else if (KeyCode === 40 && !move_up) {
        move_down = true;
        move_up = false;
        move_left = false;
        move_right = false;
    }
}
function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
