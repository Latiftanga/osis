import http from './httpService';
import { API_URL } from '../config.json';

const endpoint = `${API_URL}staff/`;

const getStaffList = () => http.get(endpoint);

const getStaff = id => http.get(`${endpoint}${id}/`);

const saveStaff = staff => {
    if (staff.id) {
        const body = {...staff};
        delete body.id;
        return http.put(`${endpoint}${staff.id}/`, body);
    }
    return http.post(endpoint, staff);
};

const deleteStaff = id => http.delete(`${endpoint}${id}`);

export {
    getStaff,
    getStaffList,
    saveStaff,
    deleteStaff
};