/**
 * Created by ian on 4/13/17.
 */


function IsoMQ(url, channel){
    var _this = this;
    this.url = "wss://" + url + "/" + channel;
    console.log(this.url);
    this.socket = new WebSocket(this.url);
    this.socket.onerror = this.onerror;
    this.socket.onmessage = function (event) {
        try{
            var payload = JSON.parse(event.data);
            _this.onmessage(payload);

        }catch (e){
            _this.onerror(e);
        }
    };
    this.socket.onopen = function () {
        console.log("Connection opened");
    }
}

IsoMQ.prototype.send = function (data) {
    var payload = null;
    try{
        payload = JSON.stringify(data);
    }catch (e){
        payload = JSON.stringify({data:new Blob(data)});
    }
    this.socket.send(payload);
};