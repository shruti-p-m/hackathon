async function uploadVideo() {
    const input = document.getElementById('videoInput');
    if (!input.files.length) return alert("Upload a video first");
  
    const formData = new FormData();
    formData.append("file", input.files[0]);
  
    const res = await fetch('https://your-flask-api-url/upload', {
      method: 'POST',
      body: formData
    });
  
    const data = await res.json();
  
    document.getElementById('transcript').innerText = data.transcript;
    document.getElementById('minutes').innerText = data.meeting_minutes;
    document.getElementById('toneTimeline').innerText = JSON.stringify(data.tone_timeline, null, 2);
    document.getElementById('sentiment').innerText = JSON.stringify(data.sentiment_per_speaker, null, 2);
    document.getElementById('emotion').innerText = JSON.stringify(data.emotion_per_speaker, null, 2);
  }
  
  /* FILE: frontend/style.css */
  body {
    font-family: Arial, sans-serif;
    padding: 2em;
    background: #f7f9fc;
  }
  h1 { color: #333; }
  pre {
    background: #eee;
    padding: 1em;
    border-radius: 5px;
    overflow: auto;
  }
  button {
    padding: 10px 15px;
    font-size: 1em;
    margin-bottom: 1em;
  }
  input[type="file"] {
    margin-bottom: 1em;
  }
  