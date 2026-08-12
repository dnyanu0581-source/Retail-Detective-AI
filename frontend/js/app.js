/* =========================================================
   RETAIL DETECTIVE AI
   FRONTEND APPLICATION
   Vanilla JavaScript
========================================================= */


/* =========================================================
   CONFIGURATION
========================================================= */

const API_URL = "http://127.0.0.1:8000";

const AI_ENDPOINT = `${API_URL}/api/ai/ask`;


/* =========================================================
   APPLICATION STATE
========================================================= */

const state = {

    user: {

        id: localStorage.getItem("user_id") || null,

        username:
            localStorage.getItem("username") || null,

        email:
            localStorage.getItem("email") || null,

        token:
            localStorage.getItem("access_token") || null
    },

    dataset: {

        name: null,

        rows: [],

        columns: [],

        numericColumns: [],

        categoricalColumns: [],

        dateColumns: [],

        rowCount: 0,

        columnCount: 0
    },

    analysis: null,

    health: null

};


/* =========================================================
   DOM HELPERS
========================================================= */

const $ = (selector) =>
    document.querySelector(selector);

const $$ = (selector) =>
    document.querySelectorAll(selector);


/* =========================================================
   TOAST NOTIFICATION
========================================================= */

function showNotification(message, type = "info") {

    const container =
        $("#toastContainer");

    const toast =
        document.createElement("div");

    toast.className =
        `toast ${type}`;

    const icon =
        type === "success"
            ? "✓"
            : type === "error"
                ? "!"
                : "i";

    const title =
        type === "success"
            ? "Success"
            : type === "error"
                ? "Something went wrong"
                : "Information";

    toast.innerHTML = `

        <div class="toast-icon">
            ${icon}
        </div>

        <div>

            <strong>${escapeHTML(title)}</strong>

            <p>${escapeHTML(message)}</p>

        </div>

    `;

    container.appendChild(toast);

    setTimeout(() => {

        toast.style.opacity = "0";
        toast.style.transform =
            "translateX(20px)";

        setTimeout(
            () => toast.remove(),
            250
        );

    }, 3500);
}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


/* =========================================================
   AUTH ELEMENTS
========================================================= */

const authPage =
    $("#authPage");

const loginPage =
    $("#loginPage");

const signupPage =
    $("#signupPage");

const appPage =
    $("#appPage");

const loginForm =
    $("#loginForm");

const signupForm =
    $("#signupForm");


/* =========================================================
   AUTH PAGE SWITCHING
========================================================= */

$("#showSignup").addEventListener(
    "click",
    () => {

        loginPage.classList.add("hidden");

        signupPage.classList.remove("hidden");

        $("#signupUsername").focus();

    }
);


$("#showLogin").addEventListener(
    "click",
    () => {

        signupPage.classList.add("hidden");

        loginPage.classList.remove("hidden");

        $("#email").focus();

    }
);


/* =========================================================
   PASSWORD VISIBILITY
========================================================= */

$$(".password-toggle").forEach(
    button => {

        button.addEventListener(
            "click",
            () => {

                const input =
                    document.getElementById(
                        button.dataset.target
                    );

                if (!input) return;

                if (
                    input.type === "password"
                ) {

                    input.type = "text";

                    button.textContent =
                        "Hide";

                } else {

                    input.type = "password";

                    button.textContent =
                        "Show";
                }

            }
        );

    }
);


/* =========================================================
   PASSWORD STRENGTH
========================================================= */

$("#signupPassword").addEventListener(
    "input",
    event => {

        const password =
            event.target.value;

        const bars =
            $$("#passwordStrength span");

        let strength = 0;

        if (password.length >= 8)
            strength++;

        if (/[A-Z]/.test(password))
            strength++;

        if (
            /[0-9]/.test(password) ||
            /[^A-Za-z0-9]/.test(password)
        )
            strength++;

        bars.forEach(
            (bar, index) => {

                bar.style.background =
                    index < strength
                        ? strength === 3
                            ? "#16a34a"
                            : "#2563eb"
                        : "#e8ecf2";

            }
        );

    }
);


/* =========================================================
   LOGIN
========================================================= */

loginForm.addEventListener(
    "submit",
    async event => {

        event.preventDefault();

        const email =
            $("#email").value
                .trim()
                .toLowerCase();

        const password =
            $("#password").value;

        const message =
            $("#loginMessage");

        message.textContent = "";

        if (!email || !password) {

            message.textContent =
                "Please enter your email and password.";

            message.style.color =
                "var(--red)";

            return;
        }

        setButtonLoading(
            loginForm.querySelector(
                "button[type='submit']"
            ),
            true,
            "Signing in..."
        );

        try {

            const response =
                await fetch(
                    `${API_URL}/api/auth/login`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            email,

                            password

                        })
                    }
                );

            const data =
                await safeJSON(response);

            if (!response.ok) {

                throw new Error(
                    data?.detail ||
                    "Unable to sign in."
                );
            }

            localStorage.setItem(
                "access_token",
                data.access_token || ""
            );

            localStorage.setItem(
                "user_id",
                data.user_id || ""
            );

            localStorage.setItem(
                "username",
                data.username || ""
            );

            localStorage.setItem(
                "email",
                data.email || email
            );

            state.user = {

                id:
                    data.user_id || null,

                username:
                    data.username || "User",

                email:
                    data.email || email,

                token:
                    data.access_token || null

            };

            message.textContent =
                "Signed in successfully.";

            message.style.color =
                "var(--green)";

            showNotification(
                "Welcome back to your retail intelligence workspace.",
                "success"
            );

            setTimeout(
                showApplication,
                350
            );

        } catch (error) {

            message.textContent =
                error.message;

            message.style.color =
                "var(--red)";

            showNotification(
                error.message,
                "error"
            );

        } finally {

            setButtonLoading(
                loginForm.querySelector(
                    "button[type='submit']"
                ),
                false,
                "Sign in"
            );

        }

    }
);


/* =========================================================
   SIGNUP
========================================================= */

signupForm.addEventListener(
    "submit",
    async event => {

        event.preventDefault();

        const username =
            $("#signupUsername").value.trim();

        const email =
            $("#signupEmail")
                .value
                .trim()
                .toLowerCase();

        const password =
            $("#signupPassword").value;

        const confirmPassword =
            $("#signupConfirmPassword").value;

        const message =
            $("#signupMessage");

        message.textContent = "";

        if (
            !username ||
            !email ||
            !password ||
            !confirmPassword
        ) {

            message.textContent =
                "Please complete all fields.";

            message.style.color =
                "var(--red)";

            return;
        }

        if (username.length < 3) {

            message.textContent =
                "Username must contain at least 3 characters.";

            message.style.color =
                "var(--red)";

            return;
        }

        if (password.length < 8) {

            message.textContent =
                "Password must contain at least 8 characters.";

            message.style.color =
                "var(--red)";

            return;
        }

        if (password !== confirmPassword) {

            message.textContent =
                "Passwords do not match.";

            message.style.color =
                "var(--red)";

            return;
        }

        const submitButton =
            signupForm.querySelector(
                "button[type='submit']"
            );

        setButtonLoading(
            submitButton,
            true,
            "Creating..."
        );

        try {

            const response =
                await fetch(
                    `${API_URL}/api/auth/signup`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            username,

                            email,

                            password

                        })
                    }
                );

            const data =
                await safeJSON(response);

            if (!response.ok) {

                throw new Error(
                    data?.detail ||
                    "Unable to create account."
                );
            }

            message.textContent =
                "Account created successfully. Please sign in.";

            message.style.color =
                "var(--green)";

            showNotification(
                "Your account has been created successfully.",
                "success"
            );

            signupForm.reset();

            setTimeout(
                () => {

                    signupPage.classList.add(
                        "hidden"
                    );

                    loginPage.classList.remove(
                        "hidden"
                    );

                    $("#email").value =
                        email;

                },
                1000
            );

        } catch (error) {

            message.textContent =
                error.message;

            message.style.color =
                "var(--red)";

            showNotification(
                error.message,
                "error"
            );

        } finally {

            setButtonLoading(
                submitButton,
                false,
                "Create account"
            );

        }

    }
);


/* =========================================================
   GOOGLE BUTTON
========================================================= */

$("#googleLogin").addEventListener(
    "click",
    () => {

        showNotification(
            "Google authentication is not connected to the current FastAPI backend yet.",
            "info"
        );

    }
);


/* =========================================================
   BUTTON LOADING
========================================================= */

function setButtonLoading(
    button,
    loading,
    text
) {

    if (!button) return;

    button.disabled = loading;

    if (loading) {

        button.dataset.originalText =
            button.innerHTML;

        button.innerHTML =
            `<span class="spinner"></span>${text}`;

    } else {

        button.innerHTML =
            button.dataset.originalText ||
            text;
    }
}


