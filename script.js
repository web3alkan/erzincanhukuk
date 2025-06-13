document.addEventListener('DOMContentLoaded', function() {
    const answerButton = document.getElementById('show-answer-btn');
    const answerSection = document.getElementById('answer-section');

    if (answerButton) {
        answerButton.addEventListener('click', function() {
            if (answerSection) {
                answerSection.classList.toggle('visible');
                if (answerSection.classList.contains('visible')) {
                    answerButton.textContent = 'Cevabı Gizle';
                } else {
                    answerButton.textContent = 'Cevabı Göster';
                }
            }
        });
    }
});

function showAnswer() {
    const answerDiv = document.getElementById('answer');
    if (answerDiv.style.display === 'none') {
        answerDiv.style.display = 'block';
    } else {
        answerDiv.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    // Tüm "Testi Bitir" butonlarını seç
    const finishButtons = document.querySelectorAll('.red-button');

    // Her bir butona tıklama olayı ekle
    finishButtons.forEach(button => {
        // Butonun "Testi Bitir" metnini içerip içermediğini kontrol et
        if (button.textContent.trim() === 'Testi Bitir') {
            button.addEventListener('click', function(e) {
                e.preventDefault(); // Varsayılan link davranışını engelle
                const userConfirmed = confirm("Tebrikler, testi tamamladınız! Ana sayfaya dönmek istiyor musunuz?");
                if (userConfirmed) {
                    window.location.href = this.href; // Onaylanırsa linke git
                }
            });
        }
    });
}); 