<template>
    <div class="users-list">
      <h1>User List</h1>
      <ul v-if="users.length > 0">
        <li v-for="(user, index) in users" :key="index">
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
        </li>
      </ul>
      <p v-else>Loading users...</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        users: [], // Array untuk menyimpan data pengguna
      };
    },
    mounted() {
      this.fetchUsers();
    },
    methods: {
      async fetchUsers() {
        try {
          const response = await axios.get("http://127.0.0.1:5000/users");
          this.users = response.data; // Simpan data pengguna ke array
        } catch (error) {
          console.error("Error fetching users:", error);
        }
      },
    },
  };
  </script>
  
  <style>
  .users-list {
    font-family: Arial, sans-serif;
    padding: 20px;
  }
  li {
    margin-bottom: 20px;
  }
  </style>
  