/* =========================================================
   SHOW APPLICATION
========================================================= */

function showApplication() {

    authPage.classList.add("hidden");

    appPage.classList.remove("hidden");

    updateUserUI();

    navigateTo("overview");

    if (state.dataset.rows.length) {

        renderAllDataViews();

    }

}


/* =========================================================
   USER UI
========================================================= */

function updateUserUI() {

    const username =
        state.user.username || "User";

    const email =
        state.user.email ||
        "user@example.com";

    $("#topbarUsername").textContent =
        username;

    $("#menuUsername").textContent =
        username;

    $("#menuName").textContent =
        username;

    $("#menuEmail").textContent =
        email;

    $("#settingsName").textContent =
        username;

    $("#settingsEmail").textContent =
        email;

    const initial =
        username
            .charAt(0)
            .toUpperCase();

    $("#profileAvatar").textContent =
        initial;

    $("#menuUsername").textContent =
        initial;

}


/* =========================================================
   LOGOUT
========================================================= */

function logout() {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "user_id"
    );

    localStorage.removeItem(
        "username"
    );

    localStorage.removeItem(
        "email"
    );

    state.user = {

        id: null,

        username: null,

        email: null,

        token: null

    };

    state.dataset.rows = [];

    state.dataset.columns = [];

    state.analysis = null;

    state.health = null;

    appPage.classList.add("hidden");

    authPage.classList.remove("hidden");

    loginPage.classList.remove("hidden");

    signupPage.classList.add("hidden");

    loginForm.reset();

    showNotification(
        "You have been signed out.",
        "success"
    );
}


$("#logoutBtn").addEventListener(
    "click",
    logout
);

$("#settingsLogout").addEventListener(
    "click",
    logout
);


/* =========================================================
   PROFILE MENU
========================================================= */

$("#profileBtn").addEventListener(
    "click",
    event => {

        event.stopPropagation();

        $("#profileMenu")
            .classList.toggle("hidden");

    }
);

document.addEventListener(
    "click",
    event => {

        if (
            !event.target.closest(
                ".profile-area"
            )
        ) {

            $("#profileMenu")
                .classList.add("hidden");

        }

    }
);


$("#settingsBtn").addEventListener(
    "click",
    () => {

        $("#profileMenu")
            .classList.add("hidden");

        navigateTo("settings");

    }
);


/* =========================================================
   NAVIGATION
========================================================= */

const pageTitles = {

    overview: {

        title:
            "Your retail performance at a glance.",

        subtitle:
            "Understand what is happening in your dataset and where attention is needed."

    },

    dataset: {

        title:
            "Bring your retail data into the workspace.",

        subtitle:
            "Upload, inspect and prepare your dataset for analysis."

    },

    analytics: {

        title:
            "Explore the patterns inside your data.",

        subtitle:
            "Investigate products, categories, sales performance and unusual records."

    },

    health: {

        title:
            "Know whether your data is ready for decisions.",

        subtitle:
            "Identify quality problems before they affect your analysis."

    },

    assistant: {

        title:
            "Ask questions about your retail data.",

        subtitle:
            "Investigate your dataset using natural-language questions."

    },

    reports: {

        title:
            "Turn your findings into a clear report.",

        subtitle:
            "Generate a report from the analysis performed on your dataset."

    },

    settings: {

        title:
            "Workspace settings",

        subtitle:
            "Manage your account and application session."

    }

};


function navigateTo(pageName) {

    $$(".page").forEach(
        page =>
            page.classList.remove(
                "active-page"
            )
    );

    $$(".nav-item").forEach(
        item =>
            item.classList.remove(
                "active"
            )
    );

    const target =
        document.getElementById(
            `${pageName}Page`
        );

    if (!target) return;

    target.classList.add(
        "active-page"
    );

    const nav =
        document.querySelector(
            `.nav-item[data-page="${pageName}"]`
        );

    if (nav) {

        nav.classList.add("active");

    }

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


/* =========================================================
   ALL DATA-PAGE BUTTONS
========================================================= */

document.addEventListener(
    "click",
    event => {

        const button =
            event.target.closest(
                "[data-page]"
            );

        if (!button) return;

        const page =
            button.dataset.page;

        navigateTo(page);

    }
);


/* =========================================================
   SETTINGS NAVIGATION
========================================================= */

const settingsNav =
    document.createElement("button");

settingsNav.type = "button";


/* =========================================================
   MOBILE NAVIGATION
========================================================= */

$("#mobileNavToggle")
    .addEventListener(
        "click",
        () => {

            const nav =
                $("#mainNav");

            const visible =
                nav.style.display === "flex";

            nav.style.display =
                visible
                    ? ""
                    : "flex";

            if (!visible) {

                nav.style.position =
                    "absolute";

                nav.style.top =
                    "64px";

                nav.style.left = "0";

                nav.style.right = "0";

                nav.style.padding =
                    "10px";

                nav.style.background =
                    "white";

                nav.style.borderBottom =
                    "1px solid var(--border)";

                nav.style.flexDirection =
                    "column";

                nav.style.alignItems =
                    "stretch";

            }

        }
    );


/* =========================================================
   FILE UPLOAD
========================================================= */

const datasetFile =
    $("#datasetFile");

const dropZone =
    $("#dropZone");

$("#chooseFileBtn").addEventListener(
    "click",
    () => datasetFile.click()
);

$("#replaceDatasetBtn").addEventListener(
    "click",
    () => datasetFile.click()
);

datasetFile.addEventListener(
    "change",
    event => {

        const file =
            event.target.files[0];

        if (file) {

            processDataset(file);

        }

    }
);


/* Drag and drop */

["dragenter", "dragover"].forEach(
    eventName => {

        dropZone.addEventListener(
            eventName,
            event => {

                event.preventDefault();

                dropZone.classList.add(
                    "dragover"
                );

            }
        );

    }
);

["dragleave", "drop"].forEach(
    eventName => {

        dropZone.addEventListener(
            eventName,
            event => {

                event.preventDefault();

                dropZone.classList.remove(
                    "dragover"
                );

            }
        );

    }
);

dropZone.addEventListener(
    "drop",
    event => {

        const file =
            event.dataTransfer.files[0];

        if (file) {

            processDataset(file);

        }

    }
);


/* =========================================================
   PROCESS DATASET
========================================================= */

async function processDataset(file) {

    const extension =
        file.name
            .split(".")
            .pop()
            .toLowerCase();

    if (
        extension !== "csv" &&
        extension !== "xlsx"
    ) {

        showNotification(
            "Please upload a CSV or XLSX file.",
            "error"
        );

        return;
    }

    if (
        extension === "xlsx"
    ) {

        showNotification(
            "CSV files are currently processed directly by this frontend. XLSX processing should be connected to the backend parser.",
            "info"
        );

        return;
    }

    $("#uploadProgress")
        .classList.remove("hidden");

    let progress = 0;

    const progressBar =
        $("#progressBar");

    const progressPercent =
        $("#progressPercent");

    const progressStatus =
        $("#progressStatus");

    const timer =
        setInterval(
            () => {

                progress +=
                    Math.floor(
                        Math.random() * 12
                    );

                if (progress >= 90) {

                    progress = 90;

                    clearInterval(timer);

                }

                progressBar.style.width =
                    `${progress}%`;

                progressPercent.textContent =
                    `${progress}%`;

                progressStatus.textContent =
                    progress < 50
                        ? "Reading dataset..."
                        : "Detecting columns and values...";

            },
            90
        );

    try {

        const text =
            await file.text();

        const rows =
            parseCSV(text);

        if (!rows.length) {

            throw new Error(
                "The uploaded CSV does not contain usable rows."
            );
        }

        const columns =
            Object.keys(rows[0]);

        state.dataset = {

            name: file.name,

            rows,

            columns,

            numericColumns:
                detectNumericColumns(
                    rows,
                    columns
                ),

            categoricalColumns:
                detectCategoricalColumns(
                    rows,
                    columns
                ),

            dateColumns:
                detectDateColumns(
                    rows,
                    columns
                ),

            rowCount:
                rows.length,

            columnCount:
                columns.length

        };

        state.health =
            calculateDataHealth();

        state.analysis =
            calculateAnalytics();

        progress = 100;

        progressBar.style.width =
            "100%";

        progressPercent.textContent =
            "100%";

        progressStatus.textContent =
            "Analysis complete.";

        setTimeout(
            () => {

                $("#uploadProgress")
                    .classList.add("hidden");

                $("#datasetWorkspace")
                    .classList.remove("hidden");

                renderAllDataViews();

                showNotification(
                    `${file.name} has been analyzed successfully.`,
                    "success"
                );

                navigateTo("overview");

            },
            500
        );

    } catch (error) {

        clearInterval(timer);

        $("#uploadProgress")
            .classList.add("hidden");

        showNotification(
            error.message ||
            "Unable to analyze dataset.",
            "error"
        );

    }

}


/* =========================================================
   CSV PARSER
========================================================= */

function parseCSV(text) {

    const rows = [];

    let row = [];

    let value = "";

    let insideQuotes = false;

    for (
        let i = 0;
        i < text.length;
        i++
    ) {

        const char =
            text[i];

        const next =
            text[i + 1];

        if (
            char === '"' &&
            insideQuotes &&
            next === '"'
        ) {

            value += '"';

            i++;

        } else if (
            char === '"'
        ) {

            insideQuotes =
                !insideQuotes;

        } else if (
            char === "," &&
            !insideQuotes
        ) {

            row.push(value);

            value = "";

        } else if (
            (
                char === "\n" ||
                char === "\r"
            ) &&
            !insideQuotes
        ) {

            if (
                char === "\r" &&
                next === "\n"
            ) {

                i++;

            }

            row.push(value);

            value = "";

            if (
                row.some(
                    cell =>
                        String(cell)
                            .trim()
                            .length
                )
            ) {

                rows.push(row);

            }

            row = [];

        } else {

            value += char;

        }

    }

    if (
        value.length ||
        row.length
    ) {

        row.push(value);

        if (
            row.some(
                cell =>
                    String(cell)
                        .trim()
                        .length
            )
        ) {

            rows.push(row);

        }

    }

    if (rows.length < 2) {
        return [];
    }

    const headers =
        makeUniqueHeaders(
            rows[0]
        );

    return rows
        .slice(1)
        .map(
            cells => {

                const object = {};

                headers.forEach(
                    (header, index) => {

                        object[header] =
                            (
                                cells[index] ??
                                ""
                            ).trim();

                    }
                );

                return object;

            }
        )
        .filter(
            row =>
                Object.values(row)
                    .some(
                        value =>
                            value !== ""
                    )
        );

}


/* =========================================================
   UNIQUE HEADERS
========================================================= */

function makeUniqueHeaders(headers) {

    const used = {};

    return headers.map(
        (header, index) => {

            let clean =
                String(header)
                    .trim();

            if (!clean) {

                clean =
                    `Column ${index + 1}`;

            }

            if (
                used[clean]
            ) {

                used[clean]++;

                clean =
                    `${clean} (${used[clean]})`;

            } else {

                used[clean] = 1;

            }

            return clean;

        }
    );

}


/* =========================================================
   COLUMN DETECTION
========================================================= */

function normalizeColumnName(name) {

    return String(name)
        .toLowerCase()
        .replace(/[_-]/g, " ")
        .trim();
}


function detectNumericColumns(
    rows,
    columns
) {

    return columns.filter(
        column => {

            const values =
                rows
                    .map(
                        row =>
                            parseNumber(
                                row[column]
                            )
                    )
                    .filter(
                        value =>
                            value !== null
                    );

            return (
                values.length >=
                Math.max(
                    3,
                    rows.length * 0.6
                )
            );

        }
    );

}


function detectDateColumns(
    rows,
    columns
) {

    return columns.filter(
        column => {

            const name =
                normalizeColumnName(
                    column
                );

            if (
                /date|time|month|year/.test(
                    name
                )
            ) {
                return true;
            }

            const values =
                rows
                    .map(
                        row =>
                            row[column]
                    )
                    .filter(Boolean)
                    .slice(0, 50);

            if (!values.length)
                return false;

            const valid =
                values.filter(
                    value =>
                        !Number.isNaN(
                            Date.parse(
                                value
                            )
                        )
                );

            return (
                valid.length /
                values.length
            ) >= 0.75;

        }
    );

}


function detectCategoricalColumns(
    rows,
    columns
) {

    return columns.filter(
        column =>
            !state.dataset.numericColumns.includes(
                column
            ) &&
            !state.dataset.dateColumns.includes(
                column
            )
    );

}


/* =========================================================
   NUMBER PARSING
========================================================= */

function parseNumber(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return null;

    }

    let clean =
        String(value)
            .replace(/,/g, "")
            .replace(/₹/g, "")
            .replace(/\$/g, "")
            .replace(/€/g, "")
            .replace(/£/g, "")
            .replace(/%/g, "")
            .trim();

    if (!clean) return null;

    const number =
        Number(clean);

    return Number.isFinite(number)
        ? number
        : null;
}


