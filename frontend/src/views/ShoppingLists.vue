<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold text-gray-900">Shopping Lists</h2>
      <button
        @click="showCreateList = true"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
      >
        + Create List
      </button>
    </div>

    <!-- Shopping Lists Grid -->
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="list in shoppingLists" :key="list.id" class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900">{{ list.name }}</h3>
            <button
              @click="deleteList(list.id)"
              class="text-red-600 hover:text-red-800"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
          
          <div class="space-y-2 mb-4">
            <div v-for="item in list.items" :key="item.id" class="flex items-center justify-between py-2 border-b">
              <div class="flex items-center space-x-3">
                <input
                  type="checkbox"
                  :checked="item.is_purchased"
                  @change="toggleItemStatus(item.id, !item.is_purchased)"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                >
                <span :class="item.is_purchased ? 'line-through text-gray-500' : 'text-gray-900'">
                  {{ item.item_name }} ({{ item.quantity }} {{ item.unit }})
                </span>
              </div>
              <button
                @click="deleteItem(item.id)"
                class="text-red-600 hover:text-red-800"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <button
            @click="openAddItem(list.id)"
            class="w-full mt-2 inline-flex items-center justify-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            + Add Item
          </button>

          <div class="mt-3 text-sm text-gray-500">
            {{ list.items.filter(i => i.is_purchased).length }} / {{ list.items.length }} completed
          </div>
        </div>
      </div>
    </div>

    <div v-if="shoppingLists.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <p class="text-gray-500">No shopping lists yet. Create your first list to get started!</p>
    </div>

    <!-- Create List Modal -->
    <div v-if="showCreateList" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Create Shopping List</h3>
            <form @submit.prevent="createList">
              <div>
                <label class="block text-sm font-medium text-gray-700">List Name</label>
                <input v-model="newListName" type="text" required
                  class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              </div>
              <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3">
                <button type="submit"
                  class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 sm:col-start-2 sm:text-sm">
                  Create
                </button>
                <button type="button" @click="showCreateList = false"
                  class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:col-start-1 sm:text-sm">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Item Modal -->
    <div v-if="showAddItem" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Add Item</h3>
            <form @submit.prevent="addItem">
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Item Name</label>
                  <input v-model="newItem.item_name" type="text" required
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Quantity</label>
                    <input v-model.number="newItem.quantity" type="number" step="0.1" required
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Unit</label>
                    <select v-model="newItem.unit" required
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                      <option>kg</option>
                      <option>g</option>
                      <option>L</option>
                      <option>ml</option>
                      <option>pieces</option>
                      <option>cups</option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3">
                <button type="submit"
                  class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 sm:col-start-2 sm:text-sm">
                  Add
                </button>
                <button type="button" @click="showAddItem = false"
                  class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:col-start-1 sm:text-sm">
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
import { ref, onMounted } from 'vue'
import { shoppingListsAPI } from '../services/api.js'

const shoppingLists = ref([])
const showCreateList = ref(false)
const showAddItem = ref(false)
const newListName = ref('')
const currentListId = ref(null)
const newItem = ref({
  item_name: '',
  quantity: 1,
  unit: 'kg',
  is_purchased: false
})

const loadShoppingLists = async () => {
  try {
    const response = await shoppingListsAPI.getAll()
    shoppingLists.value = response.data
  } catch (error) {
    console.error('Error loading shopping lists:', error)
  }
}

const createList = async () => {
  try {
    await shoppingListsAPI.create({ name: newListName.value })
    await loadShoppingLists()
    showCreateList.value = false
    newListName.value = ''
  } catch (error) {
    console.error('Error creating list:', error)
  }
}

const deleteList = async (id) => {
  if (confirm('Are you sure you want to delete this shopping list?')) {
    try {
      await shoppingListsAPI.delete(id)
      await loadShoppingLists()
    } catch (error) {
      console.error('Error deleting list:', error)
    }
  }
}

const openAddItem = (listId) => {
  currentListId.value = listId
  showAddItem.value = true
}

const addItem = async () => {
  try {
    await shoppingListsAPI.addItem(currentListId.value, newItem.value)
    await loadShoppingLists()
    showAddItem.value = false
    newItem.value = {
      item_name: '',
      quantity: 1,
      unit: 'kg',
      is_purchased: false
    }
  } catch (error) {
    console.error('Error adding item:', error)
  }
}

const toggleItemStatus = async (itemId, isPurchased) => {
  try {
    await shoppingListsAPI.updateItem(itemId, isPurchased)
    await loadShoppingLists()
  } catch (error) {
    console.error('Error updating item:', error)
  }
}

const deleteItem = async (itemId) => {
  try {
    await shoppingListsAPI.deleteItem(itemId)
    await loadShoppingLists()
  } catch (error) {
    console.error('Error deleting item:', error)
  }
}

onMounted(() => {
  loadShoppingLists()
})
</script>
