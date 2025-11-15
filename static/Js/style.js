// script.js - Posture Pal
document.getElementById('videoInput').addEventListener('change', function (event) {
    const file = event.target.files[0];
    const preview = document.getElementById('video-preview');
    if (file) {
        const url = URL.createObjectURL(file);
        preview.src = url;
        preview.style.display = "block";
    }
});

let count = 0;

function updateCounter(newCount) {
    const counter = document.getElementById('rep-count');
    if (newCount !== count) {
        count = newCount;
        counter.innerText = `Reps: ${count}`;
        counter.classList.add("pop");
        setTimeout(() => counter.classList.remove("pop"), 300);
    }
}
