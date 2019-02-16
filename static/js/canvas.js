//canvas.js



function canvasresize()
{
    let winW = $(window).width();
    let winH = $(window).height();
    if (winW/winH >= 1920/1080)
    {
        $("#maincanvas").attr("height", winH);
        $("#maincanvas").attr("width", Math.floor(winH*1920/1080));
        cachecanvas.height = winH;
        cachecanvas.width = Math.floor(winH*1920/1080);
    }
    else
    {
        $("#maincanvas").attr("width", winW);
        $("#maincanvas").attr("height", Math.floor(winW*1080/1920));
        cachecanvas.width = winW;
        cachecanvas.height = Math.floor(winW*1080/1920);
    }
}

canvasresize();
$(window).resize(function(){
    canvasresize();
});

var xhr = new XMLHttpRequest();
var alreadyloadnumber = 0;
xhr.onreadystatechange = function()
{
    if (xhr.readyState === 4)
    {
        var R_Obj = JSON.parse(xhr.responseText);
        ctx.clearRect(0, 0, maincanvas.width, maincanvas.height);
        ctx.font = "30px 黑体";
        ctx.fillStyle = "#FFFFFF";
        ctx.fillText("正在加载", maincanvas.width/2-50, maincanvas.height/2);
        for (var i = 0; i < R_Obj.images.length; i++)
        {
            R[R_Obj.images[i].name] = new Image();
            R[R_Obj.images[i].name].src = R_Obj.images[i].url;
            R[R_Obj.images[i].name].onload = function()
            {
                alreadyloadnumber++;
                if (alreadyloadnumber === R_Obj.images.length)
                {
                    start();
                }
            }
        }
    }
}
xhr.open("get", "/static/Resource.json", true);
xhr.send(null);

function start()
{
    //定时器
    setInterval(function()
        {
            cachectx.clearRect(0, 0, maincanvas.width, maincanvas.height);
            update();
            for (var i=0; i<actorsArr.length; i++)
            {
                if (actorsArr[i].active)
                {
                    actorsArr[i].render();
                }
            }
            for (var i=0; i<actorsArrArr.length; i++)
            {
                for (var j=0; j<actorsArrArr[i].length; j++)
                {
                    if (actorsArrArr[i][j].active)
                    {
                        actorsArrArr[i][j].render();
                    }
                }
                
            }
            ctx.clearRect(0, 0, maincanvas.width, maincanvas.height);
            ctx.drawImage(cachecanvas, 0, 0);
        }
    ,30);
}

$('#maincanvas').click(function(e){
    var mouseX = (e.pageX - this.offsetLeft)*100/maincanvas.width;
    var mouseY = (e.pageY - this.offsetTop)*100/maincanvas.height;
    //window.alert("click"+mouseX+", "+mouseY);
    
    var b = false;
    for (var j=actorsArrArr.length-1; j>=0; j--)
    {
        for (var i=actorsArrArr[j].length-1; i>=0; i--)
        {
            if (actorsArrArr[j][i].active)
            {
                if (mouseX>actorsArrArr[j][i].clickrange[0] && mouseX<actorsArrArr[j][i].clickrange[0]+actorsArrArr[j][i].clickrange[2] && mouseY>actorsArrArr[j][i].clickrange[1] && mouseY<actorsArrArr[j][i].clickrange[1]+actorsArrArr[j][i].clickrange[3])
                {
                    actorsArrArr[j][i].onclick();
                    b = true;
                    break;
                }
            }
        }
        if (b)
        {
            break;
        }
    }

    for (var i=actorsArr.length-1; i>=0; i--)
    {
        if (actorsArr[i].active)
        {
            if (mouseX>actorsArr[i].clickrange[0] && mouseX<actorsArr[i].clickrange[0]+actorsArr[i].clickrange[2] && mouseY>actorsArr[i].clickrange[1] && mouseY<actorsArr[i].clickrange[1]+actorsArr[i].clickrange[3])
            {
                actorsArr[i].onclick();
                break;
            }
        }
    }
});

