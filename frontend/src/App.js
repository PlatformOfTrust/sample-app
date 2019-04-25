import 'App.scss';

import React, {Component} from 'react';

import API from 'Utilities/API';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {};
        this.onLogin = this.onLogin.bind(this);
        this.onLogout = this.onLogout.bind(this);
    }

    async componentDidMount() {
        const { ok, data } = await API.me();
        if (ok) {
            this.setState({ user: data }, async () => {
                const { ok, data } = await API.getIdentity(this.state.user['@id']);
                if (ok) {
                    this.setState({ identity: data }, async () => {
                        const { ok, data } = await API.fetchDataProduct('prh-business-identity-data-product', { businessId: '2980005-2' });
                        if (ok) {
                            this.setState({ dataProduct: data });
                        }
                    });
                }
            });
        }
    }

    onLogin() {
        API.login();
    }

    async onLogout() {
        const { ok } = await API.logout();

        if (ok) {
            window.location.href = '/';
        }
    }

    render() {
        return (
            <div>
                {!this.state.user &&
                <button className="login-button" onClick={this.onLogin}>Log
                    in</button>
                }
                {this.state.user &&
                <div>
                    <button onClick={this.onLogout}>Logout</button>
                    <div className="request">
                        <h3>Auth API</h3>
                        <span>GET /me</span>
                        <pre
                            id="json">{JSON.stringify(this.state.user, undefined, 2)}</pre>
                    </div>

                    <div className="request">
                        <h3>Identities API</h3>
                        <span>GET /identities/{this.state.user['@id']}</span>
                        <pre
                            id="json">{JSON.stringify(this.state.identity, undefined, 2)}</pre>
                    </div>

                    <div className="request">
                        <h3>Broker API</h3>
                        <span>GET /fetch-data-product</span>
                        <pre
                            id="json">{JSON.stringify(this.state.dataProduct, undefined, 2)}</pre>
                    </div>
                </div>
                }
            </div>
        );
    }
}

export default App;
