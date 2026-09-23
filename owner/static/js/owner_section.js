document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".delete-btn").forEach(button => {

        button.addEventListener("click", function () {

            const deleteUrl = this.dataset.url;

            Modal.confirm({

                title: "Delete Section",

                message: "Are you sure you want to delete this section?",

                confirmText: "Delete",

                onConfirm() {

                    window.location.href = deleteUrl;

                }

            });

        });

    });

});
document.querySelectorAll(".edit-btn").forEach(button => {

    button.addEventListener("click", function () {

        const id = this.dataset.id;
        const name = this.dataset.name;
        const rack = this.dataset.rack;
        const editUrl = this.dataset.url;

        Modal.form({

            title: "Edit Section",

            icon: "✏️",

            html: `

<form
method="POST"
action="${editUrl}">

<input
type="hidden"
name="csrfmiddlewaretoken"
value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">

<label>Section Name</label>

<input
type="text"
name="section_name"
value="${name}"
required>

<br><br>

<label>Rack Number</label>

<input
type="text"
name="rack_number"
value="${rack}"
required>

<br><br>

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

</form>

`

        });

    });

});