const menuButton = document.querySelector(".menu-button");
const navLinks = document.querySelector("[data-nav-links]");
const year = document.querySelector("#year");
const contactForm = document.querySelector("#contactForm");

if (year) {
  year.textContent = new Date().getFullYear();
}

if (menuButton && navLinks) {
  menuButton.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
      menuButton.setAttribute("aria-expanded", "false");
    });
  });
}

if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(contactForm);
    const name = formData.get("name") || "";
    const email = formData.get("email") || "";
    const company = formData.get("company") || "";
    const message = formData.get("message") || "";

    const subject = encodeURIComponent(`ApexGTM AI Strategy Call - ${company}`);
    const body = encodeURIComponent(
      `Name: ${name}\nEmail: ${email}\nCompany: ${company}\n\nWhat they sell / goal:\n${message}\n\nI want to book a free ApexGTM AI strategy call.`
    );

    window.location.href = `mailto:hello@apexgtm.ai?subject=${subject}&body=${body}`;
  });
}
