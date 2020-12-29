import React, { useState } from 'react';
import { Form, Input, Button, Checkbox, Alert, Space } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import auth from '../../services/authService';
import { Link } from 'react-router-dom';


const Login = () => {

  const [ loginFailed, setLoginFailed ] = useState();

  const handleSubmit = async (values) => {
    const credentials = {...values};
    delete credentials.remember;
    try {
      await auth.login(credentials);
      window.location = '/';
    } catch (error) { setLoginFailed(true); }
  };

  return (
    <Space>
      <Form
        name="normal_login"
        className="login-form"
        initialValues={{
          remember: true,
        }}
        onFinish={handleSubmit}
      >
        {
          loginFailed &&
            <Alert
              style={{marginBottom: 15}}
              type="error"
              message="Invalid Registered Email/Password"
            />
        }
        <Form.Item
          name="email"
          rules={[
            {
              type: 'email',              
              required: true,
              message: 'Please input your Registered email!',
            },
          ]}
        >
          <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Email" />
        </Form.Item>
        <Form.Item
          name="password"
          rules={[
            {
              required: true,
              message: 'Please input your Password!',
            },
          ]}
        >
          <Input
            prefix={<LockOutlined className="site-form-item-icon" />}
            type="password"
            placeholder="Password"
          />
        </Form.Item>
        <Form.Item>
          <Form.Item name="remember" valuePropName="checked" noStyle>
            <Checkbox>Remember me</Checkbox>
          </Form.Item>
          <Link to="" className="login-form-forgot">Forget password</Link>
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" className="login-form-button">
            Log in
          </Button>
        </Form.Item>
      </Form>
    </Space>
  );
};

export default Login;