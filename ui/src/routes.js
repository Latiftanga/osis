import {
    DashboardOutlined,
    UnorderedListOutlined
} from '@ant-design/icons';
import StaffList from './views/staff/staffList';
import Dashboard from './views/dashboard';
import StaffDetails from './views/staff/staffDetails';
import NotFound from './views/notFound';
import StaffForm from './views/staff/staffForm';
import Login from './views/auth/login';

const routes = [
    {
        key: 0,
        path: '/auth-token',
        content: <Login/>,
        display: false
    },
    {
        key: 1,
        path: '/',
        displayName: 'Dashboard',
        icon: <DashboardOutlined/>,
        exact: true,
        content: <Dashboard/>,
        display: true
    },
    {
        key: 2,
        path: '/staff/new/',
        exact: true,
        content: <StaffForm/>,
        display: false
    },
    {
        key: 3,
        path: '/staff/:id/edit',
        content: <StaffForm/>,
        display: false
    },
    {
        key: 4,
        path: '/staff/:id/',
        exact: true,
        content: <StaffDetails/>,
        display: false
    },
  
    {
        key: 5,
        path: '/staff/',
        displayName: 'Staff',
        icon: <UnorderedListOutlined/>,
        exact: true,
        content: <StaffList/>,
        display: true
    },
    {
        key: 6,
        path: '/not-found',
        content: <NotFound/>,
        display: false
    },

];
export default routes;