/* =========================================================
   FIND IMPORTANT COLUMNS
========================================================= */

function findColumnByKeywords(
    keywords,
    columns =
        state.dataset.columns
) {

    return columns.find(
        column => {

            const normalized =
                normalizeColumnName(
                    column
                );

            return keywords.some(
                keyword =>
                    normalized === keyword ||
                    normalized.includes(keyword)
            );

        }
    ) || null;

}


function getAmountColumn() {

    return findColumnByKeywords(
        [
            "amount",
            "revenue",
            "sales",
            "total",
            "price"
        ]
    );

}


function getQuantityColumn() {

    return findColumnByKeywords(
        [
            "quantity",
            "qty",
            "units",
            "unit"
        ]
    );

}


function getProductColumn() {

    return findColumnByKeywords(
        [
            "product",
            "item",
            "product name",
            "item name"
        ]
    );

}


function getCategoryColumn() {

    return findColumnByKeywords(
        [
            "category",
            "type",
            "department",
            "segment"
        ]
    );

}


/* =========================================================
   DATA HEALTH
========================================================= */

function calculateDataHealth() {

    const rows =
        state.dataset.rows;

    const columns =
        state.dataset.columns;

    const totalCells =
        rows.length *
        columns.length;

    let missingCells = 0;

    rows.forEach(
        row => {

            columns.forEach(
                column => {

                    if (
                        row[column] === null ||
                        row[column] === undefined ||
                        String(row[column])
                            .trim() === ""
                    ) {

                        missingCells++;

                    }

                }
            );

        }
    );

    const missingRate =
        totalCells
            ? missingCells /
              totalCells
            : 0;

    const duplicateCount =
        countDuplicates(
            rows,
            columns
        );

    const duplicateRate =
        rows.length
            ? duplicateCount /
              rows.length
            : 0;

    let score = 100;

    score -=
        Math.min(
            40,
            missingRate * 100
        );

    score -=
        Math.min(
            25,
            duplicateRate * 100
        );

    const dateIssueCount =
        detectDateIssues();

    score -=
        Math.min(
            15,
            (
                dateIssueCount /
                Math.max(
                    1,
                    rows.length
                )
            ) * 100
        );

    score =
        Math.max(
            0,
            Math.round(score)
        );

    return {

        score,

        missingCells,

        missingRate,

        duplicateCount,

        duplicateRate,

        dateIssueCount

    };

}


function countDuplicates(
    rows,
    columns
) {

    const seen =
        new Set();

    let duplicates = 0;

    rows.forEach(
        row => {

            const key =
                columns
                    .map(
                        column =>
                            String(
                                row[column] ?? ""
                            ).trim()
                    )
                    .join("|");

            if (
                seen.has(key)
            ) {

                duplicates++;

            } else {

                seen.add(key);

            }

        }
    );

    return duplicates;

}


function detectDateIssues() {

    const dateColumns =
        state.dataset.dateColumns;

    if (!dateColumns.length)
        return 0;

    let issues = 0;

    state.dataset.rows.forEach(
        row => {

            dateColumns.forEach(
                column => {

                    const value =
                        row[column];

                    if (
                        value &&
                        Number.isNaN(
                            Date.parse(value)
                        )
                    ) {

                        issues++;

                    }

                }
            );

        }
    );

    return issues;

}


/* =========================================================
   ANALYTICS ENGINE
========================================================= */

