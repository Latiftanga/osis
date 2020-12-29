import axios from 'axios';
import { notification } from 'antd';

axios.interceptors.response.use(null, error => {
  const { response } = error;
  if (!response && response.status >=400 && response.status <500) {
    console.log('Logging the error: ', error);
    notification['error']({
      message: 'An unexpected error occured',
    })
  }
  return Promise.reject(error);
});

const setJwt = jwt => axios.defaults.headers.common['Authorization'] = `JWT ${jwt}`;

const http = {
  get: axios.get,
  post: axios.post,
  put: axios.put,
  delete: axios.delete,
  setJwt: setJwt
}

export default http;