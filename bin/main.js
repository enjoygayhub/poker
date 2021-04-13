window.onload = WebSocketTest();
var flag=true;  //可行动标记
var ws;  //websocket
var robot = { win: 0, money: 20000, bet: 0, position: 'bigblind', reset: function () { this.money = 20000; this.bet = 0; } };
var player = { win: 0, money: 20000, bet: 0, position: 'smallblind', reset: function () { this.money = 20000; this.bet = 0; } };
var table = { state: 'preflop', pot: 0, act: '', reset: function () { this.state = 'preflop'; this.pot = 0; this.act = ''; } };

function refresh() {
    document.getElementById('aiwin').innerHTML = robot.win;
    document.getElementById('aimoney').innerHTML = robot.money;
    document.getElementById('aibet').innerHTML = robot.bet;
    document.getElementById('humanwin').innerHTML = player.win;
    document.getElementById('humanmoney').innerHTML = player.money;
    document.getElementById('humanbet').innerHTML = player.bet;
    document.getElementById('state').innerHTML = table.state;
    document.getElementById('pot').innerHTML = table.pot;
    document.getElementById('act').innerHTML = table.act;
}

function WebSocketTest() {
    if ("WebSocket" in window) {
        // 打开一个 web socket
        ws = new WebSocket("ws://127.0.0.1:80");

        // 连接建立后的回调函数
        ws.onopen = function () {
            // Web Socket 已连接上，使用 send() 方法发送数据
            console.log('链接成功')
            ws.send("admin:123456");
            console.log("已发送：admin:123456");
        };

        // 接收到服务器消息后的回调函数
        ws.onmessage = function (evt) {
            var received_msg = evt.data;
            console.log("收到消息：" + received_msg);
            let mess = received_msg.split('|')
            switch (mess[0]) {
                case 'preflop':
                    robot.reset(); player.reset();
                    table.reset();
                    if (mess[1] == 'SMALLBLIND') {
                        robot.bet += 100; robot.money -= robot.bet; robot.position = 'bigblind';
                        player.bet += 50; player.money -= player.bet; player.position = 'smallblind';
                        
                    }
                    else {
                        robot.bet += 50; robot.money -= robot.bet; robot.position = 'smallblind';
                        player.bet += 100; player.money -= player.bet; player.position = 'bigblind';
                    }
                    document.getElementById('position1').src = 'images/' + robot.position + 'Puck.png';
                    document.getElementById('position2').src = 'images/' + player.position + 'Puck.png';
                    openCard('card1', mess[2], mess[3]);
                    openCard('card2', mess[4], mess[5]);
                    refresh();
                    break;
                case 'flop':
                    table.state='flop';
                    computePot();
                    refresh()
                    openCard('card3', mess[1], mess[2]);
                    openCard('card4', mess[3], mess[4]);
                    openCard('card5', mess[5], mess[6]);
                    

                    break;
                case 'turn':
                    table.state='turn';
                    computePot();
                    refresh()
                    openCard('card6', mess[1], mess[2]);
                    
                    break;
                case 'river':
                    table.state='river';
                    computePot();
                    refresh()
                    openCard('card7', mess[1], mess[2]);
                    break;
                case 'earnChips': 
                    let winmoney = Number(mess[1]);

                    if(winmoney===0){
                        document.getElementById('act').innerHTML = '平局';
                    }
                    else if(winmoney>0){
                        document.getElementById('act').innerHTML = 'player won '+winmoney;
                    }
                    else{
                        document.getElementById('act').innerHTML = 'player won '+winmoney ;
                    }
                    player.win+=winmoney;
                    robot.win-=winmoney;
                    setTimeout(rotateAllCard, 4000);
                    break;
                case 'oppo_hands':
                    openCard('card8', mess[1], mess[2]);
                    openCard('card9', mess[3], mess[4]);
                    break;
                case 'call':
                    table.act = 'robot call!';
                    robot.money=player.money;
                    robot.bet=player.bet;
                    refresh();

                default:console.log('fefault deal');
            }

        };

        // 连接关闭后的回调函数
        ws.onclose = function () {
            console.log("连接已关闭...");
        };
    }
    else {
        console.log("您的浏览器不支持 WebSocket!");
    }
}


function send_raise() {
    if (!flag) {
        return
    }
    console.log("send_raise")
    let bet = document.getElementById("bet").value;

    if (bet == "" || isNaN(parseInt(bet))) {
        
        document.getElementById("act").innerHTML = "请输入正确数值"
        return
    }
    bet = parseInt(bet);
    player.money-=bet;
    player.bet+=bet;
    refresh();
    var msg = 'raise '+bet;
    ws.send(msg)
    // flag = false
};

function send_call() {
    if (!flag) {
        return
    }
    player.money=robot.money;
    player.bet=robot.bet;
    console.log("send_call");
    var msg = "call";
    ws.send(msg);
    // flag = false
};
function send_fold() {
    if (!flag) {
        return
    }
    
    console.log("sendfold");
    var msg = "fold";
    ws.send(msg);
    // flag = false
};

function rotateAllCard() {
    let cover = document.getElementsByClassName('cover')
    let back = document.getElementsByClassName('back')
    for (i = 0; i < cover.length; i++) {
        cover[i].style.transform = 'rotatey(0deg)';
        back[i].style.transform = 'rotatey(-180deg)';
    }
    console.log("rotateall");
};
function openCard(cardname, color, num) {
    document.getElementById(cardname).src = 'sourse/' + color + num + '.png';
    var card = document.getElementById(cardname + 'cover')
    var back = document.getElementById(cardname + 'back')
    card.style.transform = 'rotatey(180deg)';
    back.style.transform = 'rotatey(0deg)';
    console.log('rotate' + cardname);

};
function computePot() {
    table.pot+=(robot.bet+player.bet);
    robot.bet=0;
    player.bet=0;
}


