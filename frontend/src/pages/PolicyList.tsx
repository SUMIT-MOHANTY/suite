import React, { useState } from 'react';
import { Table, Select, Button, Input, Space, message } from 'antd';
import { DownloadOutlined, PlusOutlined, UploadOutlined } from '@ant-design/icons';
import { useApiQuery } from '../hooks/useApiQuery';
import { downloadBlob } from '../utils/downloadBlob';
import IssuePolicyModal from './IssuePolicyModal';
import UploadXlsxModal from './UploadXlsxModal';
import type { ColumnsType } from 'antd/es/table';

const { Option } = Select;
const { Search } = Input;

interface PolicySummary {
  id: number;
  captive_id: number;
  policy_number: string;
  effective_date: string;
  expiration_date: string;
  premium: string;
  status: 'ACTIVE' | 'EXPIRED' | 'CANCELLED' | 'PENDING_RENEWAL';
  renewal_target_id?: number;
}

interface PolicyListProps {
  captiveId?: number;
}

const PolicyList: React.FC<PolicyListProps> = ({ captiveId }) => {
  const [status, setStatus] = useState<string | undefined>(undefined);
  const [search, setSearch] = useState<string>('');
  const [issueModalOpen, setIssueModalOpen] = useState(false);
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [selectedPolicy, setSelectedPolicy] = useState<number | null>(null);

  const queryParams = new URLSearchParams();
  if (status) queryParams.set('status', status);
  if (captiveId) queryParams.set('captive_id', String(captiveId));
  if (search) queryParams.set('search', search);

  const { data, isLoading, refetch } = useApiQuery<{ results: PolicySummary[]; count: number }>(
    ['policies', status, search, captiveId],
    `/api/policies?${queryParams.toString()}`
  );

  const handleExport = async (policyId: number) => {
    try {
      const response = await fetch(`/api/policies/${policyId}/export`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });
      if (!response.ok) throw new Error('Export failed');
      
      const blob = await response.blob();
      const filename = `policy-${policyId}-binder.xlsx`;
      downloadBlob(blob, filename);
    } catch (error) {
      message.error('Failed to export policy');
    }
  };

  const columns: ColumnsType<PolicySummary> = [
    {
      title: 'Policy Number',
      dataIndex: 'policy_number',
      key: 'policy_number',
      sorter: true,
    },
    {
      title: 'Effective Date',
      dataIndex: 'effective_date',
      key: 'effective_date',
      render: (date: string) => new Date(date).toLocaleDateString(),
      sorter: true,
    },
    {
      title: 'Expiration Date',
      dataIndex: 'expiration_date',
      key: 'expiration_date',
      render: (date: string) => new Date(date).toLocaleDateString(),
      sorter: true,
    },
    {
      title: 'Premium',
      dataIndex: 'premium',
      key: 'premium',
      render: (premium: string) => `$${parseFloat(premium).toLocaleString()}`,
      sorter: true,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const colors = {
          ACTIVE: 'green',
          EXPIRED: 'volcano',
          CANCELLED: 'red',
          PENDING_RENEWAL: 'geekblue',
        };
        return (
          <span style={{ color: colors[status as keyof typeof colors] }}>
            {status.replace('_', ' ')}
          </span>
        );
      },
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => handleExport(record.id)}
            type="text"
          >
            Download
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Space style={{ marginBottom: 16 }} wrap>
        <Select
          placeholder="Filter by status"
          value={status}
          onChange={setStatus}
          style={{ width: 200 }}
          allowClear
        >
          <Option value="ACTIVE">ACTIVE</Option>
          <Option value="EXPIRED">EXPIRED</Option>
          <Option value="CANCELLED">CANCELLED</Option>
          <Option value="PENDING_RENEWAL">PENDING RENEWAL</Option>
        </Select>
        
        <Search
          placeholder="Search policies"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ width: 200 }}
          allowClear
        />
        
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setIssueModalOpen(true)}
        >
          Issue Policy
        </Button>
        
        <Button
          icon={<UploadOutlined />}
          onClick={() => setUploadModalOpen(true)}
        >
          Upload ACORD
        </Button>
      </Space>

      <Table
        loading={isLoading}
        dataSource={data?.results || []}
        columns={columns}
        rowKey="id"
        pagination={{
          showSizeChanger: true,
          showTotal: (total) => `Total ${total} policies`,
          pageSizeOptions: [10, 20, 50, 100],
        }}
      />

      <IssuePolicyModal
        open={issueModalOpen}
        onClose={() => {
          setIssueModalOpen(false);
          refetch();
        }}
        captiveId={captiveId || 0}
      />

      <UploadXlsxModal
        open={uploadModalOpen}
        onClose={() => {
          setUploadModalOpen(false);
          refetch();
        }}
      />
    </div>
  );
};

export default PolicyList;
