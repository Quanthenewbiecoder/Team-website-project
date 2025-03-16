document.addEventListener("DOMContentLoaded", function () {
    const questions = document.querySelectorAll(".accordion-question");

    questions.forEach(question => {
        question.addEventListener("click", function () {
            console.log("Clicked:", this.innerText); // Debugging log
            const answer = this.nextElementSibling;
            console.log("Answer:", answer); // Debugging log

            if (answer) {
                answer.classList.toggle("open");
            }

            // Close other answers when a new one is clicked
            document.querySelectorAll(".accordion-answer").forEach(otherAnswer => {
                if (otherAnswer !== answer) {
                    otherAnswer.classList.remove("open");
                }
            });
        });
    });
});
