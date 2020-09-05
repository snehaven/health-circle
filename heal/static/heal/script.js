/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

document.addEventListener('DOMContentLoaded', function() {
      document.querySelectorAll('button').forEach(function(button) {
        let old_text = "";
        button.onclick = function() {
          if (document.querySelector(`#button-${button.dataset.id}`).innerText == "Edit") {
            old_text = document.querySelector(`#post-${button.dataset.id}`).innerText;//saves current post text
            document.querySelector(`#button-${button.dataset.id}`).innerText = "Save";//edit button becomes a save button
            //let in_field = document.createElement('input');//creates input element
            //in_field.innerText = old_text;//populate input field with older post
            //document.querySelector(`#post-${button.dataset.id}`).style.color = 'red';
            document.querySelector(`#post-${button.dataset.id}`).style.display = "none";
            document.querySelector(`#post-edit-${button.dataset.id}`).style.display = "block";
            } else {
              document.querySelector(`#post-${button.dataset.id}`).style.color = 'black';
              document.querySelector(`#button-${button.dataset.id}`).innerText = "Edit";
              old_text = document.querySelector(`#post-edit-${button.dataset.id}`).value;
              form = new FormData();
              form.append("id", button.dataset.id);
              form.append("post", old_text);

              fetch("/edit_post/", {
                method: "POST",
                body: form,
              }).then((res) => {
                document.querySelector(`#post-${button.dataset.id}`).textContent = old_text;
                document.querySelector(`#post-${button.dataset.id}`).style.display = "block";
                document.querySelector(`#post-edit-${button.dataset.id}`).style.display = "none";
                document.querySelector(`#post-edit-${button.dataset.id}`).value = old_text;
              });
            }
          }
        });
    });