function calculateAnalytics() {

    const rows =
        state.dataset.rows;

    const amountColumn =
        getAmountColumn();

    const quantityColumn =
        getQuantityColumn();

    const productColumn =
        getProductColumn();

    const categoryColumn =
        getCategoryColumn();

    const amounts =
        amountColumn
            ? rows
                .map(
                    row =>
                        parseNumber(
                            row[amountColumn]
                        )
                )
                .filter(
                    value =>
                        value !== null
                )
            : [];

    const quantities =
        quantityColumn
            ? rows
                .map(
                    row =>
                        parseNumber(
                            row[quantityColumn]
                        )
                )
                .filter(
                    value =>
                        value !== null
                )
            : [];

    const totalAmount =
        sum(amounts);

    const averageAmount =
        amounts.length
            ? totalAmount /
              amounts.length
            : null;

    const minAmount =
        amounts.length
            ? Math.min(...amounts)
            : null;

    const maxAmount =
        amounts.length
            ? Math.max(...amounts)
            : null;

    const productRanking =
        productColumn && amountColumn
            ? aggregateBy(
                rows,
                productColumn,
                amountColumn
            )
            : [];

    const categoryRanking =
        categoryColumn && amountColumn
            ? aggregateBy(
                rows,
                categoryColumn,
                amountColumn
            )
            : [];

    const anomalies =
        detectAnomalies(
            amounts,
            amountColumn
        );

    return {

        amountColumn,

        quantityColumn,

        productColumn,

        categoryColumn,

        amounts,

        quantities,

        totalAmount,

        averageAmount,

        minAmount,

        maxAmount,

        totalQuantity:
            sum(quantities),

        productRanking,

        categoryRanking,

        anomalies

    };

}


/* =========================================================
   AGGREGATION
========================================================= */

function aggregateBy(
    rows,
    groupColumn,
    valueColumn
) {

    const map =
        new Map();

    rows.forEach(
        row => {

            const group =
                String(
                    row[groupColumn] ??
                    "Unknown"
                ).trim() ||
                "Unknown";

            const value =
                parseNumber(
                    row[valueColumn]
                );

            if (
                value === null
            ) return;

            map.set(
                group,
                (
                    map.get(group) ||
                    0
                ) + value
            );

        }
    );

    return Array
        .from(map.entries())
        .map(
            ([name, value]) => ({
                name,
                value
            })
        )
        .sort(
            (a, b) =>
                b.value -
                a.value
        );

}


/* =========================================================
   ANOMALY DETECTION
   IQR METHOD
========================================================= */

function detectAnomalies(
    values,
    column
) {

    if (
        !column ||
        values.length < 8
    ) {

        return [];

    }

    const sorted =
        [...values].sort(
            (a, b) => a - b
        );

    const q1 =
        percentile(
            sorted,
            0.25
        );

    const q3 =
        percentile(
            sorted,
            0.75
        );

    const iqr =
        q3 - q1;

    const lower =
        q1 - 1.5 * iqr;

    const upper =
        q3 + 1.5 * iqr;

    return state.dataset.rows
        .map(
            (row, index) => {

                const value =
                    parseNumber(
                        row[column]
                    );

                if (
                    value === null
                ) return null;

                if (
                    value < lower ||
                    value > upper
                ) {

                    return {

                        index:
                            index + 1,

                        value,

                        direction:
                            value > upper
                                ? "high"
                                : "low"

                    };

                }

                return null;

            }
        )
        .filter(Boolean)
        .slice(0, 20);

}


function percentile(
    sorted,
    percentileValue
) {

    const index =
        (
            sorted.length - 1
        ) *
        percentileValue;

    const lower =
        Math.floor(index);

    const upper =
        Math.ceil(index);

    if (
        lower === upper
    ) {

        return sorted[lower];

    }

    return (
        sorted[lower] +
        (
            sorted[upper] -
            sorted[lower]
        ) *
        (
            index - lower
        )
    );

}


/* =========================================================
   MATH HELPERS
========================================================= */

function sum(values) {

    return values.reduce(
        (
            total,
            value
        ) =>
            total + value,
        0
    );

}


function average(values) {

    return values.length
        ? sum(values) /
          values.length
        : null;

}


/* =========================================================
   FORMATTERS
========================================================= */

function formatNumber(
    value
) {

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(value)
    ) {

        return "—";

    }

    return new Intl.NumberFormat(
        "en-IN",
        {
            maximumFractionDigits: 2
        }
    ).format(value);

}


function formatCompact(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {

        return "—";

    }

    return new Intl.NumberFormat(
        "en-IN",
        {
            notation: "compact",
            maximumFractionDigits: 2
        }
    ).format(value);

}


function formatCurrency(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {

        return "—";

    }

    return "₹" +
        formatCompact(value);

}


/* =========================================================
   RENDER ALL DATA VIEWS
========================================================= */

function renderAllDataViews() {

    renderDataset();

    renderHealth();

    renderAnalytics();

    renderOverview();

    renderAssistant();

    renderReports();

}


/* =========================================================
   DATASET VIEW
========================================================= */

function renderDataset() {

    $("#datasetName").textContent =
        state.dataset.name;

    $("#datasetStats").innerHTML = `

        ${miniStat(
            state.dataset.rowCount,
            "Records"
        )}

        ${miniStat(
            state.dataset.columnCount,
            "Columns"
        )}

        ${miniStat(
            state.dataset.numericColumns.length,
            "Numeric fields"
        )}

        ${miniStat(
            state.dataset.categoricalColumns.length,
            "Category fields"
        )}

    `;

    const columns =
        state.dataset.columns;

    $("#previewHead").innerHTML = `

        <tr>

            ${columns
                .map(
                    column =>
                        `<th>${escapeHTML(column)}</th>`
                )
                .join("")}

        </tr>

    `;

    const previewRows =
        state.dataset.rows
            .slice(0, 8);

    $("#previewBody").innerHTML =
        previewRows
            .map(
                row => `

                    <tr>

                        ${columns
                            .map(
                                column =>
                                    `<td>${escapeHTML(
                                        row[column]
                                    )}</td>`
                            )
                            .join("")}

                    </tr>

                `
            )
            .join("");

}


function miniStat(
    value,
    label
) {

    return `

        <div class="mini-stat">

            <strong>
                ${escapeHTML(value)}
            </strong>

            <span>
                ${escapeHTML(label)}
            </span>

        </div>

    `;

}


/* =========================================================
   OVERVIEW
========================================================= */

function renderOverview() {

    $("#emptyOverview")
        .classList.add("hidden");

    $("#overviewContent")
        .classList.remove("hidden");

    const a =
        state.analysis;

    const h =
        state.health;

    $("#metricGrid").innerHTML = `

        ${metricCard(
            "Records",
            formatNumber(
                state.dataset.rowCount
            ),
            "Rows analyzed",
            ""
        )}

        ${metricCard(
            a.amountColumn
                ? "Total Value"
                : "Numeric Fields",
            a.amountColumn
                ? formatCurrency(
                    a.totalAmount
                )
                : formatNumber(
                    state.dataset
                        .numericColumns
                        .length
                ),
            a.amountColumn
                ? `Using ${a.amountColumn}`
                : "Available for analysis",
            "green"
        )}

        ${metricCard(
            a.amountColumn
                ? "Average Value"
                : "Data Health",
            a.amountColumn
                ? formatCurrency(
                    a.averageAmount
                )
                : `${h.score}/100`,
            a.amountColumn
                ? "Average analyzed transaction"
                : "Overall quality score",
            "purple"
        )}

        ${metricCard(
            "Anomalies",
            formatNumber(
                a.anomalies.length
            ),
            "Unusual numeric records detected",
            "amber"
        )}

    `;


    $("#executiveSummary")
        .textContent =
        generateExecutiveSummary();


    renderAttention();

    renderStory();

    renderRecommendations();

}


function metricCard(
    label,
    value,
    detail,
    color = ""
) {

    return `

        <div class="metric-card ${color}">

            <div class="metric-label">
                ${escapeHTML(label)}
            </div>

            <div class="metric-value">
                ${escapeHTML(value)}
            </div>

            <div class="metric-detail">
                ${escapeHTML(detail)}
            </div>

        </div>

    `;

}


/* =========================================================
   EXECUTIVE SUMMARY
========================================================= */

function generateExecutiveSummary() {

    const a =
        state.analysis;

    const h =
        state.health;

    let text =
        `The dataset contains ${formatNumber(
            state.dataset.rowCount
        )} records across ${formatNumber(
            state.dataset.columnCount
        )} fields. `;

    if (a.amountColumn) {

        text +=
            `Using "${a.amountColumn}" as the primary value field, the analyzed total is ${formatCurrency(
                a.totalAmount
            )}, with an average of ${formatCurrency(
                a.averageAmount
            )}. `;

    }

    text +=
        `The current data health score is ${h.score}/100. `;

    if (
        a.anomalies.length
    ) {

        text +=
            `${a.anomalies.length} unusual numeric record(s) were detected and should be reviewed.`;

    } else {

        text +=
            "No unusual numeric records were detected using the current IQR-based check.";

    }

    return text;

}


/* =========================================================
   ATTENTION
========================================================= */

