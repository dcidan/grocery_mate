<template>
  <div class="min-h-screen bg-gray-50">
    <nav v-if="isAuthenticated" class="bg-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-2xl font-bold text-primary-600">🥗 GroceryMate</h1>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                to="/"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="$route.path === '/' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                Dashboard
              </router-link>
              <router-link
                to="/ingredients"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="$route.path === '/ingredients' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                Ingredients
              </router-link>
              <router-link
                to="/shopping"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="$route.path === '/shopping' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                Shopping Lists
              </router-link>
              <router-link
                to="/recipes"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="$route.path === '/recipes' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                Recipes
              </router-link>
            </div>
          </div>
          
        <!-- Add logout button -->
          <div class="flex items-center">
            <span class="text-sm text-gray-700 mr-4">{{ user?.username }}</span>
            <button
              @click="handleLogout"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-gray-700 hover:bg-gray-100"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
     <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>
<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { isAuthenticated, getUser, logout } from './stores/auth'

const router = useRouter()
const user = computed(() => getUser())

const handleLogout = () => {
  logout()
  router.push('/login')
}
</script>
