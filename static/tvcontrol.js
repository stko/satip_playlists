
/**
* Class to manage the websocket communications
*/

class TVControl {

  constructor() {

    messenger.register(
      "tvcontrol_",
      this.messenger_onMessage,
      this.messenger_onWSConnect,
      this.messenger_onWSClose
    );
    this.room = "";
  }

  messenger_onMessage(type, data) {
    console.log("incoming message to app", type, data);
    if (type == "app_user_message") {
      this.user_message = data.user_message;
      this.user_button_text = data.user_button_text;
      this.snackbar = true;
    }
    if (type == "tvcontrol_list_response") {
      if (data.rooms) {
        const room_list = document.getElementById("roomlist");
        room_list.innerHTML = "";
        data.rooms.forEach((room) => {
          let li = document.createElement("li");
          li.innerText = room;
          li.onclick = () => {
            this.room = room;
            messenger.emit('tvcontrol_get_list', { "room": this.room });
          };
          room_list.appendChild(li);
        });
      } else if (data.stations) {
        const channel_list = document.getElementById("channellist");
        channel_list.innerHTML = "";
        for (const station_name in data.stations) {
          let li = document.createElement("li");
          li.appendChild(document.createElement("station-logo"));
          const name_elem = document.createElement("station-name");
          name_elem.innerText = station_name;
          li.appendChild(name_elem);
          li.onclick = () => {
            messenger.emit('tvcontrol_play_station', { "url": data.stations[station_name].url });
          };
          channel_list.appendChild(li);
        }
      }
    }
  }

  messenger_onWSConnect() {
    messenger.emit('tvcontrol_get_list', { "room": this.room });
  }

  showDisconnect(disconnected) {
    console.log("websocket disconnect?:", disconnected);
  }
  messenger_onWSClose() {
  }

}

const remotecontrol = new TVControl()

