let target = [];
let attempts = 9;
const maxAttempts = 9;

const inputs = [
    document.getElementById("number1"),
    document.getElementById("number2"),
    document.getElementById("number3")
];

const resultBox = document.getElementById("results");
const img = document.getElementById("game-result-img");
const submitBtn = document.querySelector(".submit-button");

inputs.forEach((input, index) => {
    input.addEventListener("input", (e) => {
        if (e.target.value.length === 1 && index < 2) inputs[index + 1].focus();
    });
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") check_numbers();
    });
});

function updateAttempts() {
    const attemptsSpan = document.getElementById("attempts");
    if (attemptsSpan) attemptsSpan.textContent = attempts;
}

function initGame() {
    attempts = maxAttempts;
    resultBox.innerHTML = "";
    if (img) img.src = "";
    if (submitBtn) submitBtn.disabled = false;
    
    target = [];
    while (target.length < 3) {
        const n = Math.floor(Math.random() * 10);
        if (!target.includes(n)) target.push(n);
    }
    
    inputs.forEach(i => i.value = "");
    inputs[0].focus();
    updateAttempts();
}

function check_numbers() {
    const values = inputs.map(i => i.value);
    
    if (values.some(v => v === "" || isNaN(v))) {
        inputs.forEach(i => i.value = "");
        inputs[0].focus();
        return;
    }

    const nums = values.map(Number);
    let s = 0;
    let b = 0;

    nums.forEach((n, i) => {
        if (n === target[i]) s++;
        else if (target.includes(n)) b++;
    });

    attempts--;
    updateAttempts();

    const row = document.createElement("div");
    row.style.cssText = `
        display: grid !important;
        grid-template-columns: 1fr 1fr 1fr !important;
        align-items: center !important;
        width: 100% !important;
        padding: 15px 40px !important;
        box-sizing: border-box !important;
        font-size: 30px !important;
        font-weight: bold !important;
    `;

    const left = document.createElement("div");
    left.style.textAlign = "left";
    left.style.whiteSpace = "nowrap"; 
    left.textContent = nums.join("  ");

    const center = document.createElement("div");
    center.style.textAlign = "center";
    center.style.color = "#888";
    center.textContent = ":";

    const right = document.createElement("div");
    right.style.display = "flex";
    right.style.justifyContent = "flex-end";
    right.style.alignItems = "center";
    right.style.gap = "10px";

    if (s === 0 && b === 0) {
        right.innerHTML = `<span class="num-result out">O</span>`;
    } else {
        right.innerHTML = `
            <span style="letter-spacing:0">${s}</span><span class="num-result strike">S</span>
            <span style="letter-spacing:0; margin-left:5px;">${b}</span><span class="num-result ball">B</span>
        `;
    }

    row.appendChild(left);
    row.appendChild(center);
    row.appendChild(right);
    resultBox.prepend(row);

    if (s === 3) {
        if (img) img.src = "success.png";
        if (submitBtn) submitBtn.disabled = true;
        return;
    }

    if (attempts === 0) {
        if (img) img.src = "fail.png";
        if (submitBtn) submitBtn.disabled = true;
        return;
    }

    inputs.forEach(i => i.value = "");
    inputs[0].focus();
}

window.onload = initGame;