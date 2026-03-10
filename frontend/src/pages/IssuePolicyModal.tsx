import React, { useState } from 'react';
import { Modal, Steps, Form, Input, DatePicker, InputNumber, message } from 'antd';
import dayjs from 'dayjs';

const { Step } = Steps;
const { TextArea } = Input;

interface PolicyFormData {
  policy_number: string;
  effective_date: string;
  premium: string;
  coverage_limit: string;
  deductible: string;
  notes?: string;
}

interface IssuePolicyModalProps {
  open: boolean;
  onClose: () => void;
  captiveId: number;
}

const IssuePolicyModal: React.FC<IssuePolicyModalProps> = ({ open, onClose, captiveId }) => {
  const [current, setCurrent] = useState(0);
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const steps = [
    {
      title: 'Basic Details',
      content: (
        <>
          <Form.Item
            label="Policy Number"
            name="policy_number"
            rules={[{ required: true, message: 'Please enter policy number' }]}
          >
            <Input placeholder="e.g., POL-2024-001" />
          </Form.Item>
          
          <Form.Item
            label="Effective Date"
            name="effective_date"
            rules={[{ required: true, message: 'Please select effective date' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item
            label="Premium Amount"
            name="premium"
            rules={[{ required: true, message: 'Please enter premium amount' }]}
          >
            <InputNumber
              style={{ width: '100%' }}
              placeholder="0.00"
              addonBefore="$"
              min={0}
              step={0.01}
              parser={(value: string) => value.replace('$', '')}
            />
          </Form.Item>
        </>
      ),
    },
    {
      title: 'Coverage Details',
      content: (
        <>
          <Form.Item
            label="Coverage Limit"
            name="coverage_limit"
            rules={[{ required: true, message: 'Please enter coverage limit' }]}
          >
            <InputNumber
              style={{ width: '100%' }}
              placeholder="0.00"
              addonBefore="$"
              min={0}
              step={0.01}
            />
          </Form.Item>
          
          <Form.Item
            label="Deductible"
            name="deductible"
            rules={[{ required: true, message: 'Please enter deductible amount' }]}
          >
            <InputNumber
              style={{ width: '100%' }}
              placeholder="0.00"
              addonBefore="$"
              min={0}
              step={0.01}
            />
          </Form.Item>
          
          <Form.Item
            label="Notes"
            name="notes"
          >
            <TextArea rows={4} placeholder="Additional notes..." />
          </Form.Item>
        </>
      ),
    },
  ];

  const handleNext = async () => {
    try {
      const fields = current === 0 
        ? ['policy_number', 'effective_date', 'premium']
        : ['coverage_limit', 'deductible', 'notes'];
      
      await form.validateFields(fields);
      setCurrent(current + 1);
    } catch (error) {
      // Validation failed
    }
  };

  const handlePrev = () => {
    setCurrent(current - 1);
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const values = await form.validateFields();
      
      const formattedValues = {
        ...values,
        effective_date: typeof values.effective_date === 'object' 
          ? values.effective_date.format('YYYY-MM-DD')
          : values.effective_date,
        premium: String(values.premium),
        coverage_limit: String(values.coverage_limit),
        deductible: String(values.deductible),
      };

      const response = await fetch('/api/policies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          ...formattedValues,
          captive_id: captiveId,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create policy');
      }

      message.success('Policy created successfully');
      form.resetFields();
      setCurrent(0);
      onClose();
    } catch (error) {
      message.error('Failed to create policy');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title="Issue New Policy"
      open={open}
      onCancel={onClose}
      width={600}
      footer={
        <div>
          {current > 0 && (
            <Button onClick={handlePrev} style={{ marginRight: 8 }}>
              Previous
            </Button>
          )}
          {current < steps.length - 1 && (
            <Button type="primary" onClick={handleNext}>
              Next
            </Button>
          )}
          {current === steps.length - 1 && (
            <Button type="primary" loading={loading} onClick={handleSubmit}>
              Create Policy
            </Button>
          )}
        </div>
      }
    >
      <Steps current={current} style={{ marginBottom: 24 }}>
        {steps.map((step) => (
          <Step key={step.title} title={step.title} />
        ))}
      </Steps>
      <Form form={form} layout="vertical">
        {steps[current]?.content}
      </Form>
    </Modal>
  );
};

export default IssuePolicyModal;
