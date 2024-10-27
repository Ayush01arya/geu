 const form = document.querySelector("form"),
              nextBtn = form.querySelector(".nextBtn"),
              backBtn = form.querySelector(".backBtn"),
              allInput = form.querySelectorAll(".first input");

        nextBtn.addEventListener("click", () => {
            let isFormValid = true;
            allInput.forEach(input => {
                if (input.value === "") {
                    isFormValid = false;
                }
            });
            if (isFormValid) {
                form.classList.add('secActive');
            } else {
                alert("Please fill all fields in Personal Details.");
            }
        });

        backBtn.addEventListener("click", () => form.classList.remove('secActive'));

        form.addEventListener("submit", (event) => {
            event.preventDefault();

            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });

            fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => {
                        throw new Error(err.error || "Network response was not ok");
                    });
                }
                return response.json();
            })
            .then(result => {
                if (result.message === 'User registered successfully') {
                    alert("Registration successful!");
                    form.reset();
                } else {
                    alert("Registration failed: " + result.message);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred while registering. Please try again.");
            });
        });
        function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function() {
        const profilePreview = document.getElementById("profilePreview");
        profilePreview.src = reader.result;
        profilePreview.style.display = "block";
    };
    reader.readAsDataURL(event.target.files[0]);
}
