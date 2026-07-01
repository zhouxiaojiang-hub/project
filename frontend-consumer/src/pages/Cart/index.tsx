import React from 'react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const getImageSrc = (url: string | undefined) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return API_BASE + url
}
import { Card, Table, Button, InputNumber, Image, Empty, message, Space, Popconfirm } from 'antd'
import { DeleteOutlined, ShoppingOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useCartStore } from '../../store/cartStore'
import { createOrder, mockPayment } from '../../api/order'

const Cart: React.FC = () => {
  const navigate = useNavigate()
  const { items, removeItem, updateQuantity, clearCart, getTotalAmount } = useCartStore()
  const [loading, setLoading] = React.useState(false)

  const handleCheckout = async () => {
    if (items.length === 0) {
      message.warning('购物车为空')
      return
    }

    // 检查是否所有商品来自同一商户
    const merchantIds = [...new Set(items.map(item => item.merchant_id))]
    if (merchantIds.length > 1) {
      message.error('一个订单只能包含同一商户的产品，请分别下单')
      return
    }

    setLoading(true)
    try {
      // 创建订单
      const order = await createOrder({
        items: items.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity,
        })),
        payment_method: 'mock',
      })

      message.success('订单创建成功')

      // 自动支付（Mock）
      await mockPayment({ order_id: order.id })

      message.success('支付成功！')
      clearCart()
      navigate('/orders')
    } catch (error: any) {
      message.error(error.response?.data?.detail || '下单失败')
    } finally {
      setLoading(false)
    }
  }

  const columns = [
    {
      title: '图片',
      dataIndex: 'image_url',
      key: 'image_url',
      width: 100,
      render: (url: string, record: any) => (
        url ? (
          <Image src={getImageSrc(url)} alt={record.name} width={60} height={60} style={{ objectFit: 'cover' }} />
        ) : (
          <div style={{ width: 60, height: 60, background: '#f0f0f0', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 12, color: '#999' }}>
            暂无图片
          </div>
        )
      ),
    },
    {
      title: '产品名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '单价',
      dataIndex: 'price',
      key: 'price',
      render: (price: number) => `¥${price.toFixed(2)}`,
    },
    {
      title: '数量',
      dataIndex: 'quantity',
      key: 'quantity',
      render: (quantity: number, record: any) => (
        <InputNumber
          min={1}
          value={quantity}
          onChange={(value) => updateQuantity(record.product_id, value || 1)}
        />
      ),
    },
    {
      title: '小计',
      key: 'subtotal',
      render: (_: any, record: any) => `¥${(record.price * record.quantity).toFixed(2)}`,
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: any) => (
        <Popconfirm
          title="确定删除此商品吗？"
          onConfirm={() => removeItem(record.product_id)}
          okText="确定"
          cancelText="取消"
        >
          <Button type="link" danger icon={<DeleteOutlined />}>
            删除
          </Button>
        </Popconfirm>
      ),
    },
  ]

  if (items.length === 0) {
    return (
      <div style={{ padding: 24, background: '#f0f2f5', minHeight: '100vh' }}>
        <Card>
          <Empty description="购物车为空">
            <Button type="primary" onClick={() => navigate('/products')}>
              去购物
            </Button>
          </Empty>
        </Card>
      </div>
    )
  }

  return (
    <div style={{ padding: 24, background: '#f0f2f5', minHeight: '100vh' }}>
      <Card
        title="购物车"
        extra={
          <Space>
            <Button onClick={() => navigate('/products')}>继续购物</Button>
            <Button onClick={() => navigate('/')}>返回首页</Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={items}
          rowKey="product_id"
          pagination={false}
        />

        <div style={{ marginTop: 24, textAlign: 'right' }}>
          <div style={{ fontSize: 18, marginBottom: 16 }}>
            <span>总计：</span>
            <span style={{ color: '#f5222d', fontSize: 24, fontWeight: 'bold' }}>
              ¥{getTotalAmount().toFixed(2)}
            </span>
          </div>
          <Space>
            <Popconfirm
              title="确定清空购物车吗？"
              onConfirm={clearCart}
              okText="确定"
              cancelText="取消"
            >
              <Button>清空购物车</Button>
            </Popconfirm>
            <Button
              type="primary"
              size="large"
              icon={<ShoppingOutlined />}
              loading={loading}
              onClick={handleCheckout}
            >
              结算
            </Button>
          </Space>
        </div>
      </Card>
    </div>
  )
}

export default Cart
