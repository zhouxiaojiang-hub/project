import client from './client'

export interface Product {
  id: number
  merchant_id: number
  name: string
  description?: string
  price: number
  stock: number
  image_url?: string
  status: string
  sales_count: number
  created_at: string
  updated_at: string
}

export interface ProductCreateRequest {
  name: string
  description?: string
  price: number
  stock: number
  status?: string
}

export interface ProductUpdateRequest {
  name?: string
  description?: string
  price?: number
  stock?: number
  status?: string
}

export interface ProductListResponse {
  total: number
  page: number
  page_size: number
  items: Product[]
}

/**
 * 创建产品
 */
export const createProduct = async (data: ProductCreateRequest): Promise<Product> => {
  const payload: any = { ...data }
  // 确保 price 是数字，不是字符串
  if (typeof payload.price !== 'number') {
    payload.price = parseFloat(payload.price)
  }
  if (typeof payload.stock !== 'number') {
    payload.stock = parseInt(payload.stock)
  }
  const response = await client.post('/api/v1/products', payload)
  return response.data
}

/**
 * 获取产品列表
 */
export const getProducts = async (params?: {
  merchant_id?: number
  keyword?: string
  status?: string
  page?: number
  page_size?: number
}): Promise<ProductListResponse> => {
  const response = await client.get('/api/v1/products', { params })
  return response.data
}

/**
 * 获取产品详情
 */
export const getProduct = async (id: number): Promise<Product> => {
  const response = await client.get(`/api/v1/products/${id}`)
  return response.data
}

/**
 * 更新产品
 */
export const updateProduct = async (id: number, data: ProductUpdateRequest): Promise<Product> => {
  const response = await client.put(`/api/v1/products/${id}`, data)
  return response.data
}

/**
 * 删除产品
 */
export const deleteProduct = async (id: number): Promise<void> => {
  await client.delete(`/api/v1/products/${id}`)
}

/**
 * 上传产品图片
 */
export const uploadProductImage = async (id: number, file: File): Promise<Product> => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await client.post(`/api/v1/products/${id}/upload-image`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}
