<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; // Import axios untuk mengirim permintaan HTTP

const router = useRouter();
const name = ref('');
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');

const isNameEmpty = ref(false);
const isUsernameEmpty = ref(false);
const isEmailEmpty = ref(false);
const isPasswordEmpty = ref(false);
const isConfirmPasswordEmpty = ref(false);
const isPasswordMismatch = ref(false);

const showPassword = ref(false);
const showConfirmPassword = ref(false);

// Snackbar
const snackbarVisible = ref(false);
const snackbarMessage = ref('');

// Modal for Terms and Conditions
const showTermsModal = ref(false);
const agreeToTerms = ref(false);

// Loading indicator
const isLoading = ref(false);

// Show success modal
const showSuccessModal = ref(false); 

// Validasi Email
const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

const register = () => {
  // Reset validation flags
  isNameEmpty.value = !name.value;
  isUsernameEmpty.value = !username.value;
  isEmailEmpty.value = !email.value;
  isPasswordEmpty.value = !password.value;
  isConfirmPasswordEmpty.value = !confirmPassword.value;
  isPasswordMismatch.value = password.value !== confirmPassword.value;

  // Validasi email
  if (!isValidEmail(email.value)) {
    showSnackbar("Please enter a valid email.");
    return;
  }

  // Validasi password mismatch
  if (isPasswordMismatch.value) {
    showSnackbar("Passwords do not match");
  }

  if (
    !isNameEmpty.value &&
    !isUsernameEmpty.value &&
    !isEmailEmpty.value &&
    !isPasswordEmpty.value &&
    !isConfirmPasswordEmpty.value &&
    !isPasswordMismatch.value
  ) {
    showTermsModal.value = true; // Show terms modal before registering
  }
};

// Confirm registration after accepting terms
const confirmRegistration = async () => {
  if (!agreeToTerms.value) {
    showSnackbar("You must agree to the terms and conditions");
    return;
  }

  try {
    isLoading.value = true; // Show loading indicator
    // Mengirim data pendaftaran ke API Flask
    const response = await axios.post('https://api-ticketconcert.vercel.app/register', {
      name: name.value,
      username: username.value,
      email: email.value,
      password: password.value
    });
    isLoading.value = false; // Hide loading indicator

    // Cek apakah pendaftaran berhasil
    if (response.status === 200) {
      showSuccessModal.value = true;
    } else {
      showSnackbar(response.data.message || "Registration failed. Please try again.");
    }
  } catch (error) {
    isLoading.value = false; // Hide loading indicator
    console.error(error);
    showSnackbar("Error during registration. Please try again.");
  } finally {
    showTermsModal.value = false;
  }
};

// Redirect to home after successful registration
const redirectToHome = () => {
  showSuccessModal.value = false;
  router.push('/login'); // Arahkan ke halaman login setelah pendaftaran berhasil
};

// Show snackbar function
const showSnackbar = (message) => {
  snackbarMessage.value = message;
  snackbarVisible.value = true;
  setTimeout(() => {
    snackbarVisible.value = false;
  }, 3000); // Hide snackbar after 3 seconds
};

const isVisible = ref(false);
onMounted(() => {
  isVisible.value = true;
});

const beforeEnter = (el) => {
  el.style.opacity = 0;
};

const enter = (el, done) => {
  el.offsetHeight; // Trigger reflow
  el.style.transition = 'opacity 0.5s';
  el.style.opacity = 1;
  done();
};

const leave = (el, done) => {
  el.style.transition = 'opacity 0.5s';
  el.style.opacity = 0;
  done();
};
</script>