function renderAttention() {

    const items = [];

    const h =
        state.health;

    const a =
        state.analysis;

    if (
        h.missingCells > 0
    ) {

        items.push({

            type:
                h.missingRate > 0.05
                    ? "danger"
                    : "warning",

            title:
                "Missing values detected",

            text:
                `${formatNumber(
                    h.missingCells
                )} cells are empty (${(
                    h.missingRate * 100
                ).toFixed(2)}% of the dataset).`

        });

    } else {

        items.push({

            type:
                "success",

            title:
                "No missing values detected",

            text:
                "All inspected cells contain values."

        });

    }

    if (
        h.duplicateCount > 0
    ) {

        items.push({

            type:
                "warning",

            title:
                "Duplicate records found",

            text:
                `${formatNumber(
                    h.duplicateCount
                )} duplicate record(s) were detected.`

        });

    } else {

        items.push({

            type:
                "success",

            title:
                "No duplicate records detected",

            text:
                "Each row appears unique based on all available columns."

        });

    }

    if (
        a.anomalies.length
    ) {

        items.push({

            type:
                "warning",

            title:
                "Unusual numeric values detected",

            text:
                `${formatNumber(
                    a.anomalies.length
                )} records fall outside the IQR-based expected range.`

        });

    }

    if (
        a.productRanking.length
    ) {

        const top =
            a.productRanking[0];

        items.push({

            type:
                "success",

            title:
                `Strongest product: ${top.name}`,

            text:
                `It contributes ${formatCurrency(
                    top.value
                )} based on the selected value field.`

        });

    }

    $("#attentionList").innerHTML =
        items
            .slice(0, 5)
            .map(
                item => `

                    <div class="attention-item">

                        <span class="attention-dot ${item.type}">
                        </span>

                        <div>

                            <strong>
                                ${escapeHTML(
                                    item.title
                                )}
                            </strong>

                            <p>
                                ${escapeHTML(
                                    item.text
                                )}
                            </p>

                        </div>

                    </div>

                `
            )
            .join("");

}


/* =========================================================
   DATA STORY
========================================================= */

function renderStory() {

    const a =
        state.analysis;

    const stories = [];

    if (
        a.amountColumn
    ) {

        stories.push(
            `The dataset's primary value field is "${a.amountColumn}", with a total of ${formatCurrency(
                a.totalAmount
            )}.`
        );

    }

    if (
        a.productRanking.length
    ) {

        stories.push(
            `${a.productRanking[0].name} is the leading product by aggregated value in the available data.`
        );

    }

    if (
        a.categoryRanking.length
    ) {

        stories.push(
            `${a.categoryRanking[0].name} is the leading category by aggregated value.`
        );

    }

    stories.push(
        `The dataset currently contains ${formatNumber(
            state.dataset.rowCount
        )} records and ${formatNumber(
            state.dataset.columnCount
        )} fields.`
    );

    $("#storyList").innerHTML =
        stories
            .slice(0, 5)
            .map(
                (story, index) => `

                    <div class="story-item">

                        <div class="story-number">
                            ${String(
                                index + 1
                            ).padStart(
                                2,
                                "0"
                            )}
                        </div>

                        <div>

                            <strong>
                                Finding ${index + 1}
                            </strong>

                            <p>
                                ${escapeHTML(
                                    story
                                )}
                            </p>

                        </div>

                    </div>

                `
            )
            .join("");

}


/* =========================================================
   RECOMMENDATIONS
========================================================= */

function renderRecommendations() {

    const a =
        state.analysis;

    const h =
        state.health;

    const recommendations = [];

    if (
        h.missingCells > 0
    ) {

        recommendations.push({

            title:
                "Review missing values",

            text:
                "Clean important analytical fields before making decisions."

        });

    }

    if (
        h.duplicateCount > 0
    ) {

        recommendations.push({

            title:
                "Investigate duplicates",

            text:
                "Check whether duplicate rows represent repeated transactions or data-entry issues."

        });

    }

    if (
        a.anomalies.length
    ) {

        recommendations.push({

            title:
                "Review unusual records",

            text:
                "Investigate outliers before using aggregate metrics as business conclusions."

        });

    }

    if (
        a.productRanking.length
    ) {

        recommendations.push({

            title:
                "Investigate top products",

            text:
                `Focus further analysis on ${a.productRanking[0].name}, the current leading product.`

        });

    }

    if (
        !recommendations.length
    ) {

        recommendations.push({

            title:
                "Explore deeper patterns",

            text:
                "Use Explore Insights and AI Analyst to investigate the dataset further."

        });

    }

    $("#recommendationList").innerHTML =
        recommendations
            .slice(0, 4)
            .map(
                (item, index) => `

                    <div class="recommendation-card">

                        <div class="recommendation-number">
                            0${index + 1}
                        </div>

                        <h3>
                            ${escapeHTML(
                                item.title
                            )}
                        </h3>

                        <p>
                            ${escapeHTML(
                                item.text
                            )}
                        </p>

                    </div>

                `
            )
            .join("");

}


/* =========================================================
   ANALYTICS
========================================================= */

function renderAnalytics() {

    $("#analyticsEmpty")
        .classList.add("hidden");

    $("#analyticsContent")
        .classList.remove("hidden");

    const a =
        state.analysis;

    $("#analyticsMetricGrid").innerHTML = `

        ${metricCard(
            "Total analyzed value",
            a.amountColumn
                ? formatCurrency(
                    a.totalAmount
                )
                : "Not available",
            a.amountColumn
                ? a.amountColumn
                : "No suitable value column detected",
            "green"
        )}

        ${metricCard(
            "Average value",
            a.averageAmount !== null
                ? formatCurrency(
                    a.averageAmount
                )
                : "Not available",
            "Per analyzed numeric record",
            "purple"
        )}

        ${metricCard(
            "Highest value",
            a.maxAmount !== null
                ? formatCurrency(
                    a.maxAmount
                )
                : "Not available",
            "Maximum observed value",
            "amber"
        )}

        ${metricCard(
            "Total quantity",
            a.quantities.length
                ? formatNumber(
                    a.totalQuantity
                )
                : "Not available",
            a.quantityColumn ||
                "No quantity field detected",
            ""
        )}

    `;

    renderBarChart(
        "#productChart",
        a.productRanking.slice(0, 7)
    );

    renderBarChart(
        "#categoryChart",
        a.categoryRanking.slice(0, 7)
    );

    renderSalesAnalysis();

    renderProductRanking();

    renderCategoryRanking();

    renderAnomalies();

}


/* =========================================================
   BAR CHART
========================================================= */

function renderBarChart(
    selector,
    data
) {

    const container =
        $(selector);

    if (!data.length) {

        container.innerHTML = `

            <div class="empty-inline">

                No suitable grouping data is available.

            </div>

        `;

        return;

    }

    const max =
        Math.max(
            ...data.map(
                item =>
                    item.value
            )
        );

    container.innerHTML =
        data.map(
            item => `

                <div class="bar-item">

                    <span
                        class="bar-label"
                        title="${escapeHTML(
                            item.name
                        )}"
                    >
                        ${escapeHTML(
                            item.name
                        )}
                    </span>

                    <div class="bar-track">

                        <div
                            class="bar-fill"
                            style="width:${(
                                item.value /
                                max
                            ) * 100}%"
                        ></div>

                    </div>

                    <span class="bar-value">
                        ${formatCompact(
                            item.value
                        )}
                    </span>

                </div>

            `
        )
        .join("");

}


/* =========================================================
   SALES ANALYSIS
========================================================= */

function renderSalesAnalysis() {

    const a =
        state.analysis;

    const values =
        a.amounts;

    const median =
        values.length
            ? percentile(
                [...values].sort(
                    (x, y) => x - y
                ),
                0.5
            )
            : null;

    $("#salesAnalysis").innerHTML = `

        ${analysisCard(
            "Total value",
            formatCurrency(
                a.totalAmount
            )
        )}

        ${analysisCard(
            "Average value",
            formatCurrency(
                a.averageAmount
            )
        )}

        ${analysisCard(
            "Median value",
            formatCurrency(
                median
            )
        )}

        ${analysisCard(
            "Lowest value",
            formatCurrency(
                a.minAmount
            )
        )}

        ${analysisCard(
            "Highest value",
            formatCurrency(
                a.maxAmount
            )
        )}

        ${analysisCard(
            "Transactions analyzed",
            formatNumber(
                a.amounts.length
            )
        )}

    `;

}


function analysisCard(
    label,
    value
) {

    return `

        <div class="analysis-card">

            <span>
                ${escapeHTML(label)}
            </span>

            <strong>
                ${escapeHTML(value)}
            </strong>

        </div>

    `;

}


/* =========================================================
   PRODUCT RANKING
========================================================= */

