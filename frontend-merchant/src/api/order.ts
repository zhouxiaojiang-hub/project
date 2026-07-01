import client from './client'

export interface OrderItem {
  id: number
  product_id: number
  product_name: string
  unit_price: number
  quantity: number
  subtotal: number
}

export interface Order {
  id: number
  order_no: string
  consumer_id: number
  merchant_id: number
  total_amount: number
  commission: number
  merchant_income: number
  status: string
  payment_method: string
  paid_at?: string
  created_at: string
  items: OrderItem[]
}

export interface OrderCreateRequest {
  items: Array<{ product_id: number; quantity: number }>
  payment_method?: string
}

export interface PaymentRequest {
  order_id: number
}

export interface PaymentResponse {
  order_id: number
  order_no: string
  payment_method: string
  amount: number
  payment_url?: string
  qr_code?: string
}

/**
 * 创建订单
 */
export const createOrder = async (data: OrderCreateRequest): Promise<Order> => {
  const response = await client.post('/api/v1/orders', data)
  return response.data
}

/**
 * 获取订单列表
 */
export const getOrders = async (params?: {
  page?: number
  page_size?: number
}): Promise<{ total: number; items: Order[] }> => {
  const response = await client.get('/api/v1/orders', { params })
  return response.data
}

/**
 * 获取订单详情
 */
export const getOrder = async (id: number): Promise<Order> => {
  const response = await client.get(`/api/v1/orders/${id}`)
  return response.data
}

/**
 * 取消订单
 */
export const cancelOrder = async (id: number): Promise<Order> => {
  const response = await client.post(`/api/v1/orders/${id}/cancel`)
  return response.data
}

/**
 * Mock支付
 */
export const mockPayment = async (data: PaymentRequest): Promise<PaymentResponse> => {
  const response = await client.post('/api/v1/orders/payment/mock', data)
  return response.data
}
