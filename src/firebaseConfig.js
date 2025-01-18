// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getDatabase } from 'firebase/database';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCtduyPT4wSlL2gooCi5IcHyCQhKEVEL_Q",
  authDomain: "ticketconcert-59a85.firebaseapp.com",
  databaseURL: "https://ticketconcert-59a85-default-rtdb.firebaseio.com",
  projectId: "ticketconcert-59a85",
  storageBucket: "ticketconcert-59a85.firebasestorage.app",
  messagingSenderId: "873524263353",
  appId: "1:873524263353:web:fc541ad795c0f6d651de68",
  measurementId: "G-B7SCV708CK"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getDatabase(app);

export { db };