document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.rating-stars i');
    const ratingValue = document.querySelector('.rating-value');
    const ratingInput = document.getElementById('review_score');


    function initializeStars() {
        const initialValue = 5;
        ratingInput.value = initialValue;
        ratingValue.textContent = initialValue.toFixed(1);

        stars.forEach((star, index) => {
            if (index < initialValue) {
                star.classList.remove('far');
                star.classList.add('fas', 'active');
            } else {
                star.classList.remove('fas', 'active');
                star.classList.add('far');
            }
        });
    }

    initializeStars();

    stars.forEach(star => {
        star.addEventListener('click', () => {
            const value = parseInt(star.getAttribute('data-value'));
            ratingInput.value = value;
            ratingValue.textContent = value.toFixed(1);

            stars.forEach((s, index) => {
                if (index < value) {
                    s.classList.remove('far');
                    s.classList.add('fas', 'active');
                } else {
                    s.classList.remove('fas', 'active');
                    s.classList.add('far');
                }
            });

            updatePreview();
        });

        star.addEventListener('mouseover', () => {
            const hoverValue = parseInt(star.getAttribute('data-value'));
            stars.forEach((s, index) => {
                if (index < hoverValue) {
                    s.classList.remove('far');
                    s.classList.add('fas');
                } else {
                    s.classList.remove('fas');
                    s.classList.add('far');
                }
            });
        });

        star.addEventListener('mouseout', () => {
            const currentValue = parseInt(ratingInput.value);
            stars.forEach((s, index) => {
                if (index < currentValue) {
                    s.classList.remove('far');
                    s.classList.add('fas', 'active');
                } else {
                    s.classList.remove('fas', 'active');
                    s.classList.add('far');
                }
            });
        });
    });


    const textarea = document.getElementById('review_content');
    const charCounter = document.getElementById('charCounter');

    textarea.addEventListener('input', () => {
        const length = textarea.value.length;
        charCounter.textContent = `${length}/500 caratteri`;

        if (length > 450 && length <= 500) {
            charCounter.classList.add('warning');
            charCounter.classList.remove('error');
        } else if (length > 500) {
            charCounter.classList.remove('warning');
            charCounter.classList.add('error');
        } else {
            charCounter.classList.remove('warning', 'error');
        }


        updatePreview();
    });


    function updatePreview() {
        const previewContent = document.getElementById('previewContent');
        const previewAuthor = document.getElementById('previewAuthor');
        const previewRating = document.getElementById('previewRating');
        const reviewPreview = document.getElementById('reviewPreview');

        const author = document.getElementById('critic_name').value || "Critico";
        const publisher = document.getElementById('publisher_name').value || "Testata";
        const rating = document.getElementById('review_score').value;
        const content = textarea.value || "La tua recensione apparirà qui...";

        if (content.trim() !== "") {
            reviewPreview.style.display = 'block';
            previewContent.textContent = content;
            previewAuthor.textContent = `${author} - ${publisher}`;
            previewRating.textContent = `⭐ ${rating}/5`;
        } else {
            reviewPreview.style.display = 'none';
        }
    }


    document.getElementById('critic_name').addEventListener('input', updatePreview);
    document.getElementById('publisher_name').addEventListener('input', updatePreview);
    ratingInput.addEventListener('input', updatePreview);


    charCounter.textContent = `${textarea.value.length}/500 caratteri`;
});
        const stars = document.querySelectorAll('.rating-stars i');
        const ratingValue = document.querySelector('.rating-value');
        const ratingInput = document.getElementById('review_score');

        stars.forEach(star => {
            star.addEventListener('click', () => {
                const value = parseInt(star.getAttribute('data-value'));
                ratingInput.value = value;
                ratingValue.textContent = value.toFixed(1);

                stars.forEach((s, index) => {
                    if (index < value) {
                        s.classList.remove('far');
                        s.classList.add('fas', 'active');
                    } else {
                        s.classList.remove('fas', 'active');
                        s.classList.add('far');
                    }
                });
            });

            star.addEventListener('mouseover', () => {
                const hoverValue = parseInt(star.getAttribute('data-value'));
                stars.forEach((s, index) => {
                    if (index < hoverValue) {
                        s.classList.remove('far');
                        s.classList.add('fas');
                    } else {
                        s.classList.remove('fas');
                        s.classList.add('far');
                    }
                });
            });

            star.addEventListener('mouseout', () => {
                const currentValue = parseInt(ratingInput.value);
                stars.forEach((s, index) => {
                    if (index < currentValue) {
                        s.classList.remove('far');
                        s.classList.add('fas', 'active');
                    } else {
                        s.classList.remove('fas', 'active');
                        s.classList.add('far');
                    }
                });
            });
        });


        const textarea = document.getElementById('review_content');
        const charCounter = document.getElementById('charCounter');

        textarea.addEventListener('input', () => {
            const length = textarea.value.length;
            charCounter.textContent = `${length}/500 caratteri`;

            if (length > 450 && length <= 500) {
                charCounter.classList.add('warning');
                charCounter.classList.remove('error');
            } else if (length > 500) {
                charCounter.classList.remove('warning');
                charCounter.classList.add('error');
            } else {
                charCounter.classList.remove('warning', 'error');
            }

            updatePreview();
        });


        function updatePreview() {
            const previewContent = document.getElementById('previewContent');
            const previewAuthor = document.getElementById('previewAuthor');
            const previewRating = document.getElementById('previewRating');
            const reviewPreview = document.getElementById('reviewPreview');

            const author = document.getElementById('critic_name').value || "Critico";
            const publisher = document.getElementById('publisher_name').value || "Testata";
            const rating = document.getElementById('review_score').value;
            const content = textarea.value || "La tua recensione apparirà qui...";

            if (content.trim() !== "") {
                reviewPreview.style.display = 'block';
                previewContent.textContent = content;
                previewAuthor.textContent = `${author} - ${publisher}`;
                previewRating.textContent = `⭐ ${rating}/10`;
            } else {
                reviewPreview.style.display = 'none';
            }
        }


        document.getElementById('critic_name').addEventListener('input', updatePreview);
        document.getElementById('publisher_name').addEventListener('input', updatePreview);
        ratingInput.addEventListener('input', updatePreview);


        charCounter.textContent = `${textarea.value.length}/500 caratteri`;