function renderProductRanking() {

    const data =
        state.analysis
            .productRanking
            .slice(0, 15);

    $("#productRanking").innerHTML =
        data.length
            ? data
                .map(
                    (item, index) => rankingItem(
                        index + 1,
                        item.name,
                        "Aggregated value",
                        formatCurrency(
                            item.value
                        )
                    )
                )
                .join("")
            : emptyRanking();

}


/* =========================================================
   CATEGORY RANKING
========================================================= */

function renderCategoryRanking() {

    const data =
        state.analysis
            .categoryRanking
            .slice(0, 15);

    $("#categoryRanking").innerHTML =
        data.length
            ? data
                .map(
                    (item, index) => rankingItem(
                        index + 1,
                        item.name,
                        "Aggregated value",
                        formatCurrency(
                            item.value
                        )
                    )
                )
                .join("")
            : emptyRanking();

}


function rankingItem(
    rank,
    name,
    detail,
    value
) {

    return `

        <div class="ranking-item">

            <div class="rank">
                ${rank}
            </div>

            <div>

                <strong>
                    ${escapeHTML(name)}
                </strong>

                <small>
                    ${escapeHTML(detail)}
                </small>

            </div>

            <div class="ranking-value">
                ${escapeHTML(value)}
            </div>

        </div>

    `;

}


function emptyRanking() {

    return `

        <div class="attention-item">

            <div>

                <strong>
                    No grouping available
                </strong>

                <p>
                    A suitable product/category field was not detected.
                </p>

            </div>

        </div>

    `;

}


/* =========================================================
   ANOMALIES
========================================================= */

function renderAnomalies() {

    const anomalies =
        state.analysis.anomalies;

    if (!anomalies.length) {

        $("#anomalyList").innerHTML = `

            <div class="attention-item">

                <span class="attention-dot success">
                </span>

                <div>

                    <strong>
                        No unusual records detected
                    </strong>

                    <p>
                        The current IQR-based check did not find
                        unusually high or low values.
                    </p>

                </div>

            </div>

        `;

        return;
    }

    $("#anomalyList").innerHTML =
        anomalies
            .map(
                item => `

                    <div class="attention-item">

                        <span class="attention-dot warning">
                        </span>

                        <div>

                            <strong>
                                Record #${item.index}
                                — unusually ${item.direction} value
                            </strong>

                            <p>
                                ${formatNumber(
                                    item.value
                                )}
                            </p>

                        </div>

                    </div>

                `
            )
            .join("");

}


/* =========================================================
   ANALYTICS TABS
========================================================= */

$$(".analytics-tab").forEach(
    tab => {

        tab.addEventListener(
            "click",
            () => {

                const target =
                    tab.dataset.analyticsTab;

                $$(".analytics-tab")
                    .forEach(
                        item =>
                            item.classList.remove(
                                "active"
                            )
                    );

                tab.classList.add(
                    "active"
                );

                $$(".analytics-panel")
                    .forEach(
                        panel =>
                            panel.classList.remove(
                                "active"
                            )
                    );

                const panel =
                    document.getElementById(
                        `analytics${
                            target
                                .charAt(0)
                                .toUpperCase() +
                            target.slice(1)
                        }Tab`
                    );

                if (panel) {

                    panel.classList.add(
                        "active"
                    );

                }

            }
        );

    }
);


/* =========================================================
   DATA HEALTH
========================================================= */

function renderHealth() {

    $("#healthEmpty")
        .classList.add("hidden");

    $("#healthContent")
        .classList.remove("hidden");

    const h =
        state.health;

    const score =
        h.score;

    $("#healthScore").textContent =
        score;

    const degrees =
        score * 3.6;

    const color =
        score >= 85
            ? "#16a34a"
            : score >= 65
                ? "#d97706"
                : "#dc2626";

    $("#healthScoreCircle").style.background =
        `conic-gradient(
            ${color} ${degrees}deg,
            #e8edf3 ${degrees}deg
        )`;

    $("#healthHeadline")
        .textContent =
        score >= 85
            ? "Your dataset is in good shape."
            : score >= 65
                ? "Your dataset needs some attention."
                : "Your dataset requires cleaning before analysis.";

    $("#healthDescription")
        .textContent =
        `The current health score is ${score}/100 based on missing values, duplicates and detectable date issues.`;

    $("#healthMetrics").innerHTML = `

        ${healthCard(
            "Missing cells",
            formatNumber(
                h.missingCells
            ),
            `${(
                h.missingRate * 100
            ).toFixed(2)}% of cells`,
            "var(--amber-soft)",
            "var(--amber)"
        )}

        ${healthCard(
            "Duplicate rows",
            formatNumber(
                h.duplicateCount
            ),
            `${(
                h.duplicateRate * 100
            ).toFixed(2)}% of records`,
            "var(--red-soft)",
            "var(--red)"
        )}

        ${healthCard(
            "Date issues",
            formatNumber(
                h.dateIssueCount
            ),
            "Invalid detected dates",
            "var(--primary-soft)",
            "var(--primary)"
        )}

        ${healthCard(
            "Overall score",
            `${h.score}/100`,
            "Data readiness",
            "var(--green-soft)",
            "var(--green)"
        )}

    `;

    renderHealthIssues();

}


function healthCard(
    label,
    value,
    detail,
    bg,
    color
) {

    return `

        <div class="health-card">

            <div
                class="health-icon"
                style="
                    background:${bg};
                    color:${color};
                "
            >
                ✓
            </div>

            <strong>
                ${escapeHTML(value)}
            </strong>

            <span>
                ${escapeHTML(label)}
                ·
                ${escapeHTML(detail)}
            </span>

        </div>

    `;

}


function renderHealthIssues() {

    const h =
        state.health;

    const issues = [];

    if (
        h.missingCells
    ) {

        issues.push({

            title:
                "Missing values",

            text:
                `${formatNumber(
                    h.missingCells
                )} empty cells were detected across the dataset.`

        });

    }

    if (
        h.duplicateCount
    ) {

        issues.push({

            title:
                "Duplicate records",

            text:
                `${formatNumber(
                    h.duplicateCount
                )} repeated rows were detected using all available columns.`

        });

    }

    if (
        h.dateIssueCount
    ) {

        issues.push({

            title:
                "Date consistency",

            text:
                `${formatNumber(
                    h.dateIssueCount
                )} values could not be interpreted as valid dates.`

        });

    }

    if (!issues.length) {

        $("#healthIssues").innerHTML = `

            <div class="issue-item">

                <div
                    class="issue-icon"
                    style="
                        background:var(--green-soft);
                        color:var(--green);
                    "
                >
                    ✓
                </div>

                <div>

                    <strong>
                        No major data quality issues detected.
                    </strong>

                    <p>
                        Your current dataset passed the available
                        quality checks.
                    </p>

                </div>

            </div>

        `;

        return;

    }

    $("#healthIssues").innerHTML =
        issues
            .map(
                issue => `

                    <div class="issue-item">

                        <div class="issue-icon">
                            !
                        </div>

                        <div>

                            <strong>
                                ${escapeHTML(
                                    issue.title
                                )}
                            </strong>

                            <p>
                                ${escapeHTML(
                                    issue.text
                                )}
                            </p>

                        </div>

                    </div>

                `
            )
            .join("");

}


$("#runHealthBtn").addEventListener(
    "click",
    () => {

        if (
            !state.dataset.rows.length
        ) {

            showNotification(
                "Upload a dataset before checking its health.",
                "info"
            );

            return;

        }

        state.health =
            calculateDataHealth();

        renderHealth();

        showNotification(
            "Data health has been recalculated.",
            "success"
        );

    }
);


/* =========================================================
   AI ANALYST
========================================================= */

function renderAssistant() {

    if (
        !state.dataset.rows.length
    ) {

        return;

    }

    const suggestions = [];

    const a =
        state.analysis;

    if (
        a.productRanking.length
    ) {

        suggestions.push(
            "Show me the top 10 products by value"
        );

    }

    if (
        a.categoryRanking.length
    ) {

        suggestions.push(
            "Which category performs best?"
        );

    }

    if (
        a.amountColumn
    ) {

        suggestions.push(
            "Summarize my sales performance"
        );

    }

    suggestions.push(
        "What needs my attention?"
    );

    suggestions.push(
        "Show me unusual records"
    );

    suggestions.push(
        "Give me a summary of my dataset"
    );

    $("#suggestionList").innerHTML =
        suggestions
            .slice(0, 7)
            .map(
                question => `

                    <button
                        class="suggestion-chip"
                        data-question="${escapeHTML(
                            question
                        )}"
                    >
                        ${escapeHTML(
                            question
                        )}
                    </button>

                `
            )
            .join("");

}