<template>
  <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
    <main v-if="isVisible" class="p-10 w-full absolute justify-center items-center h-screen overflow-auto">
      <div class="w-full max-w-xs">
        <div class="flex items-center mb-5">
          <button @click="$router.push('/')" class="btn flex items-center mr-3">
            <i class="fas fa-arrow-left"></i>
          </button>
          <h1 class="text-2xl font-sans2">Register</h1>
        </div>

        <!-- Field Name -->
        <label class="form-control w-full max-w-xs">
          <div class="label">
            <span class="label-text">Name</span>
          </div>
          <label :class="[ 'input input-bordered flex items-center gap-2', isNameEmpty ? 'border-red-500' : '', ]">
            <i class="fas fa-user opacity-70"></i>
            <input v-model="name" type="text" class="grow" placeholder="Name" required />
          </label>
          <span v-if="isNameEmpty" class="text-red-500 text-sm mt-1">Name is required</span>
        </label>

        <!-- Field Username -->
        <label class="form-control w-full max-w-xs mt-3">
          <div class="label">
            <span class="label-text">Username</span>
          </div>
          <label :class="[ 'input input-bordered flex items-center gap-2', isUsernameEmpty ? 'border-red-500' : '', ]">
            <i class="fas fa-user-circle opacity-70"></i>
            <input v-model="username" type="text" class="grow" placeholder="Username" required />
          </label>
          <span v-if="isUsernameEmpty" class="text-red-500 text-sm mt-1">Username is required</span>
        </label>

        <!-- Field Email -->
        <label class="form-control w-full max-w-xs mt-3">
          <div class="label">
            <span class="label-text">Email</span>
          </div>
          <label :class="[ 'input input-bordered flex items-center gap-2', isEmailEmpty ? 'border-red-500' : '', ]">
            <i class="fas fa-envelope opacity-70"></i>
            <input v-model="email" type="email" class="grow" placeholder="Email" required />
          </label>
          <span v-if="isEmailEmpty" class="text-red-500 text-sm mt-1">Email is required</span>
        </label>

        <!-- Field Password -->
        <label class="form-control w-full max-w-xs mt-3">
          <div class="label">
            <span class="label-text">Password</span>
          </div>
          <label :class="[ 'input input-bordered flex items-center gap-2', isPasswordEmpty ? 'border-red-500' : '', ]">
            <i class="fas fa-lock opacity-70"></i>
            <input v-model="password" :type="showPassword ? 'text' : 'password'" class="grow" placeholder="Password" required />
            <button type="button" @click="showPassword = !showPassword">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </label>
          <span v-if="isPasswordEmpty" class="text-red-500 text-sm mt-1">Password is required</span>
        </label>

        <!-- Field Confirm Password -->
        <label class="form-control w-full max-w-xs mt-3">
          <div class="label">
            <span class="label-text">Confirm Password</span>
          </div>
          <label :class="[ 'input input-bordered flex items-center gap-2', isConfirmPasswordEmpty || isPasswordMismatch ? 'border-red-500' : '', ]">
            <i class="fas fa-lock opacity-70"></i>
            <input v-model="confirmPassword" :type="showConfirmPassword ? 'text' : 'password'" class="grow" placeholder="Confirm Password" required />
            <button type="button" @click="showConfirmPassword = !showConfirmPassword">
              <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </label>
          <span v-if="isConfirmPasswordEmpty" class="text-red-500 text-sm mt-1">Confirmation is required</span>
          <span v-if="isPasswordMismatch" class="text-red-500 text-sm mt-1">Passwords do not match</span>
        </label>

        <div class="text-sm mt-3">
          Have an account? <a class="link" @click="$router.push('/login')">Login</a>
        </div>

        <div class="flex justify-end mt-5">
          <button class="btn bg-secondary" @click="register" :disabled="isLoading">Register</button>
        </div>

        <!-- Snackbar -->
        <transition name="fade">
          <div v-if="snackbarVisible" class="snackbar w-full max-w-xs mt-3 bg-red-500 text-white py-2 px-4 rounded-lg shadow-lg">
            {{ snackbarMessage }}
          </div>
        </transition>

        <!-- Terms Modal -->
        <transition name="fade">
          <div v-if="showTermsModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 w-full">
            <div class="bg-white p-6 rounded-lg w-full max-w-xs">
              <h2 class="text-lg font-semibold mb-4">Terms and Conditions</h2>
              <p class="mb-4">
                Please review and agree to our terms and conditions to complete your registration.
              </p>
              <label class="flex items-center">
                <input type="checkbox" v-model="agreeToTerms" class="mr-2" />
                <span>I agree to the terms and conditions</span>
              </label>
              <div class="flex justify-end mt-4">
                <button class="btn bg-gray-500 text-white mr-2" @click="showTermsModal = false">Cancel</button>
                <button class="btn bg-blue-500 text-white" @click="confirmRegistration">Confirm</button>
              </div>
            </div>
          </div>
        </transition>

        <!-- Success Modal -->
        <transition name="fade">
          <div v-if="showSuccessModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 w-full">
            <div class="bg-white p-6 rounded-lg w-full max-w-xs">
              <h2 class="text-lg font-semibold mb-4">Registration Successful</h2>
              <p class="mb-4">Your account has been created successfully!</p>
              <div class="flex justify-end mt-4">
                <button class="btn bg-primary text-white" @click="redirectToHome">Go to Login</button>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </main>
  </transition>
</template>

<style scoped>
.snackbar {
  transition: opacity 0.3s ease;
}
</style>
