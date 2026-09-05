(function () {
  const timer = document.getElementById("countdown");
  if (!timer) return;
  const end = new Date(timer.dataset.endTime).getTime();
  const tick = () => {
    const seconds = Math.max(0, Math.floor((end - Date.now()) / 1000));
    const hh = String(Math.floor(seconds / 3600)).padStart(2, "0");
    const mm = String(Math.floor(seconds % 3600 / 60)).padStart(2, "0");
    const ss = String(seconds % 60).padStart(2, "0");
    timer.textContent = `${hh}:${mm}:${ss}`;
    if (seconds === 0) { document.querySelectorAll("#submission-form input, #submission-form button").forEach(el => el.disabled = true); window.setTimeout(() => window.location.reload(), 700); return; }
    window.setTimeout(tick, 1000);
  };
  tick();
}());
