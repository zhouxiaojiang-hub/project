import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Input, Button, Image, message, Empty, Pagination, Badge } from 'antd'
import { SearchOutlined, ShoppingCartOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { getProducts, Product } from '../../api/product'
import { useCartStore } from '../../store/cartStore'

const { Search } = Input
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const getImageSrc = (imageUrl: string | undefined) => {
  if (!imageUrl) return ''
  if (imageUrl.startsWith('http')) return imageUrl
  return API_BASE + imageUrl
}

const ProductList: React.FC = () => {
  const navigate = useNavigate()
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pageSize] = useState(12)
  const [keyword, setKeyword] = useState('')
  const { addItem, getTotalItems } = useCartStore()

  useEffect(() => {
    loadProducts()
  }, [page, keyword])

  const loadProducts = async () => {
    setLoading(true)
    try {
      const response = await getProducts({
        keyword: keyword || undefined,
        status: 'on_sale',
        page,
        page_size: pageSize,
      })
      setProducts(response.items)
      setTotal(response.total)
    } catch (error) {
      message.error('加载产品列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (value: string) => {
    setKeyword(value)
    setPage(1)
  }

  const handleAddToCart = (product: Product) => {
    addItem({
      product_id: product.id,
      name: product.name,
      price: Number(product.price),
      quantity: 1,
      image_url: product.image_url,
      merchant_id: product.merchant_id,
    })
    message.success(`${product.name} 已加入购物车`)
  }

  return (
    <div style={{ padding: 24, background: '#f0f2f5', minHeight: '100vh' }}>
      <Card>
        <div style={{ marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Search
            placeholder="搜索产品"
            allowClear
            enterButton={<Button type="primary" icon={<SearchOutlined />}>搜索</Button>}
            size="large"
            onSearch={handleSearch}
            style={{ maxWidth: 600 }}
          />
          <Badge count={getTotalItems()} showZero>
            <Button type="primary" icon={<ShoppingCartOutlined />} size="large" onClick={() => navigate('/cart')}>
              购物车
            </Button>
          </Badge>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '60px 0' }}>加载中...</div>
        ) : products.length === 0 ? (
          <Empty description="暂无产品" />
        ) : (
          <>
            <Row gutter={[16, 16]}>
              {products.map((product) => (
                <Col xs={24} sm={12} md={8} lg={6} key={product.id}>
                  <Card
                    hoverable
                    cover={
                      product.image_url ? (
                        <Image
                          src={getImageSrc(product.image_url)}
                          alt={product.name}
                          height={200}
                          style={{ objectFit: 'cover' }}
                          preview={{ src: getImageSrc(product.image_url) }}
                        />
                      ) : (
                        <div style={{ height: 200, background: '#f0f0f0', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#999' }}>
                          暂无图片
                        </div>
                      )
                    }
                    actions={[
                      <Button type="primary" icon={<ShoppingCartOutlined />} onClick={() => handleAddToCart(product)}>
                        加入购物车
                      </Button>,
                    ]}
                  >
                    <Card.Meta
                      title={<div style={{ fontSize: 16, fontWeight: 'bold' }}>{product.name}</div>}
                      description={
                        <div>
                          <div style={{ color: '#f5222d', fontSize: 20, fontWeight: 'bold', marginBottom: 8 }}>
                            ¥{Number(product.price).toFixed(2)}
                          </div>
                          {product.description && (
                            <div style={{ color: '#666', fontSize: 12, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                              {product.description}
                            </div>
                          )}
                          <div style={{ color: '#999', fontSize: 12, marginTop: 8 }}>
                            销量: {product.sales_count}
                            {product.stock !== -1 && ` | 库存: ${product.stock}`}
                          </div>
                        </div>
                      }
                    />
                  </Card>
                </Col>
              ))}
            </Row>
            <div style={{ marginTop: 24, textAlign: 'center' }}>
              <Pagination current={page} pageSize={pageSize} total={total} onChange={setPage}
                showTotal={(total) => `共 ${total} 个产品`} />
            </div>
          </>
        )}
      </Card>
    </div>
  )
}

export default ProductList
