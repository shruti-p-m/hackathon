async function analyzeVideo() {
  const fileInput = document.getElementById('videoUpload');
  const formData = new FormData();
  formData.append('video', fileInput.files[0]);

  const response = await fetch('https://your-render-url.onrender.com/api/analyze', {
    method: 'POST',
    body: formData
  });
  const data = await response.json();
  document.getElementById('results').innerText = JSON.stringify(data, null, 2);
}