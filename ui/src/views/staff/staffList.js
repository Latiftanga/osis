import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { Button, Table, notification } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import {getStaffList, deleteStaff } from '../../services/staffService'

const StaffList = () => {

  const [data, setData] = useState([]);
  const history = useHistory();

  const handleDelete = async (record) => {
    const originalData = data;
    const newData = data.filter(staff => staff.id !== record.id);
    setData(newData);
    deleteStaff(record.id)
      .catch((ex) => {
        const { response } = ex;
        if (response && response.status >=400 && response.status<500 )
          notification['info']({
            message: `${response.data.detail}`,
          })
        setData(originalData);
      });
  }

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => <Link to={'/staff/' + record.id} >{text}</Link>
    },
    {
      title: 'Phone',
      dataIndex: 'phone',
      key: 'phone',
    },
    {
      title: 'Address',
      dataIndex: 'address',
      key: 'address',
    },
    {
      title: 'Action',
      key: 'action',
      render: (text, record) => (
        <Button type="link"
        danger size="small"
        shape="circle"
        onClick={() => handleDelete(record)}
        >
          <DeleteOutlined />
        </Button>
      )
  
    },
  ];  
  

  const addNew = () => history.push('/staff/new');

  useEffect(() => {
    const fetchData = async () => {
      const { data } = await getStaffList();
      setData(data);
    };
    fetchData();
  }, []);

  return (
    <>
      <Button type="primary" onClick={addNew} >+ Add New</Button>
      <Table dataSource={data} columns={columns} rowKey="id" />
    </>
  )
};

export default StaffList;