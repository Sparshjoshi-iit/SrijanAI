// ✅ Firebase Configuration (No imports needed)
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, GoogleAuthProvider, signInWithPopup, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-auth.js";
 // 🔥 Animate the login box
 gsap.from(".container", { 
    opacity: 0, 
    scale: 0.8, 
    duration: 1, 
    ease: "back.out(1.7)" 
});

const firebaseConfig = {
    apiKey: "AIzaSyDTXOwNs_lLyx_5u-vQ3_dSUoDTEVgT-5I",
    authDomain: "vehicletelemeterysystem.firebaseapp.com",
    databaseURL: "https://vehicletelemeterysystem-default-rtdb.firebaseio.com",
    projectId: "vehicletelemeterysystem",
    storageBucket: "vehicletelemeterysystem.appspot.com",
    messagingSenderId: "366500314879",
    appId: "1:366500314879:web:d794290b17b2edc0e496ca",
    measurementId: "G-S4CZZBYRZB"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// 🔹 Register User
function registerUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            alert("Registration successful! Please log in.");
        })
        .catch((error) => {
            alert("Registration failed: " + error.message);
        });
}

// 🔹 Log in User with Email/Password
function loginUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            alert("Login successful!");

            // Store user role in localStorage
            localStorage.setItem("userRole", "user");

            // Redirect to the respective dashboard
            window.location.href = "dashboard.html";
        })
        .catch((error) => {
            alert("Login failed: " + error.message);
        });
}

// 🔹 Google Sign-In (Fixed)
document.getElementById("google-signin")?.addEventListener("click", () => {
    signInWithPopup(auth, provider)
        .then((result) => {
            alert(`Welcome, ${result.user.displayName}! Redirecting to Dashboard...`);
            window.location.href = "dashboard.html";

            // ✅ Now properly inside the `.then()` block
            result.user.getIdToken().then((idToken) => {
                sendTokenToBackend(idToken);
            });
        })
        .catch((error) => {
            if (error.code === "auth/popup-closed-by-user") {
                alert("Google Sign-In popup was closed. Please try again.");
            } else {
                alert("Google Sign-In Failed: " + error.message);
            }
        });
});

// 🔹 Send Token to Backend
function sendTokenToBackend(idToken) {
    console.log("Sending token to backend...");
    fetch("http://127.0.0.1:8000/users", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${idToken}`,
        },
        body: JSON.stringify({ username: "test_user", password: idToken }),
    })
    .then(response => response.json())
    .then(data => console.log("Backend Response:", data))
    .catch(error => console.error("Error sending token:", error));
}

// 🔹 Attach register & login event listeners
document.getElementById("register").addEventListener("click", (e) => {
    e.preventDefault();
    registerUser();
});

document.getElementById("login").addEventListener("click", (e) => {
    e.preventDefault();
    loginUser();
});
function selectTab(selectedTab,url) {
    let tabs = document.querySelectorAll(".tab");

    // Remove 'active' class from all tabs
    tabs.forEach(tab => tab.classList.remove("active"));

    // Add 'active' class to the clicked tab
    selectedTab.classList.add("active");
    window.location.href=url
}
