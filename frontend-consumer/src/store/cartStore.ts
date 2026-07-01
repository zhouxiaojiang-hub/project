import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface CartItem {
  product_id: number
  name: string
  price: number
  quantity: number
  image_url?: string
  merchant_id: number
}

interface CartState {
  items: CartItem[]
  addItem: (item: CartItem) => void
  removeItem: (productId: number) => void
  updateQuantity: (productId: number, quantity: number) => void
  clearCart: () => void
  getTotalAmount: () => number
  getTotalItems: () => number
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (item) => {
        const items = get().items
        const existingItem = items.find((i) => i.product_id === item.product_id)

        if (existingItem) {
          // 更新数量
          set({
            items: items.map((i) =>
              i.product_id === item.product_id
                ? { ...i, quantity: i.quantity + item.quantity }
                : i
            ),
          })
        } else {
          // 添加新商品
          set({ items: [...items, item] })
        }
      },

      removeItem: (productId) => {
        set({ items: get().items.filter((i) => i.product_id !== productId) })
      },

      updateQuantity: (productId, quantity) => {
        if (quantity <= 0) {
          get().removeItem(productId)
        } else {
          set({
            items: get().items.map((i) =>
              i.product_id === productId ? { ...i, quantity } : i
            ),
          })
        }
      },

      clearCart: () => {
        set({ items: [] })
      },

      getTotalAmount: () => {
        return get().items.reduce((total, item) => total + item.price * item.quantity, 0)
      },

      getTotalItems: () => {
        return get().items.reduce((total, item) => total + item.quantity, 0)
      },
    }),
    {
      name: 'cart-storage',
    }
  )
)
