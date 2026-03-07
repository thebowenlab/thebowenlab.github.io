document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("email-link");
  if (!el) return;

  const user = el.getAttribute("data-user");
  const domain = el.getAttribute("data-domain");
  if (!user || !domain) return;

  const addr = `${user}@${domain}`;
  el.setAttribute("href", `mailto:${addr}`);
  el.setAttribute("aria-label", `Email ${addr}`);
});
