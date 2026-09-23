function openDeleteProductModal(button){

    document.getElementById("deleteProductModal").style.display = "flex";

    document.getElementById("confirmDeleteBtn").href =
        button.dataset.url;

}

function closeDeleteProductModal(){

    document.getElementById("deleteProductModal").style.display = "none";

}

window.addEventListener("click", function(event){

    const modal = document.getElementById("deleteProductModal");

    if(event.target === modal){

        modal.style.display = "none";

    }

});

document.querySelectorAll(".edit-btn").forEach(function(button){

    button.addEventListener("click", function(){

        document.getElementById("editProductModal").style.display = "flex";

        document.getElementById("editProductName").value =
            this.dataset.name;

        document.getElementById("editCategory").value =
            this.dataset.category;

        document.getElementById("editSection").value =
            this.dataset.section;

        document.getElementById("editDescription").value =
            this.dataset.description;

        document.getElementById("editActualPrice").value =
            this.dataset.actualPrice;

        document.getElementById("editOfferPrice").value =
            this.dataset.offerPrice;

        document.getElementById("editQuantity").value =
            this.dataset.quantity;

        const preview = document.getElementById("editPreview");

            if(this.dataset.image){

                preview.src =
                    "/media/" + this.dataset.image.replace(/\\/g,"/");

                preview.style.display = "block";

            }else{

                preview.style.display = "none";

            }

        document.getElementById("editProductForm").action =
            "/owner/edit_product/" + this.dataset.id + "/";

    });

});
function closeEditProductModal(){

    document.getElementById("editProductModal").style.display = "none";

}
window.addEventListener("click", function(event){

    const modal = document.getElementById("editProductModal");

    if(event.target === modal){

        modal.style.display = "none";

    }

});
document.getElementById("addProductBtn").addEventListener("click", function(){

    document.getElementById("addProductModal").style.display = "flex";

});
function closeAddProductModal(){

    document.getElementById("addProductModal").style.display = "none";

}
window.addEventListener("click", function(event){

    const modal = document.getElementById("addProductModal");

    if(event.target === modal){

        modal.style.display = "none";

    }

});
// ---------------- Product Search ----------------

// ---------------- Product Search & Filter ----------------

const searchInput = document.getElementById("productSearch");

const categoryFilter =
document.getElementById("categoryFilter");

const sectionFilter =
document.getElementById("sectionFilter");

searchInput.addEventListener("keyup", filterProducts);

categoryFilter.addEventListener("change", filterProducts);

sectionFilter.addEventListener("change", filterProducts);

function filterProducts(){

    const searchValue =
        searchInput.value.toLowerCase().trim();

    const selectedCategory =
        categoryFilter.value;

    const selectedSection =
        sectionFilter.value;

    const rows =
        document.querySelectorAll(
            "#productTable tbody tr"
        );

    rows.forEach(function(row){

        const productName =
            row.querySelector(".product-name")
                .textContent
                .toLowerCase();

        const category =
            row.querySelector(".category-name")
                .dataset.category;

        const section =
            row.querySelector(".section-name")
                .dataset.section;

        const searchMatch =
            productName.includes(searchValue);

        const categoryMatch =
            selectedCategory === "" ||
            category === selectedCategory;

        const sectionMatch =
            selectedSection === "" ||
            section === selectedSection;

        if(
            searchMatch &&
            categoryMatch &&
            sectionMatch
        ){

            row.style.display = "";

        }
        else{

            row.style.display = "none";

        }

    });

}