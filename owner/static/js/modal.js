const Modal = {

    overlay: document.getElementById("appModal"),

    title: document.getElementById("modalTitle"),

    icon: document.getElementById("modalIcon"),

    body: document.getElementById("modalBody"),

    footer: document.getElementById("modalFooter"),

    open() {

        this.overlay.classList.add("show");

    },

    close() {

        this.overlay.classList.remove("show");

        this.body.innerHTML = "";

        this.footer.innerHTML = "";

    },

    confirm(options) {

        this.icon.innerHTML = "⚠️";

        this.title.innerHTML = options.title;

        this.body.innerHTML = `
            <p>${options.message}</p>
        `;

        this.footer.innerHTML = `
            <button class="cancel-btn" id="modalCancelBtn">
                Cancel
            </button>

            <button class="confirm-btn" id="modalConfirmBtn">
                ${options.confirmText || "Confirm"}
            </button>
        `;

        this.open();

        document
            .getElementById("modalCancelBtn")
            .onclick = () => {

                this.close();

            };

        document
            .getElementById("modalConfirmBtn")
            .onclick = () => {

                this.close();

                if (options.onConfirm) {

                    options.onConfirm();

                }

            };

    },

  form(options) {

    this.icon.innerHTML = options.icon || "✏️";

    this.title.innerHTML = options.title || "";

    this.body.innerHTML = options.html || "";

    this.footer.innerHTML = options.footer || "";

    this.open();

    // Run callback after modal content is inserted
    if (typeof options.onOpen === "function") {
        options.onOpen();
    }

}

};