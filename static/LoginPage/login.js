/* -----------------------------------------------------------
   FIRST & LAST NAME VALIDATION (Alphabet only) newly added
----------------------------------------------------------- */

function isAlphaOnly(value) {
    return /^[A-Za-z]+$/.test(value.trim());
}

const signupForm = document.querySelector('#signup-container form');


if (signupForm) {
    const inputs = signupForm.querySelectorAll('input');

    // Remove error on typing
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            input.classList.remove('input-error');
            const err = input.closest('.space-y-2').querySelector('.error-msg');
            if (err) err.innerText = '';
        });
    });

    signupForm.addEventListener('submit', function (e) {
        e.preventDefault(); // ALWAYS stop first

        let valid = true;
        let firstErrorInput = null;
        const errorMessages = []; // New: Collect all error messages

        const firstName = signupForm.querySelector('[name="firstname"]');
        const lastName = signupForm.querySelector('[name="lastname"]');
        const emailInput = signupForm.querySelector('[name="email"]');
        const phoneInput = signupForm.querySelector('[name="phone"]');
        const passwordInput = signupForm.querySelector('#signup-pass');
        const confirmPassInput = signupForm.querySelector('#signup-confirm-pass');

        function markError(input, message) {
            if (valid) firstErrorInput = input;
            valid = false;
            input.classList.add('input-error');
            const span = input.closest('.space-y-2').querySelector('.error-msg');
            if (span) span.innerText = message;
            errorMessages.push(message); // New: Collect the message
            // Removed: showToast(message); // No longer call here to avoid overwriting
        }

        /* ---------- FIRST NAME ---------- */
        if (!firstName.value.trim()) {
            markError(firstName, "First name is required.");
        } else if (!isAlphaOnly(firstName.value)) {
            markError(firstName, "Only letters allowed.");
        }

        /* ---------- LAST NAME ---------- */
        if (!lastName.value.trim()) {
            markError(lastName, "Last name is required.");
        } else if (!isAlphaOnly(lastName.value)) {
            markError(lastName, "Only letters allowed.");
        }

        /* ---------- EMAIL ---------- */
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const allowedDomains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"];
        const emailValue = emailInput.value.trim();
        const emailDomain = emailValue.split("@")[1]?.toLowerCase();

        if (!emailValue) {
            markError(emailInput, "Email is required.");
        } else if (!emailPattern.test(emailValue)) {
            markError(emailInput, "Invalid email format.");
        } else if (!allowedDomains.includes(emailDomain)) {
            markError(emailInput, "Use Gmail, Yahoo, Outlook or Hotmail.");
        }

        /* ---------- PHONE ---------- */
        if (!phoneInput.value.trim()) {
            markError(phoneInput, "Phone number is required.");
        } else if (!/^[6-9]\d{9}$/.test(phoneInput.value.trim())) {
            markError(phoneInput, "Enter valid 10-digit number starting 6–9.");
        }

        /* ---------- PASSWORD ---------- */
        if (!passwordInput.value) {
            markError(passwordInput, "Password is required.");
        } else if (scorePassword(passwordInput.value) < 3) {
            markError(passwordInput, "Password is too weak.");
        }

        /* ---------- CONFIRM PASSWORD ---------- */
        if (!confirmPassInput.value) {
            markError(confirmPassInput, "Please confirm password.");
        } else if (passwordInput.value !== confirmPassInput.value) {
            markError(confirmPassInput, "Passwords do not match.");
        }

        /* ---------- FINAL VALIDATION ---------- */
        if (!valid) {
            // New: Show a single toast with the first error (or customize as needed)
            if (errorMessages.length > 0) {
                showToast(errorMessages[0]); // Shows only the first error in toast
            }
            firstErrorInput?.focus();
            shakeForm();
            return false; // stop form submit
        }


        signupForm.submit(); // ✅ submit only if valid
    });

    function shakeForm() {
        signupForm.classList.add('shake');
        setTimeout(() => signupForm.classList.remove('shake'), 400);
    }
}



/* -----------------------------------------------------------
   1. VIEW SWITCHING LOGIC (Pure JS)
   ----------------------------------------------------------- */
function switchView(view) {
    const signinContainer = document.getElementById('signin-container');
    const signupContainer = document.getElementById('signup-container');

    const viewport = document.getElementById('viewport');

    if (view === 'signup') {
        // Animate Out Sign In
        signinContainer.classList.add('exit-left');
        signinContainer.classList.remove('active');

        // Animate In Sign Up
        setTimeout(() => {
            signupContainer.classList.add('active');
            signupContainer.classList.remove('exit-left');
            // Adjust height dynamically
            viewport.style.minHeight = signupContainer.offsetHeight + 'px';
        }, 50);

        changeHeroText("Join the builders.");

    } else {
        // Animate Out Sign Up
        signupContainer.classList.remove('active');

        // Animate In Sign In
        signinContainer.classList.remove('exit-left');
        signinContainer.classList.add('active');

        // Adjust height dynamically
        viewport.style.minHeight = signinContainer.offsetHeight + 'px';

        changeHeroText("Welcome back.");
    }
}

function changeHeroText(newText) {
    const title = document.getElementById('heroTitle');
    title.classList.add('fade-out'); // fade out
    setTimeout(() => {
        title.innerText = newText;
        title.classList.remove('fade-out'); // fade in
    }, 300);
}

/* -----------------------------------------------------------
   2. UTILITIES (Password Toggle, Strength)
   ----------------------------------------------------------- */