document.addEventListener(
    "click",
    event => {

        const chip =
            event.target.closest(
                ".suggestion-chip"
            );

        if (!chip) return;

        $("#chatInput").value =
            chip.dataset.question;

        $("#chatForm").dispatchEvent(
            new Event(
                "submit",
                {
                    bubbles: true,
                    cancelable: true
                }
            )
        );

    }
);


/* =========================================================
   CHAT
========================================================= */

$("#chatForm").addEventListener(
    "submit",
    async event => {

        event.preventDefault();

        const input =
            $("#chatInput");

        const question =
            input.value.trim();

        if (!question)
            return;

        if (
            !state.dataset.rows.length
        ) {

            addChatMessage(
                "user",
                question
            );

            addChatMessage(
                "ai",
                "Please upload a retail dataset first. Once your data is loaded, I can analyze it and answer dataset-related questions."
            );

            input.value = "";

            return;

        }

        addChatMessage(
            "user",
            question
        );

        input.value = "";

        const thinking =
            addChatMessage(
                "ai",
                "Analyzing your dataset..."
            );

        try {

            const answer =
                await answerQuestion(
                    question
                );

            thinking.remove();

            addChatMessage(
                "ai",
                answer
            );

        } catch (error) {

            thinking.remove();

            addChatMessage(
                "ai",
                "I couldn't analyze that request right now. Please try a question about your uploaded retail data."
            );

        }

    }
);


/* =========================================================
   QUESTION ENGINE
========================================================= */

async function answerQuestion(
    question
) {

    const q =
        question
            .toLowerCase()
            .trim();

    if (
        isClearlyIrrelevant(q)
    ) {

        return (
            "I'm designed specifically for your retail dataset. " +
            "I can't help with unrelated topics, but I can answer " +
            "questions about products, sales, categories, values, " +
            "trends, anomalies and data quality."
        );

    }


    /* Try backend AI when available */

    try {

        const backendAnswer =
            await askBackendAI(
                question
            );

        if (
            backendAnswer
        ) {

            return backendAnswer;

        }

    } catch (error) {

        /* Fall back to local analysis */

    }


    return localDatasetAnswer(
        q
    );

}


/* =========================================================
   BACKEND AI
========================================================= */

async function askBackendAI(
    question
) {

    const controller =
        new AbortController();

    const timeout =
        setTimeout(
            () =>
                controller.abort(),
            2500
        );

    try {

        const response =
            await fetch(
                AI_ENDPOINT,
                {
                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        ...(state.user.token
                            ? {
                                Authorization:
                                    `Bearer ${state.user.token}`
                            }
                            : {})

                    },

                    body: JSON.stringify({

                        question,

                        dataset:
                            state.dataset.rows,

                        columns:
                            state.dataset.columns

                    }),

                    signal:
                        controller.signal

                }
            );

        if (!response.ok) {

            return null;

        }

        const data =
            await response.json();

        return (
            data.answer ||
            data.response ||
            data.message ||
            null
        );

    } finally {

        clearTimeout(timeout);

    }

}


/* =========================================================
   IRRELEVANT QUESTION DETECTION
========================================================= */

function isClearlyIrrelevant(q) {

    const retailTerms = [

        "sales",
        "sale",
        "revenue",
        "amount",
        "price",
        "product",
        "products",
        "item",
        "items",
        "category",
        "categories",
        "customer",
        "customers",
        "order",
        "orders",
        "transaction",
        "transactions",
        "quantity",
        "units",
        "dataset",
        "data",
        "row",
        "rows",
        "column",
        "columns",
        "trend",
        "trends",
        "analysis",
        "analyze",
        "analytics",
        "anomaly",
        "anomalies",
        "duplicate",
        "missing",
        "clean",
        "health",
        "report",
        "top",
        "average",
        "mean",
        "median",
        "maximum",
        "minimum",
        "highest",
        "lowest",
        "best",
        "worst",
        "compare",
        "summarize",
        "summary",
        "insight",
        "insights"
    ];

    return !retailTerms.some(
        term =>
            q.includes(term)
    );

}


/* =========================================================
   LOCAL DATASET ANSWERS
========================================================= */

function localDatasetAnswer(q) {

    const a =
        state.analysis;

    if (
        q.includes("top") &&
        (
            q.includes("product") ||
            q.includes("item")
        )
    ) {

        if (
            !a.productRanking.length
        ) {

            return (
                "I can't determine the top products because " +
                "I couldn't detect a suitable product and value column."
            );

        }

        const top =
            a.productRanking
                .slice(0, 10);

        return (

            "Here are the top products by aggregated value:\n\n" +

            top
                .map(
                    (item, index) =>
                        `${index + 1}. ${
                            item.name
                        } — ${
                            formatCurrency(
                                item.value
                            )
                        }`
                )
                .join("\n")

        );

    }


    if (
        q.includes("top") &&
        (
            q.includes("value") ||
            q.includes("amount") ||
            q.includes("price")
        )
    ) {

        if (
            !a.amounts.length
        ) {

            return (
                "I couldn't identify a numeric value field suitable for this question."
            );

        }

        const top =
            [...a.amounts]
                .sort(
                    (x, y) =>
                        y - x
                )
                .slice(0, 10);

        return (

            `Top 10 values from "${a.amountColumn}":\n\n` +

            top
                .map(
                    (value, index) =>
                        `${index + 1}. ${
                            formatNumber(value)
                        }`
                )
                .join("\n")

        );

    }


    if (
        q.includes("category") &&
        (
            q.includes("best") ||
            q.includes("highest") ||
            q.includes("top") ||
            q.includes("perform")
        )
    ) {

        if (
            !a.categoryRanking.length
        ) {

            return (
                "I couldn't identify both a category field and a suitable numeric value field."
            );

        }

        const top =
            a.categoryRanking[0];

        return (
            `The strongest category by aggregated value is "${top.name}", with ${formatCurrency(
                top.value
            )}.`
        );

    }


    if (
        q.includes("summary") ||
        q.includes("summarize")
    ) {

        return generateExecutiveSummary();

    }


    if (
        q.includes("attention") ||
        q.includes("problem") ||
        q.includes("issue")
    ) {

        const h =
            state.health;

        const findings = [];

        if (
            h.missingCells
        ) {

            findings.push(
                `${formatNumber(
                    h.missingCells
                )} missing cells`
            );

        }

        if (
            h.duplicateCount
        ) {

            findings.push(
                `${formatNumber(
                    h.duplicateCount
                )} duplicate records`
            );

        }

        if (
            a.anomalies.length
        ) {

            findings.push(
                `${formatNumber(
                    a.anomalies.length
                )} unusual numeric records`
            );

        }

        if (!findings.length) {

            return (
                "I did not detect a major issue in the available checks. " +
                "Your current data health score is " +
                `${h.score}/100.`
            );

        }

        return (
            "The main things that need attention are:\n\n" +
            findings
                .map(
                    item =>
                        `• ${item}`
                )
                .join("\n")
        );

    }


    if (
        q.includes("unusual") ||
        q.includes("anomal")
    ) {

        if (
            !a.anomalies.length
        ) {

            return (
                "I did not detect unusual values using the current IQR-based anomaly check."
            );

        }

        return (

            `I detected ${a.anomalies.length} unusual numeric record(s). ` +
            "The first records are:\n\n" +

            a.anomalies
                .slice(0, 10)
                .map(
                    item =>
                        `• Record #${item.index}: ${formatNumber(
                            item.value
                        )} (${item.direction})`
                )
                .join("\n")

        );

    }


    if (
        q.includes("average") ||
        q.includes("mean")
    ) {

        return (
            a.averageAmount !== null
                ? `The average value of "${a.amountColumn}" is ${formatCurrency(
                    a.averageAmount
                )}.`
                : "I couldn't identify a suitable numeric value field."
        );

    }


    if (
        q.includes("highest") ||
        q.includes("maximum") ||
        q.includes("max")
    ) {

        return (
            a.maxAmount !== null
                ? `The highest value in "${a.amountColumn}" is ${formatCurrency(
                    a.maxAmount
                )}.`
                : "I couldn't identify a suitable numeric value field."
        );

    }


    if (
        q.includes("lowest") ||
        q.includes("minimum") ||
        q.includes("min")
    ) {

        return (
            a.minAmount !== null
                ? `The lowest value in "${a.amountColumn}" is ${formatCurrency(
                    a.minAmount
                )}.`
                : "I couldn't identify a suitable numeric value field."
        );

    }


    if (
        q.includes("duplicate")
    ) {

        return (
            `The dataset contains ${formatNumber(
                state.health.duplicateCount
            )} duplicate record(s).`
        );

    }


    if (
        q.includes("missing")
    ) {

        return (
            `The dataset contains ${formatNumber(
                state.health.missingCells
            )} missing cells, representing ${(
                state.health.missingRate * 100
            ).toFixed(2)}% of all cells.`
        );

    }


    if (
        q.includes("health") ||
        q.includes("quality")
    ) {

        return (
            `Your current Data Health score is ${state.health.score}/100.`
        );

    }


    return (

        "I understand that you're asking about your retail data, " +
        "but I couldn't map that question to a supported analysis yet. " +
        "Try asking about top products, categories, values, averages, " +
        "missing values, duplicates, anomalies or a dataset summary."

    );

}


