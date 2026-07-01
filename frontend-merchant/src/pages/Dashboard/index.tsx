import React, { useEffect } from 'react'
import { Card, Button, Space, Descriptions, Row, Col } from 'antd'
import { useNavigate } from 'react-router-dom'
import { ShopOutlined, ShoppingOutlined, BarChartOutlined, DollarOutlined } from '@ant-design/icons'
import { useAuthStore } from '../../store/authStore'
import { logout as logoutApi } from '../../api/auth'

const Dashboard: React.FC = () => {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()

  useEffect(() => {
    if (!user) {
      navigate('/login')
    }
  }, [user, navigate])

  const handleLogout = async () => {
    try {
      await logoutApi()
    } catch (error) {
      console.error(error)
    } finally {
      logout()
      navigate('/login')
    }
  }

  if (!user) {
    return null
  }

  return (
    <div style={{ padding: 24, background: '#f0f2f5', minHeight: '100vh' }}>
      <Card
        title="商户管理后台"
        extra={
          <Space>
            <Button onClick={handleLogout}>退出登录</Button>
          </Space>
        }
      >
        <Descriptions title="用户信息" bordered column={2}>
          <Descriptions.Item label="用户ID">{user.id}</Descriptions.Item>
          <Descriptions.Item label="用户名">{user.username}</Descriptions.Item>
          <Descriptions.Item label="手机号">{user.phone}</Descriptions.Item>
          <Descriptions.Item label="角色">{user.role === 'merchant' ? '商户' : '消费者'}</Descriptions.Item>
          <Descriptions.Item label="状态">{user.status === 'active' ? '正常' : '禁用'}</Descriptions.Item>
          <Descriptions.Item label="注册时间">{new Date(user.created_at).toLocaleString('zh-CN')}</Descriptions.Item>
        </Descriptions>

        <div style={{ marginTop: 24 }}>
          <h3>快捷入口</h3>
          <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
            <Col xs={24} sm={12} md={6}>
              <Card hoverable onClick={() => navigate('/products')} style={{ textAlign: 'center' }}>
                <ShoppingOutlined style={{ fontSize: 48, color: '#1890ff' }} />
                <h4>产品管理</h4>
                <p>管理您的产品</p>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card hoverable onClick={() => navigate('/orders')} style={{ textAlign: 'center' }}>
                <ShopOutlined style={{ fontSize: 48, color: '#52c41a' }} />
                <h4>订单管理</h4>
                <p>查看订单和收入</p>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card hoverable style={{ textAlign: 'center', opacity: 0.5 }}>
                <BarChartOutlined style={{ fontSize: 48, color: '#faad14' }} />
                <h4>收入统计</h4>
                <p>即将开放</p>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Card hoverable style={{ textAlign: 'center', opacity: 0.5 }}>
                <DollarOutlined style={{ fontSize: 48, color: '#f5222d' }} />
                <h4>提现管理</h4>
                <p>即将开放</p>
              </Card>
            </Col>
          </Row>
        </div>
      </Card>
    </div>
  )
}

export default Dashboard
