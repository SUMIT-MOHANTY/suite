import React from 'react';
import { Table, Space, Button, Badge, Popconfirm, message } from 'antd';
import { useApiQuery, useApiMutation } from '../hooks/useApiQuery';

const CaptivesList: React.FC = () => {
  const { data, isLoading, error } = useApiQuery('captives', '/v1/captives/');
  const deleteMutation = useApiMutation('/v1/captives/', 'delete');

  const handleDelete = async (id: number) => {
    try {
      await deleteMutation.mutateAsync({ id });
      message.success('Captive deleted successfully');
    } catch (error) {
      message.error('Failed to delete captive');
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: (a: any, b: any) => a.name.localeCompare(b.name),
    },
    {
      title: 'Policy Count',
      dataIndex: 'policy_count',
      key: 'policy_count',
      render: (count: number) => <Badge count={count} />,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      filters: [
        { text: 'Active', value: 'active' },
        { text: 'Inactive', value: 'inactive' },
      ],
      onFilter: (value: any, record: any) => record.status === value,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record: any) => (
        <Space>
          <Button type="link">Edit</Button>
          <Popconfirm
            title="Are you sure to delete this captive?"
            onConfirm={() => handleDelete(record.id)}
          >
            <Button type="link" danger>Delete</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <h1>Captives Management</h1>
      <Table
        dataSource={data?.results}
        columns={columns}
        loading={isLoading}
        rowKey="id"
      />
    </div>
  );
};

export default CaptivesList;
