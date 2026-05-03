
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
      } else if (data.livetv) {
        const channel_list = document.getElementById("channellist");
        channel_list.innerHTML = "";
        var channel_counter = 0;
        for (const channel_name in data.livetv) {
          channel_counter += 1;
          const channel = data.livetv[channel_name];
          const tr = document.createElement("tr");
          var td_elem = document.createElement("td");
          td_elem.innerText = String(channel_counter);
          td_elem.classList.add("tv-channel-number");
          tr.appendChild(td_elem);
          td_elem = document.createElement("td")
          td_elem.innerHTML = "&#9654;";
          td_elem.onclick = () => {
            messenger.emit('tvcontrol_play_station', { "type": "live", "url": channel.url });
          };
          td_elem.classList.add("tv-play-button");
          tr.appendChild(td_elem);
          td_elem = document.createElement("td")
          td_elem.innerText = channel.name;
          td_elem.classList.add("tv-channel-name");
          tr.appendChild(td_elem);
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

  power_on_off() {
    messenger.emit('tvcontrol_power_switch', {});
  }
}

const remotecontrol = new TVControl()

