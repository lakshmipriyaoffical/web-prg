const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function showError(id, msg) {
  document.getElementById(id + "Err").textContent = msg;
  return msg === "";
}

function checkName(v)  { return showError("name", v.trim() ? "" : "Name is required."); }
function checkEmail(v) {
  if (!v.trim()) return showError("email", "Email is required.");
  return showError("email", emailPattern.test(v) ? "" : "Enter a valid email address.");
}
function checkPassword(v) {
  if (!v) return showError("password", "Password is required.");
  if (v.length < 8) return showError("password", "Password must be at least 8 characters.");
  if (!/[A-Z]/.test(v)) return showError("password", "Include at least one uppercase letter.");
  if (!/[a-z]/.test(v)) return showError("password", "Include at least one lowercase letter.");
  if (!/\d/.test(v)) return showError("password", "Include at least one digit.");
  if (!/[^A-Za-z0-9]/.test(v)) return showError("password", "Include at least one special character.");
  return showError("password", "");
}
function checkConfirm(p, c) {
  return showError("confirm", p === c && c ? "" : "Passwords do not match.");
}