function Pic(imgname, x2, y2, w2, h2, x1, y1, w1, h1)//x1, y1, w1, h1是百分比
{
    this.imgname = imgname;
    this.x1 = x1;
    this.y1 = y1;
    this.w1 = w1;
    this.h1 = h1;
    this.x2 = x2;
    this.y2 = y2;
    this.w2 = w2;
    this.h2 = h2;

    this.clickrange = [0, 0, 0, 0];
    this.onclick = function(){};

    this.active = true;

    actorsArr.push(this);
}

Pic.prototype.render = function()
{
    //draw
    cachectx.drawImage(R[this.imgname], this.x2, this.y2, this.w2, this.h2, Math.floor(this.x1/100*maincanvas.width), Math.floor(this.y1/100*maincanvas.height), Math.floor(this.w1/100*maincanvas.width), Math.floor(this.h1/100*maincanvas.height));
}

function PicA(imgname, x2, y2, w2, h2, x1, y1, w1, h1)//x1, y1, w1, h1是百分比
{
    this.imgname = imgname;
    this.x1 = x1;
    this.y1 = y1;
    this.w1 = w1;
    this.h1 = h1;
    this.x2 = x2;
    this.y2 = y2;
    this.w2 = w2;
    this.h2 = h2;

    this.clickrange = [0, 0, 0, 0];
    this.onclick = function(){};

    this.active = true;
}

PicA.prototype.render = function()
{
    //draw
    cachectx.drawImage(R[this.imgname], this.x2, this.y2, this.w2, this.h2, Math.floor(this.x1/100*maincanvas.width), Math.floor(this.y1/100*maincanvas.height), Math.floor(this.w1/100*maincanvas.width), Math.floor(this.h1/100*maincanvas.height));
}

function Text(str, x, y, f)//x,y,f是百分比
{
    this.x = x;
    this.y = y;
    this.f = f;
    this.text = str;
    this.font = "bold "+f/100*maincanvas.height+"px Arial";
    this.fillStyle = "#FFFFFF";

    this.clickrange = [0, 0, 0, 0];
    this.onclick = function(){};

    this.active = true;

    actorsArr.push(this);
}

Text.prototype.render = function()
{
    cachectx.font = this.font;
    cachectx.fillStyle = this.fillStyle;
    cachectx.fillText(this.text, this.x/100*maincanvas.width, this.y/100*maincanvas.height);
}

Bg = new Pic('background', 0, 35, 1400, 856-35, 0, 0, 100, 100);
head1 = new Pic('head1', 0, 0, 200, 200, 3, 14, 10, 17);
head2 = new Pic('head2', 0, 0, 200, 200, 87, 14, 10, 17);
Lname = new Text("等待中", 3, 35, 3);
Rname = new Text("等待中", 87, 35, 3);
upline = new Pic('upline', 0, 0, 1980, 93, 0, 0, 100, 12);

upmsg = new Text("房间："+roomname+" 用户："+playername, 4, 7, 4);
upmsg.fillStyle = "#3F2006";

sysmsg = new Text("系统消息："+publicmessage, 35, 18, 4);

zhunbei = new Pic('zhunbei', 0, 0, 165, 110, 46, 60, 8, 9.2);
zhunbei.clickrange = [46, 60, 8, 9.2];
zhunbei.onclick = function()
{
    readypost();
}

qiang = new Pic('qiang', 0, 0, 165, 110, 40, 60, 8, 9.2);
qiang.clickrange = [40, 60, 8, 9.2];
qiang.active = false;
qiang.onclick = function()
{
    grabpost();
}

buqiang = new Pic('buqiang', 0, 0, 165, 110, 52, 60, 8, 9.2);
buqiang.clickrange = [52, 60, 8, 9.2];
buqiang.active = false;
buqiang.onclick = function()
{
    notgrabpost();
}

