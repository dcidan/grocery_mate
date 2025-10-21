<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold text-gray-900">Ingredients</h2>
      <button
        @click="showAddModal = true"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
      >
        + Add Ingredient
      </button>
    </div>

    <!-- Filter Tabs -->
    <div class="mb-6 border-b border-gray-200">
      <nav class="-mb-px flex space-x-8">
        <button
          @click="filterLocation = null"
          :class="filterLocation === null ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
        >
          All ({{ ingredients.length }})
        </button>
        <button
          @click="filterLocation = 'Fridge'"
          :class="filterLocation === 'Fridge' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
        >
          ❄️ Fridge
        </button>
        <button
          @click="filterLocation = 'Pantry'"
          :class="filterLocation === 'Pantry' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
        >
          🗄️ Pantry
        </button>
      </nav>
    </div>

    <!-- Ingredients List -->
    <div class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul class="divide-y divide-gray-200">
        <li v-for="ingredient in filteredIngredients" :key="ingredient.id" class="hover:bg-gray-50">
          <div class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <h3 class="text-lg font-medium text-gray-900">{{ ingredient.name }}</h3>
                <div class="mt-2 flex items-center text-sm text-gray-500 space-x-4">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ ingredient.category }}
                  </span>
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    {{ ingredient.location }}
                  </span>
                  <span>Quantity: {{ ingredient.quantity }} {{ ingredient.unit }}</span>
                  <span v-if="ingredient.expiry_date" :class="isExpiringSoon(ingredient.expiry_date) ? 'text-red-600 font-semibold' : ''">
                    Expires: {{ formatDate(ingredient.expiry_date) }}
                  </span>
                </div>
              </div>
              <div class="flex space-x-2">
                <button
                  @click="editIngredient(ingredient)"
                  class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Edit
                </button>
                <button
                  @click="deleteIngredientConfirm(ingredient.id)"
                  class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </li>
      </ul>
      <div v-if="filteredIngredients.length === 0" class="text-center py-12">
        <p class="text-gray-500">No ingredients found. Add your first ingredient to get started!</p>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || editingIngredient" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              {{ editingIngredient ? 'Edit Ingredient' : 'Add New Ingredient' }}
            </h3>
            <form @submit.prevent="saveIngredient">
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Name</label>
                  <input v-model="form.name" type="text" required
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Category</label>
                  <select v-model="form.category" required
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                    <option>Vegetables</option>
                    <option>Fruits</option>
                    <option>Dairy</option>
                    <option>Meat</option>
                    <option>Grains</option>
                    <option>Beverages</option>
                    <option>Condiments</option>
                    <option>Other</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Location</label>
                  <select v-model="form.location" required
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                    <option>Fridge</option>
                    <option>Pantry</option>
                  </select>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Quantity</label>
                    <input v-model.number="form.quantity" type="number" step="0.1" required
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Unit</label>
                    <select v-model="form.unit" required
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                      <option>kg</option>
                      <option>g</option>
                      <option>L</option>
                      <option>ml</option>
                      <option>pieces</option>
                      <option>cups</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Expiry Date (Optional)</label>
                  <input v-model="form.expiry_date" type="date"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                </div>
              </div>
              <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                <button type="submit"
                  class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none sm:col-start-2 sm:text-sm">
                  Save
                </button>
                <button type="button" @click="closeModal"
                  class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:col-start-1 sm:text-sm">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ingredientsAPI } from '../services/api.js'

const ingredients = ref([])
const filterLocation = ref(null)
const showAddModal = ref(false)
const editingIngredient = ref(null)
const form = ref({
  name: '',
  category: 'Vegetables',
  location: 'Fridge',
  quantity: 1,
  unit: 'kg',
  expiry_date: null
})

const filteredIngredients = computed(() => {
  if (!filterLocation.value) return ingredients.value
  return ingredients.value.filter(i => i.location === filterLocation.value)
})

const loadIngredients = async () => {
  try {
    const response = await ingredientsAPI.getAll()
    ingredients.value = response.data
  } catch (error) {
    console.error('Error loading ingredients:', error)
  }
}

const saveIngredient = async () => {
  try {
    if (editingIngredient.value) {
      await ingredientsAPI.update(editingIngredient.value.id, form.value)
    } else {
      await ingredientsAPI.create(form.value)
    }
    await loadIngredients()
    closeModal()
  } catch (error) {
    console.error('Error saving ingredient:', error)
    alert('Error saving ingredient')
  }
}

const editIngredient = (ingredient) => {
  editingIngredient.value = ingredient
  form.value = { ...ingredient }
}

const deleteIngredientConfirm = async (id) => {
  if (confirm('Are you sure you want to delete this ingredient?')) {
    try {
      await ingredientsAPI.delete(id)
      await loadIngredients()
    } catch (error) {
      console.error('Error deleting ingredient:', error)
    }
  }
}

const closeModal = () => {
  showAddModal.value = false
  editingIngredient.value = null
  form.value = {
    name: '',
    category: 'Vegetables',
    location: 'Fridge',
    quantity: 1,
    unit: 'kg',
    expiry_date: null
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const isExpiringSoon = (expiryDate) => {
  const today = new Date()
  const expiry = new Date(expiryDate)
  const diffDays = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24))
  return diffDays <= 7 && diffDays >= 0
}

onMounted(() => {
  loadIngredients()
})
</script>
