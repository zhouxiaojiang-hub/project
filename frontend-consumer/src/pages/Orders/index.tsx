import React, { useState, useEffect } from 'react'
import { Card, Table, Tag, Button, Space, message, Modal } from 'antd'
import { useNavigate } from 'react-router-dom'
import { getOrders, cancelOrder, Order } from '../../api/order'

const Orders: React.FC = () => {
  const navigate = useNavigate()
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(false)
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pageSize] = useState(10)
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null)
  const [detailModalOpen, setDetailModalOpen] = useState(false)

  useEffect(() => {
    loadOrders()
  }, [page])

  const loadOrders = async () => {
    setLoading(true)
    try {
      const response = await getOrders({ page, page_size: pageSize })
      setOrders(response.items)
      setTotal(response.total)
    } catch (error) {
      message.error('加载订单列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (orderId: number) => {
    try {
      await cancelOrder(orderId)
      message.success('订单已取消')
      loadOrders()
    } catch (error: any) {
      message.error(error.response?.data?.detail || '取消订单失败')
    }
  }

  const showDetail = (order: Order) => {
    setSelectedOrder(order)
    setDetailModalOpen(true)
  }

  const getStatusTag = (status: string) => {
    const statusMap: { [key: string]: { color: string; text: string } } = {
      pending: { color: 'orange', text: '待支付' },
      paid: { color: 'green', text: '已支付' },
      cancelled: { color: 'default', text: '已取消' },
    }
    const statusInfo = statusMap[status] || { color: 'default', text: status }
    return <Tag color={statusInfo.color}>{statusInfo.text}</Tag>
  }

  const columns = [
    {
      title: '订单号',
      dataIndex: 'order_no',
      key: 'order_no',
    },
    {
      title: '总金额',
      dataIndex: 'total_amount',
      key: 'total_amount',
      render: (amount: number) => `¥${amount.toFixed(2)}`,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => getStatusTag(status),
    },
    {
      title: '支付方式',
      dataIndex: 'payment_method',
      key: 'payment_method',
      render: (method: string) => method === 'mock' ? 'Mock支付' : method,
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Order) => (
        <Space size="small">
          <Button type="link" size="small" onClick={() => showDetail(record)}>
            查看详情
          </Button>
          {record.status === 'pending' && (
            <Button
              type="link"
              danger
              size="small"
              onClick={() => {
                Modal.confirm({
                  title: '确定取消此订单吗？',
                  onOk: () => handleCancel(record.id),
                })
              }}
            >
              取消订单
            </Button>
          )}
        </Space>
      ),
    },
  ]

  return (
    <div style={{ padding: 24, background: '#f0f2f5', minHeight: '100vh' }}>
      <Card
        title="我的订单"
        extra={
          <Button onClick={() => navigate('/')}>返回首页</Button>
        }
      >
        <Table
          columns={columns}
          dataSource={orders}
          rowKey="id"
          loading={loading}
          pagination={{
            current: page,
            pageSize: pageSize,
            total: total,
            onChange: setPage,
            showTotal: (total) => `共 ${total} 个订单`,
          }}
        />
      </Card>

      <Modal
        title="订单详情"
        open={detailModalOpen}
        onCancel={() => setDetailModalOpen(false)}
        footer={null}
        width={700}
      >
        {selectedOrder && (
          <div>
            <div style={{ marginBottom: 16 }}>
              <p><strong>订单号：</strong>{selectedOrder.order_no}</p>
              <p><strong>状态：</strong>{getStatusTag(selectedOrder.status)}</p>
              <p><strong>创建时间：</strong>{new Date(selectedOrder.created_at).toLocaleString('zh-CN')}</p>
              {selectedOrder.paid_at && (
                <p><strong>支付时间：</strong>{new Date(selectedOrder.paid_at).toLocaleString('zh-CN')}</p>
              )}
            </div>

            <Table
              dataSource={selectedOrder.items}
              rowKey="id"
              pagination={false}
              columns={[
                { title: '产品名称', dataIndex: 'product_name', key: 'product_name' },
                { title: '单价', dataIndex: 'unit_price', key: 'unit_price', render: (p: number) => `¥${p.toFixed(2)}` },
                { title: '数量', dataIndex: 'quantity', key: 'quantity' },
                { title: '小计', dataIndex: 'subtotal', key: 'subtotal', render: (s: number) => `¥${s.toFixed(2)}` },
              ]}
            />

            <div style={{ marginTop: 16, textAlign: 'right' }}>
              <p><strong>总金额：</strong><span style={{ color: '#f5222d', fontSize: 18 }}>¥{selectedOrder.total_amount.toFixed(2)}</span></p>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}

export default Orders
