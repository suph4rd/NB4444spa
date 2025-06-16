$("#btnMenu").on("click", (e) => {
    e.preventDefault();
    let elem = document.querySelector("#LeftMenu");
    if (elem.classList.contains("d-none")) {
        elem.classList.remove("d-none");
    } else {
        elem.classList.add("d-none");
    }
})