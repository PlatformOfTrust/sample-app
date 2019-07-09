import 'index.scss';

import React from 'react';
import ReactDOM from 'react-dom';
import App from 'App';

import * as serviceWorker from 'serviceWorker';

const root = document.getElementById('root');

if (root) {
    const rootEl = (
        <App/>
    );

    ReactDOM.render(rootEl, root);

    // If you want your app to work offline and load faster, you can change
    // unregister() to register() below. Note this comes with some pitfalls.
    // Learn more about service workers: http://bit.ly/CRA-PWA
    serviceWorker.unregister();
} else {
    console.error('Root is not HTML element', root);
}