/* =========================================================
   CHAT MESSAGE
========================================================= */

function addChatMessage(
    type,
    message
) {

    const container =
        $("#chatMessages");

    const welcome =
        container.querySelector(
            ".chat-welcome"
        );

    if (welcome) {

        welcome.remove();

    }

    const element =
        document.createElement("div");

    element.className =
        `chat-message ${type}`;

    const formatted =
        escapeHTML(message)
            .replaceAll(
                "\n",
                "<br>"
            );

    element.innerHTML = `

        <div class="message-bubble">

            <span class="message-label">
                ${type === "user"
                    ? "YOU"
                    : "AI ANALYST"}
            </span>

            ${formatted}

        </div>

    `;

    container.appendChild(
        element
    );

    container.scrollTop =
        container.scrollHeight;

    return element;

}


/* =========================================================
   REPORTS
========================================================= */

function renderReports() {

    if (
        state.dataset.rows.length
    ) {

        $("#reportsEmpty")
            .classList.add("hidden");

        $("#reportsContent")
            .classList.remove("hidden");

    }

}


$$(".generate-report").forEach(
    button => {

        button.addEventListener(
            "click",
            () => {

                if (
                    !state.dataset.rows.length
                ) {

                    showNotification(
                        "Upload a dataset before generating a report.",
                        "info"
                    );

                    return;

                }

                generateReport(
                    button.dataset.report
                );

            }
        );

    }
);


/* =========================================================
   GENERATE REPORT
========================================================= */

function generateReport(
    type
) {

    const button =
        document.querySelector(
            `.generate-report[data-report="${type}"]`
        );

    const original =
        button.innerHTML;

    button.disabled = true;

    button.innerHTML =
        "Preparing report...";

    setTimeout(
        () => {

            $("#reportPreview")
                .classList.remove("hidden");

            $("#reportDate")
                .textContent =
                new Date()
                    .toLocaleString(
                        "en-IN"
                    );

            $("#reportBody")
                .innerHTML =
                buildReportHTML(
                    type
                );

            button.disabled =
                false;

            button.innerHTML =
                original;

            showNotification(
                "Your report has been generated from the analyzed dataset.",
                "success"
            );

        },
        800
    );

}


/* =========================================================
   REPORT HTML
========================================================= */

function buildReportHTML(
    type
) {

    const a =
        state.analysis;

    const h =
        state.health;

    const reportTitle =
        type === "investigation"
            ? "Data Investigation Report"
            : "Retail Performance Report";

    const findings = [];

    if (
        a.productRanking.length
    ) {

        findings.push({

            title:
                "Leading product",

            text:
                `${a.productRanking[0].name} has the highest aggregated value among detected products.`

        });

    }

    if (
        a.categoryRanking.length
    ) {

        findings.push({

            title:
                "Leading category",

            text:
                `${a.categoryRanking[0].name} has the highest aggregated value among detected categories.`

        });

    }

    if (
        h.missingCells
    ) {

        findings.push({

            title:
                "Missing data",

            text:
                `${formatNumber(
                    h.missingCells
                )} missing cells were detected.`

        });

    }

    if (
        a.anomalies.length
    ) {

        findings.push({

            title:
                "Anomalies",

            text:
                `${formatNumber(
                    a.anomalies.length
                )} unusual numeric records were detected using the IQR method.`

        });

    }

    return `

        <h2>
            ${escapeHTML(reportTitle)}
        </h2>

        <p>
            This report was generated from
            <strong>
                ${escapeHTML(
                    state.dataset.name
                )}
            </strong>.
            All numerical findings shown below are calculated
            from the uploaded dataset.
        </p>


        <h3>
            Dataset Snapshot
        </h3>

        <div class="report-summary-grid">

            <div class="report-summary">

                <strong>
                    ${formatNumber(
                        state.dataset.rowCount
                    )}
                </strong>

                <span>
                    Records
                </span>

            </div>


            <div class="report-summary">

                <strong>
                    ${formatNumber(
                        state.dataset.columnCount
                    )}
                </strong>

                <span>
                    Columns
                </span>

            </div>


            <div class="report-summary">

                <strong>
                    ${h.score}/100
                </strong>

                <span>
                    Data Health
                </span>

            </div>


            <div class="report-summary">

                <strong>
                    ${formatNumber(
                        a.anomalies.length
                    )}
                </strong>

                <span>
                    Anomalies
                </span>

            </div>

        </div>


        <h3>
            Executive Summary
        </h3>

        <p>
            ${escapeHTML(
                generateExecutiveSummary()
            )}
        </p>


        <h3>
            Key Findings
        </h3>

        ${
            findings.length
                ? findings
                    .map(
                        finding => `

                            <div class="report-finding">

                                <strong>
                                    ${escapeHTML(
                                        finding.title
                                    )}
                                </strong>

                                <p>
                                    ${escapeHTML(
                                        finding.text
                                    )}
                                </p>

                            </div>

                        `
                    )
                    .join("")
                : `
                    <p>
                        No major findings were identified
                        from the currently available analysis.
                    </p>
                `
        }


        <h3>
            Recommended Actions
        </h3>

        <p>

            ${
                h.missingCells
                    ? "Review and clean missing values before making high-confidence decisions. "
                    : ""
            }

            ${
                h.duplicateCount
                    ? "Investigate duplicate records to determine whether they represent valid repeated transactions. "
                    : ""
            }

            ${
                a.anomalies.length
                    ? "Review unusual records before relying on aggregate metrics. "
                    : ""
            }

            ${
                !h.missingCells &&
                !h.duplicateCount &&
                !a.anomalies.length
                    ? "Continue exploring product, category and value-level patterns through Explore Insights and AI Analyst."
                    : ""
            }

        </p>

    `;

}


/* =========================================================
   PRINT REPORT
========================================================= */

$("#printReportBtn").addEventListener(
    "click",
    () => {

        if (
            $("#reportPreview")
                .classList.contains(
                    "hidden"
                )
        ) {

            showNotification(
                "Generate a report first.",
                "info"
            );

            return;

        }

        window.print();

    }
);


/* =========================================================
   CSV EXPORT
========================================================= */

$("#downloadCsvBtn").addEventListener(
    "click",
    () => {

        if (
            !state.dataset.rows.length
        ) {

            showNotification(
                "No dataset is available for export.",
                "info"
            );

            return;

        }

        const rows = [

            [
                "Metric",
                "Value"
            ],

            [
                "Dataset",
                state.dataset.name
            ],

            [
                "Records",
                state.dataset.rowCount
            ],

            [
                "Columns",
                state.dataset.columnCount
            ],

            [
                "Data Health",
                state.health.score
            ],

            [
                "Total Value",
                state.analysis.totalAmount
            ],

            [
                "Average Value",
                state.analysis.averageAmount
            ],

            [
                "Anomalies",
                state.analysis.anomalies.length
            ]

        ];

        const csv =
            rows
                .map(
                    row =>
                        row
                            .map(
                                value =>
                                    `"${String(
                                        value ?? ""
                                    ).replaceAll(
                                        '"',
                                        '""'
                                    )}"`
                            )
                            .join(",")
                )
                .join("\n");

        const blob =
            new Blob(
                [csv],
                {
                    type:
                        "text/csv;charset=utf-8;"
                }
            );

        const url =
            URL.createObjectURL(
                blob
            );

        const link =
            document.createElement(
                "a"
            );

        link.href = url;

        link.download =
            "retail_intelligence_report.csv";

        link.click();

        URL.revokeObjectURL(
            url
        );

        showNotification(
            "Report CSV exported successfully.",
            "success"
        );

    }
);


/* =========================================================
   INITIALIZATION
========================================================= */

window.addEventListener(
    "DOMContentLoaded",
    () => {

        if (
            state.user.token
        ) {

            showApplication();

        } else {

            authPage.classList.remove(
                "hidden"
            );

            appPage.classList.add(
                "hidden"
            );

        }

    }
);


/* =========================================================
   SAFE JSON
========================================================= */

async function safeJSON(
    response
) {

    const text =
        await response.text();

    if (!text) return {};

    try {

        return JSON.parse(text);

    } catch {

        return {

            detail:
                text

        };

    }

}