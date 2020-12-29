import React, { useState } from 'react';
import { Layout, Menu } from 'antd';
import { NavLink, Route, Switch, Redirect } from 'react-router-dom';
import {
  MenuUnfoldOutlined,
  MenuFoldOutlined,
} from '@ant-design/icons';
import routes from '../routes';

const { Header, Sider, Content } = Layout;

const AdminLayout = () => {

    const [collapsed, setCollapsed] = useState(false);

    const toggle = () => setCollapsed(!collapsed);

    return (
        <Layout>
        <Sider trigger={null} collapsible collapsed={collapsed}>
          <div className="logo" />
          <Menu theme="dark" mode="inline" defaultSelectedKeys={['0']}>
            {
              routes.filter((r)=>r.display).map((route) => (
                <Menu.Item key={route.key} icon={route.icon}>
                  <NavLink to={route.path}>{route.displayName}</NavLink>
                </Menu.Item>
              ))
            }
          </Menu>
        </Sider>
        <Layout className="site-layout">
          <Header className="site-layout-background" style={{ padding: 0 }}>
            {React.createElement(collapsed ? MenuUnfoldOutlined : MenuFoldOutlined, {
              className: 'trigger',
              onClick: toggle,
            })}
          </Header>
          <Content
            className="site-layout-background"
            style={{
              margin: '24px 16px',
              padding: 24,
              minHeight: 280,
            }}
          >
            <Switch>
              {
                routes.map((route) => (
                  <Route
                    key={route.key}
                    path={route.path}
                    exact={route.exact}
                    children={route.content}
                  />
                ))
              }
              <Redirect to="not-found"/>
            </Switch>
          </Content>
        </Layout>
      </Layout>
    );
};
export default AdminLayout;