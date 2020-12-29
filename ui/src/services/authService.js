import http from './httpService';
import { API_URL } from '../config.json';
import jwt_decode from 'jwt-decode';

const endpoint = `${API_URL}auth-token/`;

export async function login(credentials) {
    const { data } = await http.post(endpoint, credentials);
    localStorage.setItem('token', data.token);
};

export function getToken()  { return localStorage.getItem('token') };

http.setJwt(localStorage.getItem('token'));

export function loginWithJwt(jwt) { localStorage.setItem('token', jwt) };

export function getUser() {
    try {
        return jwt_decode(localStorage.getItem('token'));
    } catch (error) {
        return null;
    }
};

export function logOut() { localStorage.removeItem('token') };

const auth = { login, loginWithJwt, getUser, logOut, getToken };

export default auth;