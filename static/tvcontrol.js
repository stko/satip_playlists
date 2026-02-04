
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
          let tr = document.createElement("tr");
          tr.appendChild(document.createElement("td"));
          const name_elem = document.createElement("td");
          name_elem.innerText = station_name;
          name_elem.onclick = () => {
            messenger.emit('tvcontrol_play_station', { "type": "live", "url": data.stations[station_name].url });
          };
          tr.appendChild(name_elem);
          channel_list.appendChild(tr);
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

  mediathek() { }
}

const remotecontrol = new TVControl()

