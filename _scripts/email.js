document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".email-link").forEach((el) => {
    const user = el.getAttribute("data-user");
    const domain = el.getAttribute("data-domain");
    if (!user || !domain) return;
    const addr = `${user}@${domain}`;
    el.href = `mailto:${addr}`;
  });
});
