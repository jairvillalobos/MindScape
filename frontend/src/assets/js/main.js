// Obtén una referencia al elemento de video en tu HTML
let videoElement = document.getElementById("video");
let stopButton = document.getElementById("stopButton");
let playButton = document.getElementById("playButton");

let stream, socket;

playButton.addEventListener("click", () => {
  // Si la transmisión de la cámara ya está activa, no hagas nada
  if (stream && stream.active) return;

  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((mediaStream) => {
      stream = mediaStream;
      videoElement.srcObject = stream;

      // Si el WebSocket está cerrado o no se ha creado aún, ábrelo
      if (!socket || socket.readyState === WebSocket.CLOSED) {
        socket = new WebSocket("ws://localhost:8000/ws");
        socket.addEventListener("message", (event) => {
          // Supongamos que el servidor envía los datos en formato JSON
          let data = JSON.parse(event.data);

          // Crea una nueva imagen y establece su fuente a la imagen recibida del servidor
          let img = new Image();
          img.src = "data:image/jpeg;base64," + data.image;

          // Cuando la imagen se haya cargado, dibújala en el elemento de video
          img.onload = () => {
            let context = videoElement.getContext("2d");
            context.drawImage(img, 0, 0, videoElement.width, videoElement.height);
          };

          // Crea o actualiza un elemento HTML para cada emoción detectada
          let emotionsElement = document.getElementById("emotions");
          emotionsElement.innerHTML = "";
          data.emotions.forEach((emotion, index) => {
            let element = document.createElement("div");
            element.textContent = `Emoción detectada: ${emotion.emotion}`;
            emotionsElement.appendChild(element);
        });
        
        });

        // Cada segundo, toma un frame del video y envíalo al servidor
        setInterval(() => {
          if (socket.readyState === WebSocket.OPEN) {
            let canvas = document.createElement("canvas");
            canvas.width = videoElement.videoWidth;
            canvas.height = videoElement.videoHeight;
            let context = canvas.getContext("2d");
            context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
            let frame = canvas.toDataURL("image/jpeg");
            socket.send(frame);
          }
        }, 1000);
      }
    })
    .catch((err) => {
      console.error("Error accediendo a la cámara: ", err);
    });
});

stopButton.addEventListener("click", () => {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
  }
  if (socket) {
    socket.close();
  }
});
