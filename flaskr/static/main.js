const like_button = document.querySelectorAll("#like_button");
const like_count = document.querySelectorAll("#like_count");
const unlike_button = document.querySelectorAll("#unlike_button");
const unlike_count = document.querySelectorAll("#unlike_count");

//////// toggle --> View post details ////////
const toggle_btn = document.querySelectorAll(".toggle_btn");
const text_body = document.querySelectorAll(".text_body");
for (let i = 0; i < toggle_btn.length; i++) {
  toggle_btn[i].addEventListener("click", () => {
    if (text_body[i].style.display == "none") {
      text_body[i].style.display = "block";
    } else {
      text_body[i].style.display = "none";
    }
  });
}

//////// like posts ////////
const like = document.querySelectorAll("#like");
for (let i = 0; i < like.length; i++) {
  like[i].addEventListener("click", () => {
    let id=text_body[i].id
    fetch(`/like_unlike/${id}/1`)
      .then((res) => res.json)
      .then((data) => {});
    if (like_count[i].innerHTML === "0") {
      like_count[i].innerHTML = "1";
      like_button[i].classList.remove("fa-regular");
      like_button[i].classList.add("fa-solid");
      if (unlike_count[i].innerHTML === "1") {
        unlike_count[i].innerHTML = "0";
        unlike_button[i].classList.remove("fa-solid");
        unlike_button[i].classList.add("fa-regular");
      }
    } else {
      like_count[i].innerHTML = "0";
      like_button[i].classList.remove("fa-solid");
      like_button[i].classList.add("fa-regular");
    }
  });
}

//////// unlike posts ////////
const unlike = document.querySelectorAll("#unlike");
for (let i = 0; i < unlike.length; i++) {
  unlike[i].addEventListener("click", () => {
    let id=text_body[i].id
    fetch(`/like_unlike/${id}/0`)
      .then((res) => res.json)
      .then((data) => {});
    if (unlike_count[i].innerHTML === "0") {
      unlike_count[i].innerHTML = "1";
      unlike_button[i].classList.remove("fa-regular");
      unlike_button[i].classList.add("fa-solid");
      if (like_count[i].innerHTML === "1") {
        like_count[i].innerHTML = "0";
        like_button[i].classList.remove("fa-solid");
        like_button[i].classList.add("fa-regular");
      }
    } else {
      unlike_count[i].innerHTML = "0";
      unlike_button[i].classList.remove("fa-solid");
      unlike_button[i].classList.add("fa-regular");
    }
  });
}

