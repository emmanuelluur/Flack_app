const post = (url, data) => {
    return new Promise((resolve, reject) => {
      let request = new XMLHttpRequest();
      request.open('POST', url, true);
      request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
          resolve(this.responseText);
        }
      }
      request.onerror = function () {
        reject(Error("Network Error"));
      };

      request.send(data);
    })
  }
