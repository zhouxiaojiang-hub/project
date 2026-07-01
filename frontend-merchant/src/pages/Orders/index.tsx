import React, { useState, useEffect } from 'react'
import { Card, Table, Tag, Button, Space, message, Modal, Statistic, Row, Col } from 'antd'
import { useNavigate } from 'react-router-dom'
import { getOrders, Order } from '../../api/order'

const Orders: React.FC = () => {
  const navigate = useNavigate()
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(false)
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pageSize] = useState(10)
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null)
  const [detailModalOpen, setDetailModalOpen] = useState(false)

  // 统计数据
  const [stats, setStats] = useState({
    totalIncome: 0,
    totalOrders: 0,
    paidOrders: 0,
  })

  useEffect(() => {
    loadOrders()
  }, [page])

  const loadOrders = async () => {
    setLoading(true)
    try {
      const response = await getOrders({ page, page_size: pageSize })
      setOrders(response.items)
      setTotal(response.total)

      // 计算统计数据
      const totalIncome = response.items
        .filter((o: Order) => o.status === 'paid')
        .reduce((sum: number, o: Order) => sum + o.merchant_income, 0)
      const paidOrders = response.items.filter((o: Order) => o.status === 'paid').length

      setStats({
        totalIncome,
        totalOrders: response.total,
        paidOrders,
      })
    } catch (error) {
      message.error('加载订单列表失败')
    } finally {
      setLoading(false)
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
      title: '平台抽佣',
      dataIndex: 'commission',
      key: 'commission',
      render: (commission: number) => `¥${commission.toFixed(2)}`,
    },
    {
      title: '实收金额',
      dataIndex: 'merchant_income',
      key: 'merchant_income',
      render: (income: number) => (
        <span style={{ color: '#52c41a', fontWeight: 'bold' }}>
          ¥{income.toFixed(2)}
        </span>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => getStatusTag(status),
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
        <Button type="link" size="small" onClick={() => showDetail(record)}>
          查看详情
        </Button>
      ),
    },
  ]

  return (
    <div style={{ padding: 24, background: '#f0f2f5', minHeight: '100vh' }}>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="累计收入"
              value={stats.totalIncome}
              precision={2}
              prefix="¥"
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="订单总数"
              value={stats.totalOrders}
              suffix="个"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="已支付订单"
              value={stats.paidOrders}
              suffix="个"
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      <Card
        title="订单列表"
        extra={
          <Button onClick={() => navigate('/dashboard')}>返回控制台</Button>
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
              <p><strong>订单金额：</strong>¥{selectedOrder.total_amount.toFixed(2)}</p>
              <p><strong>平台抽佣（10%）：</strong><span style={{ color: '#ff4d4f' }}>-¥{selectedOrder.commission.toFixed(2)}</span></p>
              <p><strong>实收金额：</strong><span style={{ color: '#52c41a', fontSize: 18, fontWeight: 'bold' }}>¥{selectedOrder.merchant_income.toFixed(2)}</span></p>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}

export default Orders
