import React from 'react';
import { Form, Input, Select, DatePicker, Button, notification } from 'antd';
import moment from 'moment';
import { useHistory, useLocation, useParams } from 'react-router-dom';
import { saveStaff } from '../../services/staffService';

const layout = {
  labelCol: { span: 5, },
  wrapperCol: { span: 10, },
};

const tailLayout = { wrapperCol: { offset: 5, span: 16, }, };

const StaffForm = () => {

  const history = useHistory();
  const location = useLocation();
  const { id } = useParams();

  const handleSubmit = async (values) => {
    const data = {...values};
    if (data.date_of_birth)
      data.date_of_birth = moment(values.date_of_birth).format('YYYY-MM-DD');
    try {
      const {data: staff } = await saveStaff(data);
      history.push(`/staff/${staff.id}/`, staff);
      notification['success']({
        message: 'Staff Details saved'
      })
    } catch (error) {
      const { detail } = error.data;

      notification['error']({
        message: detail
      })
    }
  }

  const getInitialValues = id => {
    if (id) {
      const { state } = location;
      if (state.date_of_birth) {state.date_of_birth = moment(state.date_of_birth)}
      return state;
    } else {return null;}
  }

  const { Option } = Select;

  return (
    <Form
      {...layout}
      name="Personal Info"
      initialValues={ id && getInitialValues(id) }
      onFinish={handleSubmit}
    >
      <Form.Item label="id" name="id" hidden={true}>
        <Input />
      </Form.Item>
      <Form.Item name="title" label="Title">
          <Select allowClear>
          <Option value="Mr">Mr.</Option>
          <Option value="Ms">Ms.</Option>
          </Select>
      </Form.Item>
      <Form.Item
        label="First Name"
        name="first_name"
        rules={[ { required: true, message: 'Please input your first name!', }, ]}
      >
        <Input />
      </Form.Item>
      <Form.Item label="Middle Name" name="middle_name">
        <Input />
      </Form.Item>
      <Form.Item
        label="Last Name"
        name="last_name"
        rules={[ { required: true, message: 'Please input your last name!', }, ]}
      >
        <Input />
      </Form.Item>
      <Form.Item name="sex" label="Sex" rules={[ {required: true} ]}>
        <Select allowClear>
          <Option value="M">Male</Option>
          <Option value="F">Female</Option>
        </Select>
      </Form.Item>
      <Form.Item label="Date of Birth" name="date_of_birth">
          <DatePicker/>
      </Form.Item>
      <Form.Item label="Address" name="address">
        <Input />
      </Form.Item>
      <Form.Item label="Mobile" name="phone">
        <Input />
      </Form.Item>
      <Form.Item label="Email" name="email">
        <Input type="email"/>
      </Form.Item>
      <Form.Item label="SSSNIT" name="sssnit_no">
        <Input />
      </Form.Item>
      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          { id ? "Update" : "Create" }
        </Button>
      </Form.Item>
    </Form>
  );
};
export default StaffForm;