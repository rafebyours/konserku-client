// firebase-messaging-sw.js
importScripts('https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/11.2.0/firebase-messaging.js');


const firebaseConfig = {
    apiKey: "AIzaSyDVGA1JmFiSykGr--odSNNg6fZPvSp89jI",
    authDomain: "ticketconcert-59a85.firebaseapp.com",
    projectId: "ticketconcert-59a85",
    storageBucket: "ticketconcert-59a85.appspot.com",
    messagingSenderId: "873524263353",
    appId: "1:873524263353:android:0d264f0a069bb31051de68",
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function (payload) {
  console.log('Background message received: ', payload);
  // Customize notification here
  self.registration.showNotification(payload.notification.title, {
    body: payload.notification.body,
    icon: payload.notification.icon,
  });
});
