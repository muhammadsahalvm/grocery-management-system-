document
    .querySelectorAll(".updateStockBtn")
    .forEach(function(button) {

        button.addEventListener("click", function() {

            const modal =
                document.getElementById("updateStockModal");

            const productName =
                document.getElementById("stockProductName");

            const currentStock =
                document.getElementById("currentStock");

            const stockQuantity =
                document.getElementById("stockQuantity");

            const updateForm =
                document.getElementById("updateStockForm");


            /* Open modal */

            modal.style.display = "flex";


            /* Product information */

            productName.textContent =
                this.dataset.name;


            currentStock.textContent =
                this.dataset.stock;


            /* Current quantity */

            stockQuantity.value =
                this.dataset.stock;


            /* Update URL */

            updateForm.action =
                "/staff/update-stock/"
                + this.dataset.id
                + "/";

        });

    });


/* ==========================================
   CLOSE STOCK MODAL
========================================== */

function closeStockModal() {

    document
        .getElementById("updateStockModal")
        .style.display = "none";

}


/* Close button */

const closeStockModalButton =
    document.getElementById("closeStockModal");

if (closeStockModalButton) {

    closeStockModalButton.addEventListener(
        "click",
        closeStockModal
    );

}


/* Cancel button */

const cancelStockUpdate =
    document.getElementById("cancelStockUpdate");

if (cancelStockUpdate) {

    cancelStockUpdate.addEventListener(
        "click",
        closeStockModal
    );

}


/* Click outside modal */

window.addEventListener(
    "click",
    function(event) {

        const modal =
            document.getElementById("updateStockModal");

        if (
            modal &&
            event.target === modal
        ) {

            closeStockModal();

        }

    }
);

/* ==========================================
   CUSTOM FILTER DROPDOWNS
========================================== */

document
    .querySelectorAll(".custom-select")
    .forEach(function(dropdown) {

        const trigger =
            dropdown.querySelector(
                ".custom-select-trigger"
            );

        const valueDisplay =
            dropdown.querySelector(
                ".custom-select-value"
            );

        const hiddenInput =
            dropdown.querySelector(
                'input[type="hidden"]'
            );

        const options =
            dropdown.querySelectorAll(
                ".custom-select-option"
            );


        /* Open / close */

        trigger.addEventListener(
            "click",
            function(event) {

                event.stopPropagation();

                document
                    .querySelectorAll(".custom-select")
                    .forEach(function(otherDropdown) {

                        if (
                            otherDropdown !== dropdown
                        ) {

                            otherDropdown.classList.remove(
                                "open"
                            );

                        }

                    });

                dropdown.classList.toggle("open");

            }
        );


        /* Select option */

        options.forEach(function(option) {

            option.addEventListener(
                "click",
                function(event) {

                    event.stopPropagation();

                    const selectedValue =
                        this.dataset.value;

                    const selectedText =
                        this.textContent.trim();


                    hiddenInput.value =
                        selectedValue;


                    valueDisplay.textContent =
                        selectedText;


                    options.forEach(
                        function(item) {

                            item.classList.remove(
                                "selected"
                            );

                        }
                    );


                    this.classList.add(
                        "selected"
                    );


                    dropdown.classList.remove(
                        "open"
                    );

                }
            );

        });

    });


/* ==========================================
   CLOSE DROPDOWNS OUTSIDE CLICK
========================================== */

document.addEventListener(
    "click",
    function() {

        document
            .querySelectorAll(".custom-select")
            .forEach(function(dropdown) {

                dropdown.classList.remove(
                    "open"
                );

            });

    }
);