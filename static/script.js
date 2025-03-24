const quizData = [
    { question: "Hva står IT for", options: ["Informasjonsteknologi", "Internett-teknologi", "Internasjonal transport", "Intelligent teknologi"], answer: "Informasjonsteknologi" },
    { question: "Hva brukes en harddisk til?", options: ["Lagring av data", "Kjøring av programmer", "Internett-tilkobling", "Strømforsyning"], answer: "Lagring av data" },
    { question: "Hva er hovedoppgaven til en CPU?", options: ["Vise bilder på skjermen", "Koble til Wi-Fi", "Lagring av filer", "Behandle data og kjøre programmer"], answer: "Behandle data og kjøre programmer" }
];

let currentQuestion = 0;
let score = 0;

function loadQuestion() {
    const questionElement = document.getElementById("question");
    const optionsDiv = document.getElementById("options");

    if (currentQuestion >= quizData.length) {
        questionElement.innerText = "Quiz Over! Final Score: " + score;
        optionsDiv.innerHTML = "";
        return;
    }
    
    const q = quizData[currentQuestion];
    questionElement.innerText = q.question;
    
    optionsDiv.innerHTML = "";
    
    q.options.forEach(option => {
        const button = document.createElement("button");
        button.innerText = option;
        button.classList.add("option");
        button.onclick = () => checkAnswer(option);
        optionsDiv.appendChild(button);
    });
}

function checkAnswer(selectedOption) {
    if (selectedOption === quizData[currentQuestion].answer) {
        score += 1;
        document.getElementById("score").innerText = score;
    }
    currentQuestion++;
    loadQuestion();
}

loadQuestion();


// Hent score fra URL


