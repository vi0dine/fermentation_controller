import axios from "axios"

export const setupAxios = () => {
    axios.defaults.baseURL = "http://192.168.2.60:4001/api"
    axios.defaults.headers.post["Content-Type"] = "application/json"
    axios.interceptors.request.use(
        function (config) {
            // @ts-ignore
            const username = "test"
            const password = "test"
            config.headers["Authorization"] = `Basic ${btoa(username + ":" + password)}`
            return config
        },
        function (err) {
            return Promise.reject(err)
        }
    )
}
