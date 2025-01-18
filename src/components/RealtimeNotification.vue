<template>
  <div>
    <!-- Modal untuk menampilkan notifikasi -->
    <div
      v-if="showModal"
      class="fixed top-5 left-1/2 transform -translate-x-1/2 bg-white p-4 rounded-lg shadow-xl w-80 flex items-center space-x-4 z-50"
    >
      <!-- Ikon di sebelah kiri -->
      <img src="../image/logo/icon-only.png" alt="Logo" class="w-12 h-12 object-contain" />

      <!-- Konten notifikasi -->
      <div>
        <h2 class="text-lg font-semibold text-gray-800 mb-1">{{ notificationTitle }}</h2>
        <p class="text-sm text-gray-600">{{ notificationMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { onValue, ref as firebaseRef } from "firebase/database";
import { db } from "../firebaseConfig";
import { PushNotifications } from "@capacitor/push-notifications";

export default {
  data() {
    return {
      messages: [],
      lastMessage1: null,
      lastMessage2: null,
      showModal: false,
      notificationTitle: "",
      notificationMessage: "",
    };
  },
  mounted() {
    const messagesRef = firebaseRef(db, "messages");
    onValue(messagesRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        const message1 = data.message1;
        const message2 = data.message2;

        this.messages = [message1, message2];

        if (this.lastMessage1 !== message1 || this.lastMessage2 !== message2) {
          this.lastMessage1 = message1;
          this.lastMessage2 = message2;
          this.showNotification(message1, message2);
        }
      }
    });

    PushNotifications.requestPermissions().then((result) => {
      if (result.receive === "granted") {
        PushNotifications.register();

        PushNotifications.addListener("pushNotificationReceived", (notification) => {
          this.showNotification(notification.title, notification.body);
        });

        PushNotifications.addListener("pushNotificationActionPerformed", (notification) => {
          console.log("Push notification action performed: ", notification);
        });
      }
    });
  },
  methods: {
    showNotification(title, message) {
      this.notificationTitle = title;
      this.notificationMessage = message;
      this.showModal = true;

      setTimeout(() => {
        this.showModal = false;
      }, 5000); // Menyembunyikan notifikasi setelah 5 detik
    },
  },
};
</script>

<style scoped>
/* Ukuran dan styling modal */
.fixed {
  max-width: 320px; /* Lebar modal lebih proporsional */
  border: 1px solid #e5e7eb; /* Border ringan untuk tampilan rapi */
}
img {
  border-radius: 50%; /* Ikon bulat */
  background-color: #f3f4f6; /* Latar belakang ikon */
}
.text-lg {
  font-size: 1.125rem; /* Ukuran font judul lebih besar */
}
.text-sm {
  font-size: 0.875rem; /* Ukuran font deskripsi */
}
</style>
