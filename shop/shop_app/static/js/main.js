document.addEventListener('DOMContentLoaded', function () {
    const quantityForms = document.querySelectorAll('.input-group.quantity');

    quantityForms.forEach(form => {
        const quantityInput = form.querySelector('.form-control');
        const btnMinus = form.querySelector('.btn-minus');
        const btnPlus = form.querySelector('.btn-plus');

        btnMinus.addEventListener('click', function () {
            if (quantityInput.value > 1) {
                quantityInput.value--;
            }
        });

        btnPlus.addEventListener('click', function () {
            quantityInput.value++;
        });
    });
});


