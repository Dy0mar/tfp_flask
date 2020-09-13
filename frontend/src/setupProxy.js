const { createProxyMiddleware } = require('http-proxy-middleware');
module.exports = function(app) {
    const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000/'
    app.use(createProxyMiddleware('/api',
        { target: API_URL }
    ));
}
