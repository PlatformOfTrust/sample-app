import config from 'config';

class API {
    baseUrl = '';

    constructor() {
        this.baseUrl = config.appBackend;
    }

    static async ResponseHandler(response) {
        try {
            return { ok: response.ok, data: await response.json() };
        } catch (error) {
            return {
                ok: false,
                data: { message: 'Cannot process response', error }
            };
        }
    }

    // Authorization API
    async login() {
        return fetch(`${this.baseUrl}/login`).then(await API.ResponseHandler);
    }

    async logout() {
        return fetch(`${this.baseUrl}/logout`).then(await API.ResponseHandler);
    }

    async me() {
        return fetch(`${this.baseUrl}/me`).then(await API.ResponseHandler);
    }

    // Identity API
    async getIdentity(id) {
        return fetch(`${this.baseUrl}/identities/${id}`).then(await API.ResponseHandler);
    }

    // Broker API
    async fetchDataProduct(productCode, parameters) {
        return fetch(`${this.baseUrl}/fetch-data-product`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                productCode,
                parameters
            })
        }).then(await API.ResponseHandler);
    }
}

const instance = new API();

export default instance;
