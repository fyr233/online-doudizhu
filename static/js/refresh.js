var publicmessage = '';
var playerstate = '';
var playerscore = '';
var playerrole = '';
var playercards = [];
var lastcards = [];
var Lplayername = '';
var Lplayercardsamount = 1;
var Rplayername = '';
var Rplayercardsamount = 1;

//canvas.js中的变量
var maincanvas = document.getElementById("maincanvas");
var cachecanvas = document.createElement("canvas");
var ctx = maincanvas.getContext("2d");
var cachectx = cachecanvas.getContext("2d");
var actorsArr = [];
var actorsArrArr = [];
var R = {};


var getJSON = function(url, params) {
    return new Promise(function(resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.open('post', url, );//true);
      xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      xhr.responseType = 'json';
      xhr.onload = function() {
        var status = xhr.status;
        if (status == 200) {
          resolve(xhr.response);
        } else {
          reject(status);
        }
      };
      xhr.send(params);
    });
};

function refresh(){
    let params = 'roomid='+roomid+'&playerid='+playerid;
    getJSON('/refresh', params).then(function(data) {
        //alert('Your Json result is:  ' + data['roomname']); //you can comment this, i used it to debug
        publicmessage = data['publicmessage'];
        playerstate = data['playerstate'];
        playerscore = data['playerscore'];
        playerrole = data['playerrole'];
        playercards = JSON.parse(data['playercards']);
        lastcards = JSON.parse(data['lastcards']);
        Lplayername = data['Lplayername'];
        Lplayercardsamount = parseInt(data['Lplayercardsamount']);
        Rplayername = data['Rplayername'];
        Rplayercardsamount = parseInt(data['Rplayercardsamount']);

        $("#publicmessage").text('系统消息：'+publicmessage);
        $("#playerstate").text('您的状态：'+playerstate);
        $("#playerscore").text('您的分数：'+playerscore);
        $("#playerrole").text('您的角色：'+playerrole);
        $("#playercards").text('您的牌：'+playercards);
        $("#lastcards").text('之前的牌：'+lastcards);
        $("#Lplayername").text('上家：'+Lplayername);
        $("#Lplayercardsamount").text('上家还剩：'+Lplayercardsamount+'张');
        $("#Rplayername").text('下家：'+Rplayername);
        $("#Rplayercardsamount").text('下家还剩：'+Rplayercardsamount+'张');

    }, function(status) { //error detection....
      //alert('Something went wrong.');
    });

    setTimeout('refresh()', 1000);
}

if (roomid >= 0)
    refresh();

function readypost() {
    let params = 'roomid='+roomid+'&playerid='+playerid;
    getJSON('/ready', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
        
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
}

function grabpost() {
    let params = 'roomid='+roomid+'&playerid='+playerid+'&choice=1';
    getJSON('/grab', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
        
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
}

function notgrabpost() {
    let params = 'roomid='+roomid+'&playerid='+playerid+'&choice=0';
    getJSON('/grab', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
        
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
}

function outpost() {
    var selectedcards = [];
    for (var i=0; i<actorsArrArr[2].length; i++)
    {
      if (actorsArrArr[2][i].selected)
      {
        selectedcards.push(actorsArrArr[2][i].imgname);
      }
    }
    if (selectedcards.length===0)
      return;
    let params = 'roomid='+roomid+'&playerid='+playerid+'&cards=['+String(selectedcards)+']';
    getJSON('/out', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
}

function passpost() {
    let params = 'roomid='+roomid+'&playerid='+playerid;
    getJSON('/pass', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
        
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
}

function quitpost() {
    let params = 'roomid='+roomid+'&playerid='+playerid;
    getJSON('/quit', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
        
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
}