document.addEventListener("DOMContentLoaded", function() {
    // Gera um tempo aleatório entre 0 e 20 minutos
    var promoTime = Math.floor(Math.random() * 21);

    // Exibe o tempo inicial no banner
    document.getElementById("promo-timer").innerText = promoTime;

    // Função para atualizar o contador a cada minuto
    function updateTimer() {
        promoTime--;
        if (promoTime >= 0) {
            document.getElementById("promo-timer").innerText = promoTime;
        } else {
            document.querySelector(".promotion-banner").innerText = "Promoção encerrada!";
        }
    }

    // Atualiza o contador a cada minuto (60000 ms)
    setInterval(updateTimer, 60000);
});
