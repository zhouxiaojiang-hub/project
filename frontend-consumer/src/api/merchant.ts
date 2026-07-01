import client from './client'

export interface Merchant {
  id: number
  user_id: number
  shop_name: string
  description?: string
  category?: string
  location?: string
  cover_url?: string
  created_at: string
}

/**
 * 获取商户列表
 */
export const getMerchants = async (params?: {
  keyword?: string
  category?: string
  page?: number
  page_size?: number
}): Promise<{ total: number; items: Merchant[] }> => {
  const response = await client.get('/api/v1/merchants', { params })
  return response.data
}

/**
 * 获取商户详情
 */
export const getMerchant = async (id: number): Promise<Merchant> => {
  const response = await client.get(`/api/v1/merchants/${id}`)
  return response.data
}
