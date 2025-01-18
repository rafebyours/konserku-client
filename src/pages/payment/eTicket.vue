<template>
  <MainLayout>
    <div class="ticket-page">
      <div class="ticket-container" v-if="transaction">
        <div class="ticket-upper">
          <h2 class="ticket-title text font-sans z-10 mb-4">Tiket Konser</h2>
          <div class="qr-code">
            <img :src="qrCodeUrl" alt="QR Code" />
          </div>
        </div>
        <div class="ticket-lower">
          <div class="detail-item">
            <strong>Nama:</strong>
            <span>{{ transaction.user_details.name }}</span>
          </div>
          <div class="detail-item">
            <strong>Konser:</strong>
            <span>{{ transaction.concert_details.title }}</span>
          </div>
          <div class="detail-item">
            <strong>Lokasi:</strong>
            <span>{{ transaction.concert_details.location }}</span>
          </div>
          <div class="detail-item">
            <strong>Tanggal:</strong>
            <span>{{ transaction.concert_details.date }}</span>
          </div>
          <div class="detail-item">
            <strong>Jumlah Tiket:</strong>
            <span>{{ transaction.quantity }}</span>
          </div>
          <div class="detail-item">
            <strong>Total Harga:</strong>
            <span>{{ formatRupiah(transaction.total_cost) }}</span>
          </div>
          <div class="ticket-notice">
            <p>
              Harap tunjukkan QR Code ini di gate masuk untuk mendapatkan tiket fisik dan gelang sesuai dengan jumlah tiket yang Anda beli.
            </p>
          </div>
        </div>
      </div>
      <button @click="downloadTicket" class="download-button" v-if="transaction">Unduh Tiket</button>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import MainLayout from '@/layouts/MainLayout.vue';
import { jsPDF } from "jspdf";
import QRCode from "qrcode";

const route = useRoute();
const transaction = ref(null);
const qrCodeUrl = ref("");
const router = useRouter();

const fetchTransactionDetails = async () => {
  try {
    const transactionId = route.params.id;
    const response = await fetch(`https://api-ticketconcert.vercel.app/api/ticket/${transactionId}`);
    const data = await response.json();

    console.log('Transaction Data:', data); // Tambahkan log ini untuk melihat respons dari API

    if (data.status === 'success') {
      transaction.value = data.data;
      generateQRCode(); // Generate QR Code setelah data diterima
    } else {
      router.push({ name: 'NotFoundPage' }); // Redirect if transaction not found
    }
  } catch (error) {
    console.error('Error fetching transaction:', error);
    router.push({ name: 'ErrorPage' }); // Redirect on error
  }
};

const formatRupiah = (number) => {
  return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR" }).format(number);
};

const generateQRCode = async () => {
  if (transaction.value) {
    const ticketInfo = JSON.stringify({
      name: transaction.value.userName,
      concert: transaction.value.concert_details.title,
      date: transaction.value.concert_details.date,
    });
    qrCodeUrl.value = await QRCode.toDataURL(ticketInfo);
  }
};

const downloadTicket = () => {
  const pdf = new jsPDF();
  const ticketElement = document.querySelector(".ticket-container");

  // Generate PDF
  pdf.html(ticketElement, {
    callback: (doc) => {
      doc.save("ticket.pdf");
    },
    x: 10,
    y: 10,
  });
};

onMounted(() => {
  fetchTransactionDetails();
});
</script>

<style scoped>
.ticket-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #ffff;
  min-height: 100vh;
}

.ticket-container {
  width: 100%;
  max-width: 400px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.ticket-upper {
  background-color: #f0fdf4;
  padding: 20px;
  text-align: center;
}

.ticket-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.qr-code img {
  max-width: 200px; /* Ukuran lebih besar */
  margin: 0 auto; /* Pusatkan gambar */
  display: block; /* Memastikan diatur sebagai block element */
  border-radius: 10px;
}

.ticket-lower {
  padding: 20px;
  border-top: 2px dashed #ccc;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  margin-bottom: 8px;
}

.detail-item strong {
  color: #444;
}

.ticket-notice {
  margin-top: 20px;
  padding: 10px;
  background-color: #f8f8f8;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 12px;
  color: #666;
  text-align: center;
}

.ticket-notice p {
  margin: 0;
  line-height: 1.5;
}

.download-button {
  margin-top: 20px;
  background-color: #22c55e;
  color: white;
  padding: 12px 20px;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.download-button:hover {
  background-color: #00796b;
}
</style>
