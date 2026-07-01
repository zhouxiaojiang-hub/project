import React, { useState, useEffect } from 'react'
import { Table, Button, Space, Modal, Form, Input, InputNumber, Select, Upload, message, Image, Popconfirm, Card } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import { getProducts, createProduct, updateProduct, deleteProduct, uploadProductImage, Product } from '../../api/product'

const { TextArea } = Input
const { Option } = Select

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const Products: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pageSize] = useState(10)

  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingProduct, setEditingProduct] = useState<Product | null>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    loadProducts()
  }, [page])

  const loadProducts = async () => {
    setLoading(true)
    try {
      const response = await getProducts({ page, page_size: pageSize })
      setProducts(response.items)
      setTotal(response.total)
    } catch (error) {
      message.error('加载产品列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setEditingProduct(null)
    form.resetFields()
    setIsModalOpen(true)
  }

  const handleEdit = (product: Product) => {
    setEditingProduct(product)
    form.setFieldsValue({
      name: product.name,
      description: product.description,
      price: product.price,
      stock: product.stock,
      status: product.status,
    })
    setIsModalOpen(true)
  }

  const handleDelete = async (id: number) => {
    try {
      await deleteProduct(id)
      message.success('删除成功')
      loadProducts()
    } catch (error: any) {
      message.error(error.response?.data?.detail || '删除失败')
    }
  }

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()
      if (editingProduct) {
        await updateProduct(editingProduct.id, values)
        message.success('更新成功')
      } else {
        await createProduct(values)
        message.success('创建成功')
      }
      setIsModalOpen(false)
      loadProducts()
    } catch (error: any) {
      message.error(error.response?.data?.detail || '操作失败')
    }
  }

  const handleUploadImage = async (productId: number, file: File) => {
    try {
      await uploadProductImage(productId, file)
      message.success('图片上传成功')
      loadProducts()
    } catch (error: any) {
      message.error(error.response?.data?.detail || '图片上传失败')
    }
    return false
  }

  const getImageSrc = (imageUrl: string | undefined) => {
    if (!imageUrl) return ''
    if (imageUrl.startsWith('http')) return imageUrl
    return API_BASE + imageUrl
  }

  const columns = [
    {
      title: '图片',
      dataIndex: 'image_url',
      key: 'image_url',
      width: 140,
      render: (url: string, record: Product) => (
        <Space direction="vertical" size={4} align="center">
          {url ? (
            <Image
              src={getImageSrc(url)}
              alt={record.name}
              width={80}
              height={80}
              style={{ objectFit: 'cover', borderRadius: 8 }}
            />
          ) : (
            <div style={{
              width: 80, height: 80, background: '#f5f5f5',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              borderRadius: 8, color: '#999', fontSize: 12
            }}>
              暂无图片
            </div>
          )}
          <Upload
            showUploadList={false}
            beforeUpload={(file) => {
              handleUploadImage(record.id, file)
              return false
            }}
            accept="image/png,image/jpeg,image/jpg"
          >
            <Button size="small" type="link">上传</Button>
          </Upload>
        </Space>
      ),
    },
    { title: '产品名称', dataIndex: 'name', key: 'name' },
    { title: '价格', dataIndex: 'price', key: 'price', render: (p: number) => `¥${Number(p).toFixed(2)}` },
    { title: '库存', dataIndex: 'stock', key: 'stock', render: (s: number) => s === -1 ? '不限' : s },
    { title: '销量', dataIndex: 'sales_count', key: 'sales_count' },
    {
      title: '状态', dataIndex: 'status', key: 'status',
      render: (s: string) => <span style={{ color: s === 'on_sale' ? 'green' : 'gray' }}>{s === 'on_sale' ? '在售' : '下架'}</span>
    },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at', render: (d: string) => new Date(d).toLocaleDateString('zh-CN') },
    {
      title: '操作', key: 'action',
      render: (_: any, record: Product) => (
        <Space size="small">
          <Button type="link" size="small" icon={<EditOutlined />} onClick={() => handleEdit(record)}>编辑</Button>
          <Popconfirm title="确定删除此产品吗？" onConfirm={() => handleDelete(record.id)} okText="确定" cancelText="取消">
            <Button type="link" danger size="small" icon={<DeleteOutlined />}>删除</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div style={{ padding: 24 }}>
      <Card
        title="产品管理"
        extra={<Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>新增产品</Button>}
      >
        <Table
          columns={columns}
          dataSource={products}
          rowKey="id"
          loading={loading}
          pagination={{
            current: page, pageSize: pageSize, total: total, onChange: setPage,
            showTotal: (t: number) => `共 ${t} 个产品`,
          }}
        />
      </Card>

      <Modal
        title={editingProduct ? '编辑产品' : '新增产品'}
        open={isModalOpen}
        onOk={handleSubmit}
        onCancel={() => setIsModalOpen(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item label="产品名称" name="name" rules={[{ required: true, message: '请输入产品名称' }]}>
            <Input placeholder="请输入产品名称" />
          </Form.Item>
          <Form.Item label="产品描述" name="description">
            <TextArea rows={4} placeholder="请输入产品描述" />
          </Form.Item>
          <Form.Item label="价格" name="price" rules={[{ required: true, message: '请输入价格' }]}>
            <InputNumber min={0} step={0.01} precision={2} style={{ width: '100%' }} prefix="¥" placeholder="请输入价格" />
          </Form.Item>
          <Form.Item label="库存" name="stock" rules={[{ required: true, message: '请输入库存' }]} tooltip="-1表示不限库存">
            <InputNumber min={-1} style={{ width: '100%' }} placeholder="-1表示不限库存" />
          </Form.Item>
          <Form.Item label="状态" name="status" initialValue="on_sale" rules={[{ required: true, message: '请选择状态' }]}>
            <Select>
              <Option value="on_sale">在售</Option>
              <Option value="off_shelf">下架</Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Products
