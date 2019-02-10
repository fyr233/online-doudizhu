var publicmessage = '';
var playerstate = '';
var playerscore = '';
var playerrole = '';
var playercards = '';
var lastcards = '';
var Lplayername = '';
var Lplayercardsamount = '';
var Rplayername = '';
var Rplayercardsamount = '';

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
        playercards = data['playercards'];
        lastcards = data['lastcards'];
        Lplayername = data['Lplayername'];
        Lplayercardsamount = data['Lplayercardsamount'];
        Rplayername = data['Rplayername'];
        Rplayercardsamount = data['Rplayercardsamount'];

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

$("#ready").click(function () {
    let params = 'roomid='+roomid+'&playerid='+playerid;
    getJSON('/ready', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
        
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
});

$("#grab").click(function () {
    let params = 'roomid='+roomid+'&playerid='+playerid+'&choice=1';
    getJSON('/grab', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
        
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
});

$("#notgrab").click(function () {
    let params = 'roomid='+roomid+'&playerid='+playerid+'&choice=0';
    getJSON('/grab', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
        
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
});

$("#out").click(function () {
    if ($("#outcards").val()!='')
    {
      let params = 'roomid='+roomid+'&playerid='+playerid+'&cards='+$("#outcards").val();//未完成
      getJSON('/out', params).then(function(data) {
          //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug

      }, function(status) { //error detection....
        alert('Something went wrong.');
      });
    }
});

$("#pass").click(function () {
    let params = 'roomid='+roomid+'&playerid='+playerid;
    getJSON('/pass', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
        
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
});

$("#quit").click(function () {
    let params = 'roomid='+roomid+'&playerid='+playerid;
    getJSON('/quit', params).then(function(data) {
        //alert('Your Json result is:  ' + data); //you can comment this, i used it to debug
        
    }, function(status) { //error detection....
      alert('Something went wrong.');
    });
});