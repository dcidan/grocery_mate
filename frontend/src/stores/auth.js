import { ref, computed } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

// State
const token = ref(localStorage.getItem('token') || null)
const user = ref(null)

// Getters
export const isAuthenticated = computed(() => !!token.value)

// Actions
export async function login(email, password) {
  try {
    const formData = new FormData()
    formData.append('username', email)  // OAuth2 expects 'username'
    formData.append('password', password)
    
    const response = await axios.post(`${API_URL}/auth/login`, formData)
    token.value = response.data.access_token
    localStorage.setItem('token', token.value)
    
    // Get user info
    await fetchCurrentUser()
    return true
  } catch (error) {
    console.error('Login failed:', error)
    return false
  }
}

export async function register(email, username, password) {
  try {
    await axios.post(`${API_URL}/auth/register`, {
      email,
      username,
      password
    })
    // Auto-login after registration
    return await login(email, password)
  } catch (error) {
    console.error('Registration failed:', error)
    throw error
  }
}

export async function fetchCurrentUser() {
  try {
    const response = await axios.get(`${API_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    user.value = response.data
  } catch (error) {
    console.error('Failed to fetch user:', error)
    logout()
  }
}

export function logout() {
  token.value = null
  user.value = null
  localStorage.removeItem('token')
}

export function getToken() {
  return token.value
}

export function getUser() {
  return user.value
}