function togglePass(id, btn) {
    const input = document.getElementById(id);
    const isHidden = input.type === "password";

    input.type = isHidden ? "text" : "password";

    if (isHidden) {
        // Eye Slash (Visible)
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.94 10.94 0 0 1 12 20c-7 0-10-6.5-10-8a10.3 10.3 0 0 1 3.05-4.22"></path><path d="M1 1l22 22"></path></svg>';
        btn.classList.add('active-eye');
    } else {
        // Eye (Hidden)
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
        btn.classList.remove('active-eye');
    }
}

/* -----------------------------------------------------------
   3. PASSWORD STRENGTH METER
   ----------------------------------------------------------- */
const passInput = document.getElementById('signup-pass');
if (passInput) {
    passInput.addEventListener('input', function (e) {
        updateStrengthMeter(e.target.value, 'strength-bar');
    });
}

const changePassInput = document.getElementById('new-pass');
if (changePassInput) {
    changePassInput.addEventListener('input', function (e) {
        updateStrengthMeter(e.target.value, 'change-strength-bar');
    });
}

function scorePassword(pw) {
    if (!pw || pw.length === 0) return 0;
    let score = 0;
    if (pw.length >= 8) score++;
    if (pw.length >= 12) score++;
    if (/[a-z]/.test(pw) && /[A-Z]/.test(pw)) score++;
    if (/\d/.test(pw)) score++;
    if (/[^A-Za-z0-9]/.test(pw)) score++;

    if (score <= 1) return 1; // Weak
    if (score === 2) return 2; // Medium
    if (score === 3) return 3; // Good
    return 4; // Strong
}

function updateStrengthMeter(val, barId = 'strength-bar') {
    const bar = document.getElementById(barId);
    if (!bar) return;

    if (!val) {
        bar.style.width = '0%';
        return;
    }

    const score = scorePassword(val);
    const width = (score / 4) * 100;
    let color = '#ff4d4d'; // Red
    if (score > 2) color = '#ffb86b'; // Orange
    if (score === 4) color = '#10b981'; // Green

    bar.style.width = width + '%';
    bar.style.backgroundColor = color;
}

/* -----------------------------------------------------------
   4. THEME TOGGLE LOGIC
   ----------------------------------------------------------- */
const themeBtn = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

themeBtn.addEventListener('click', () => {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';

    html.setAttribute('data-theme', next);

    if (next === 'dark') {
        // Sun Icon
        themeIcon.innerHTML = '<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>';
    } else {
        // Moon Icon
        themeIcon.innerHTML = '<path d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/>';
    }
});

/* -----------------------------------------------------------
   5. FORM SUBMISSION (Validation Shake)
   ----------------------------------------------------------- */
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    const isManagedAuthForm =
        !!form.closest('#signin-container') ||
        !!form.closest('#signup-container') ||
        !!form.querySelector('#new-pass');

    if (isManagedAuthForm) return;

    form.addEventListener('submit', (e) => {
        let isValid = true;

        // Simple required check
        form.querySelectorAll('input[required]').forEach(input => {
            if (input.value.trim() === '') {
                isValid = false;
                input.classList.add('input-error');
                setTimeout(() => input.classList.remove('input-error'), 300);
            }
        });

        if (!isValid) {
            e.preventDefault(); // Stop if invalid
        }
        // If valid, allow Django form submission to proceed
    });
});

// Initialize viewport height on load
window.addEventListener('load', () => {
    const activeForm = document.querySelector('.auth-form-container.active');
    if (activeForm) {
        document.getElementById('viewport').style.minHeight = activeForm.offsetHeight + 'px';
    }
});





const signinForm = document.querySelector('#signin-container form');

if (signinForm) {

  const inputs = signinForm.querySelectorAll("input");

  inputs.forEach(input=>{
    input.addEventListener("input",()=>{
      input.classList.remove("input-error");

      const err = input.closest(".space-y-2")?.querySelector(".error-msg");
      if(err) err.innerText="";
    });
  });

  signinForm.addEventListener("submit",(e)=>{

    let valid = true;

    const email = signinForm.querySelector('[name="emailorphone"]');
    const pass = signinForm.querySelector('[name="password"]');

    function markError(input,msg){
        valid=false;
        input.classList.add("input-error");

        const span=input.closest(".space-y-2")?.querySelector(".error-msg");
        if(span) span.innerText=msg;
    }

    if(!email.value.trim()){
        markError(email,"Email or phone is required.");
    }

    if(!pass.value.trim()){
        markError(pass,"Password is required.");
    }

    if(!valid){
        e.preventDefault();
    }

  });
}

    // Change-password form handler (run on pages that have the change-password form)
    const changePasswordForm = document.querySelector('form[action*="change-password"]');

    if (changePasswordForm) {
        const newPass = changePasswordForm.querySelector('[name="new_password"]');
        const confirmPass = changePasswordForm.querySelector('[name="confirm_password"]');

        const inputs = changePasswordForm.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                input.classList.remove('input-error');
                const err = input.closest('.space-y-2')?.querySelector('.error-msg');
                if (err) err.innerText = '';
            });
        });

        changePasswordForm.addEventListener('submit', (e) => {
            let valid = true;

            function markError(input, msg) {
                valid = false;
                input.classList.add('input-error');
                const span = input.closest('.space-y-2')?.querySelector('.error-msg');
                if (span) span.innerText = msg;
            }

            // Keep same password rule as login page: required field validation.
            if (!newPass.value.trim()) {
                markError(newPass, 'Password is required.');
            }

            // Enforce minimum strength (same as signup): score >= 3
            else if (scorePassword(newPass.value) < 3) {
                markError(newPass, 'Password is too weak.');
            }

            if (!confirmPass.value.trim()) {
                markError(confirmPass, 'Please confirm password.');
            } else if (newPass.value !== confirmPass.value) {
                markError(confirmPass, 'Passwords do not match.');
            }

            if (!valid) {
                e.preventDefault();
            }
        });
    }