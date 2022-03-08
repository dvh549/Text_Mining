// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAq1pvOn7qnHGblKFOylAZIlSrhL2f9WCw",
  authDomain: "textmining-6c1ef.firebaseapp.com",
  projectId: "textmining-6c1ef",
  storageBucket: "textmining-6c1ef.appspot.com",
  messagingSenderId: "359583053714",
  appId: "1:359583053714:web:30d956d4cc77d25940b34b"
};

// Initialize Firebase
// const app = initializeApp(firebaseConfig);
// // Initialize Firebase
initializeApp(firebaseConfig)
export const db = getFirestore()