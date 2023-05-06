function create_boad() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = "green";
    ctx.fillRect(0,0,480,480)

    ctx.strokeStyle = 'black';
    for (let j = 0; j <= 60 * 8; j = j + 60) {
        ctx.strokeRect(j,0,0,480);
        ctx.strokeRect(0,j,480,0);
    }
}

function point_putpotision(x,y) {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    //置ける場所
    ctx.beginPath();
    ctx.arc(30 + 60 * x, 30 + 60 * y, 6, 0, Math.PI * 2, true);
    ctx.fillStyle = "red";
    ctx.fill();
}

function put_black(x,y) {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    //黒
    ctx.beginPath();
    ctx.arc(30 + 60 * x, 30 + 60 * y, 20, 0, Math.PI * 2, true);
    ctx.fillStyle = "black";
    ctx.fill();
}

function put_white(x,y) {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    //白
    ctx.beginPath();
    ctx.arc(30 + 60 * x, 30 + 60 * y, 20, 0, Math.PI * 2, true);
    ctx.fillStyle = "white";
    ctx.fill();
}

function clear() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0,0,480,480)
    create_boad()
}



function click_event() {
    const target = document.getElementById('canvas');
    //クリックイベント
    target.onclick =( evt )=> {
    console.log( `${ Math.floor( evt.offsetX / 60 ) }${ Math.floor( evt.offsetY / 60 ) } ` );
    send_data = `${ Math.floor( evt.offsetX / 60 ) }${ Math.floor( evt.offsetY / 60 ) }`
    $.ajax("/register", {
        type: "post",
        data: {"data": send_data},          
    })
    setTimeout(function() {
        put()
      }, 100); 
    };  
}

var now_board = [];
var old_board = [];
async function update(){
    const url = './get_board';
    const options = { methot: 'GET' };
    const response = await fetch(url, options);
    const data = await response.json();
    now_board = data.board

    if (JSON.stringify(now_board) !== JSON.stringify(old_board)){
        console.log(now_board);
        console.log(old_board);
        put();
        old_board = JSON.parse(JSON.stringify(now_board));
    }
}


async function put(){
    clear()
    const url = './get_board'
    const options = { methot: 'GET' }
    const response = await fetch(url, options);
    const data = await response.json();

    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            if (data.board[i][j] == "b") {
                put_black(i,j)
            }
            else if (data.board[i][j] == "w") {
                put_white(i,j)
            }
            else if (data.board[i][j] == "r") {
                point_putpotision(i,j)
            }
        } 
    }


    document.getElementById("area2").innerText = data.e_message;
    document.getElementById("area3").innerText = data.q_message;
    document.getElementById("area4").innerText = data.end_message;
}
