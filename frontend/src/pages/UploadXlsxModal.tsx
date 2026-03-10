import React, { useState } from 'react';
import { Modal, Upload, Button, List, Typography, Alert, Spin, message } from 'antd';
import { InboxOutlined, DownloadOutlined, CheckCircleOutlined } from '@ant-design/icons';

const { Dragger } = Upload;
const { Text, Paragraph } = Typography;

interface UploadXlsxModalProps {
  open: boolean;
  onClose: () => void;
}

interface PreviewData {
  policy_number: string;
  effective_date: string;
  premium: string;
  [key: string]: any;
}

const UploadXlsxModal: React.FC<UploadXlsxModalProps> = ({ open, onClose }) => {
  const [fileList, setFileList] = useState([]);
  const [preview, setPreview] = useState<PreviewData[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploaded, setUploaded] = useState(false);

  const checkFile = (file: File) => {
    const isXlsx = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
    if (!isXlsx) {
      message.error('You can only upload .xlsx files!');
      return Upload.LIST_IGNORE;
    }
    return true;
  };

  const handlePreview = async (file: File) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/policies/preview', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      });

      if (!response.ok) throw new Error('Preview generation failed');
      
      const data = await response.json();
      setPreview(data);
      setUploaded(true);
    } catch (error) {
      message.error('Failed to preview file');
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!fileList.length) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', fileList[0] as any);

    try {
      const response = await fetch('/api/policies/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      });

      if (!response.ok) throw new Error('Upload failed');
      
      message.success('ACORD data uploaded successfully');
      onClose();
    } catch (error) {
      message.error('Failed to upload file');
    } finally {
      setLoading(false);
    }
  };

  const props = {
    onRemove: (file: any) => {
      const index = fileList.indexOf(file);
      const newFileList = fileList.slice();
      newFileList.splice(index, 1);
      setFileList(newFileList);
      setPreview([]);
      setUploaded(false);
    },
    beforeUpload: (file: File) => {
      const check = checkFile(file);
      if (check === true) {
        setFileList([file]);
        handlePreview(file);
      }
      return false;
    },
    fileList,
  };

  return (
    <Modal
      title="Upload ACORD Data"
      open={open}
      onCancel={onClose}
      width={800}
      footer={
        <div>
          <Button onClick={onClose}>Cancel</Button>
          <Button 
            type="primary" 
            loading={loading} 
            onClick={handleUpload}
            disabled={!uploaded}
          >
            Confirm Upload
          </Button>
        </div>
      }
    >
      {!uploaded ? (
        <Dragger {...props} maxCount={1}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined style={{ fontSize: 48, color: '#1890ff' }} />
          </p>
          <p className="ant-upload-text">Click or drag ACORD file to upload</p>
          <p className="ant-upload-hint">
            Support for single .xlsx file. Please ensure the file contains valid ACORD data.
          </p>
        </Dragger>
      ) : (
        <>
          <Alert
            message="Preview"
            description={`Found ${preview.length} policies to import`}
            type="info"
            showIcon
            action={
              <Button icon={<DownloadOutlined />} size="small">
                Download Template
              </Button>
            }
          />
          <List
            size="small"
            dataSource={preview.slice(0, 5)}
            header={<Text strong>First 5 Policies Preview:</Text>}
            renderItem={(item) => (
              <List.Item>
                <Text>{item.policy_number}</Text> - 
                <Text type="secondary">{item.effective_date}</Text> - 
                <Text type="success">${parseFloat(item.premium).toLocaleString()}</Text>
              </List.Item>
            )}
          />
          {preview.length > 5 && (
            <Paragraph type="secondary" style={{ textAlign: 'center' }}>
              ... and {preview.length - 5} more
            </Paragraph>
          )}
        </>
      )}
      
      {loading && (
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Spin size="large" />
          <Paragraph>Processing file...</Paragraph>
        </div>
      )}
    </Modal>
  );
};

export default UploadXlsxModal;