chu = new Pic('chu', 0, 0, 165, 110, 40, 60, 8, 9.2);
chu.clickrange = [40, 60, 8, 9.2];
chu.active = false;
chu.onclick = function()
{
    outpost();
}

buchu = new Pic('buchu', 0, 0, 165, 110, 52, 60, 8, 9.2);
buchu.clickrange = [52, 60, 8, 9.2];
buchu.active = false;
buchu.onclick = function()
{
    passpost();
}

actorsArrArr.push([]);
actorsArrArr.push([]);
actorsArrArr.push([]);
actorsArrArr.push([]);

var cardsshift = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
var playercardslen = 0;
var Lplayercardslen = 0;
var Rplayercardslen = 0;

function update()
{
    Lname.text = Lplayername;
    Lname.font = "bold "+Lname.f/100*maincanvas.height+"px Arial";
    Rname.text = Rplayername;
    Rname.font = "bold "+Rname.f/100*maincanvas.height+"px Arial";
    upmsg.text = "房间："+roomname+" 用户："+playername;
    upmsg.font = "bold "+upmsg.f/100*maincanvas.height+"px Arial";
    sysmsg.text = "系统消息："+publicmessage;
    sysmsg.font = "bold "+sysmsg.f/100*maincanvas.height+"px Arial";

    switch(playerstate)
    {
        case "notready":
            zhunbei.active = true;
            qiang.active = false;
            buqiang.active = false;
            chu.active = false;
            buchu.active = false;
            break;
        case "ready":
        case "waiting":
            zhunbei.active = false;
            qiang.active = false;
            buqiang.active = false;
            chu.active = false;
            buchu.active = false;
            break;
        case "grabbing on turn":
            zhunbei.active = false;
            qiang.active = true;
            buqiang.active = true;
            chu.active = false;
            buchu.active = false;
            break;
        case "playing":
            zhunbei.active = false;
            qiang.active = false;
            buqiang.active = false;
            chu.active = true;
            buchu.active = true;
            break;
    }

    if (Lplayercardslen != Lplayercardsamount)
    {
        actorsArrArr[0] = [];
        for (var i=0; i<Lplayercardsamount; i++)
        {
            actorsArrArr[0].push(new PicA('back', 0, 0, 226, 347, 5, 38+3*i, 12, 14));
        }
        Lplayercardslen = Lplayercardsamount;
    }
    
    if (Rplayercardslen != Rplayercardsamount)
    {
        actorsArrArr[1] = [];
        for (var i=0; i<Rplayercardsamount; i++)
        {
            actorsArrArr[1].push(new PicA('back', 0, 0, 226, 347, 84, 38+3*i, 12, 14));
        }
        Rplayercardslen = Rplayercardsamount;
    }

    if (playercardslen != playercards.length)
    {
        actorsArrArr[2] = [];
        for (var i=0; i<playercards.length; i++)
        {
            var p = new PicA(String(playercards[i]), 0, 0, 226, 347, 50-playercards.length*3/2+3*i, 72+cardsshift[i]*2, 7.9, 21.6);
            p.selected = false;
            p.clickrange = [50-playercards.length*3/2+3*i, 72+cardsshift[i]*2, 7.9, 21.6];
            p.onclick = function()
            {
                //window.alert(this.imgname);
                if (this.selected)
                {
                    this.selected = false;
                    this.y1 += 2;
                }
                else
                {
                    this.selected = true;
                    this.y1 -= 2;
                }
            }
            actorsArrArr[2].push(p);
        }
        playercardslen = playercards.length;
    }
    

    actorsArrArr[3] = [];
    for (var i=0; i<lastcards.length; i++)
    {
        actorsArrArr[3].push(new PicA(String(lastcards[i]), 0, 0, 226, 347, 50-lastcards.length*3/2+3*i, 30, 7.9, 21.6));
    }
}