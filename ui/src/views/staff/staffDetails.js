import React, { useState, useEffect} from 'react';
import { useParams } from 'react-router-dom';
import { Card, Descriptions, Divider, Menu, Dropdown, Button } from 'antd';
import { EllipsisOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import axios from 'axios';

const StaffDetails = () => {
    const [data, setData] = useState([]);
    const { id } = useParams();

    const staffOperations = (
        <Menu>
            <Menu.Item>
                <Link to={{pathname:`/staff/${id}/edit`, state: data}}>Edit Personal Info</Link> 
            </Menu.Item>
        </Menu>
    );

    const fetchData = async (param_id) => {
        const { data } = await axios.get(`http://127.0.0.1:8000/api/staff/${param_id}`);
        setData(data);
    };

    useEffect(() => {
        fetchData(id);
    }, [id]);
    // const location = useLocation();
    
    return (
        <Card
        >
          <Descriptions
            title="Personal Information"
            extra={
                <Dropdown overlay={staffOperations} >
                    <Button type="ghost" shape="circle" icon={<EllipsisOutlined />} />
                </Dropdown>
            }
          >
            <Descriptions.Item label="First Name">{data.first_name}</Descriptions.Item>
            <Descriptions.Item label="Last Name">{data.last_name}</Descriptions.Item>
            <Descriptions.Item label="Other Names">{data.middle_name}</Descriptions.Item>
            <Descriptions.Item label="Sex">{data.sex}</Descriptions.Item>
            <Descriptions.Item label="Date of Birth">{data.date_of_birth}</Descriptions.Item>
            <Descriptions.Item label="Address">{data.address}</Descriptions.Item>
            <Descriptions.Item label="Mobile"> {data.phone} </Descriptions.Item>
            <Descriptions.Item label="Email"> {data.email} </Descriptions.Item>
            <Descriptions.Item label="SSSNIT No"> {data.sssnit_no} </Descriptions.Item>
        </Descriptions>
        <Divider />
        
        <Descriptions title="Account Information">
            {
                data.account ? (
                    <Descriptions.Item label="Account">available</Descriptions.Item>
                ) : (
                    <Descriptions.Item label="Account">Not available</Descriptions.Item>
                )
            }
        </Descriptions>

        <Divider />

        <Descriptions title="Appointment Information">
        </Descriptions>
        <Divider />
        <Descriptions title="Certificates/Qualifications">
        </Descriptions>
        <Divider />
        <Descriptions title="Promotions">
        </Descriptions>
        </Card>
    )
};

export default StaffDetails;