

function closeEditModal(){

    document.getElementById("editModal").style.display="none";

}


document.addEventListener("DOMContentLoaded", function () {

    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(button => {

        button.addEventListener("click", function () {

            const deleteUrl = this.dataset.url;

            Modal.confirm({

                title: "Delete Category",

                message: "Are you sure you want to delete this category? This action cannot be undone.",

                confirmText: "Delete",

                onConfirm() {

                    window.location.href = deleteUrl;

                }

            });

        });

    });
    const editButtons = document.querySelectorAll(".edit-btn");

        editButtons.forEach(button=>{

        button.addEventListener("click",function(){

        const id=this.dataset.id;

        const name=this.dataset.name;

        const image=this.dataset.image;

        const editUrl = this.dataset.url;

        Modal.form({

            title:"Edit Category",

            icon:"✏️",

            html:`

<form
id="editCategoryForm"
method="POST"
action="${editUrl}"
enctype="multipart/form-data">

<input
type="hidden"
name="csrfmiddlewaretoken"
value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">

<div class="form-group">

<label>Category Name</label>

<input
type="text"
name="category_name"
value="${name}"
required>

</div>

<div class="form-group">

<label>Current Image</label>

<br>

<img
src="/media/${image}"
style="width:100px;border-radius:10px;margin:10px 0;">

</div>

<div class="form-group">

<label>New Image</label>

<input
type="file"
name="category_image">

</div>

<div style="margin-top:20px">

<button
type="button"
class="cancel-btn"
onclick="Modal.close()">

Cancel

</button>

<button
type="submit"
class="confirm-btn">

Update

</button>

</div>

</form>

`

        });

    });

});

});
