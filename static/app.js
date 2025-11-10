
const form = document.getElementById('engageForm');
const result = document.getElementById('result');
const jsonOut = document.getElementById('jsonOut');
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = document.getElementById('text').value;
  if (!text.trim()) { alert('Paste some text to analyze'); return; }
  jsonOut.textContent = 'Analyzing...';
  result.hidden = false;
  try {
    const res = await fetch('/api/engage', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({text})
    });
    const data = await res.json();
    jsonOut.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    jsonOut.textContent = 'Error: ' + err;
  }
});
