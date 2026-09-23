document.getElementById("addStaffBtn")
.addEventListener("click", function(){

    document.getElementById("addStaffModal")
    .style.display = "flex";

});

function closeAddStaffModal(){

    document.getElementById("addStaffModal")
    .style.display = "none";

}

window.addEventListener("click", function(event){

    const modal =
        document.getElementById("addStaffModal");

    if(event.target === modal){

        modal.style.display = "none";

    }

});

// ---------- Delete Staff ----------

function openDeleteStaffModal(button){

    document.getElementById("deleteStaffModal").style.display = "flex";

    document.getElementById("confirmDeleteStaffBtn").href =
        button.dataset.url;

}

function closeDeleteStaffModal(){

    document.getElementById("deleteStaffModal").style.display = "none";

}

window.addEventListener("click", function(event){

    const modal =
        document.getElementById("deleteStaffModal");

    if(event.target === modal){

        modal.style.display = "none";

    }

});

document.querySelectorAll(".edit-btn").forEach(function(button){

    button.addEventListener("click", function(){

        document.getElementById("editStaffModal").style.display = "flex";

        document.getElementById("editStaffName").value =
            this.dataset.name;

        document.getElementById("editUsername").value =
            this.dataset.username;

        document.getElementById("editPassword").value =
            this.dataset.password;

        document.getElementById("editSalary").value =
            this.dataset.salary;

        document.getElementById("editStatus").value =
            this.dataset.status === "True"
                ? "True"
                : "False";

        document.getElementById("editStaffForm").action =
            "/owner/edit_staff/" + this.dataset.id + "/";

    });

});

function closeEditStaffModal(){

    document.getElementById("editStaffModal").style.display = "none";

}

window.addEventListener("click", function(event){

    const modal =
        document.getElementById("editStaffModal");

    if(event.target === modal){

        modal.style.display = "none";

    }

});
// ---------- Staff Search ----------

document
.getElementById("staffSearch")
.addEventListener("keyup", function(){

    const value = this.value.toLowerCase();

    document
    .querySelectorAll(".staff-row")
    .forEach(function(row){

        const text =
            row.innerText.toLowerCase();

        row.style.display =
            text.includes(value)
            ? ""
            : "none";

    });

});