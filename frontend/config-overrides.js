const path = require("path");

module.exports = function override(config, env) {
    config.resolve.alias = {
        ...config.resolve.alias,
        "@": path.resolve(__dirname, "src"),
        "@utils": path.resolve(__dirname, "src/utils"),
        "@components": path.resolve(__dirname, "src/components"),
        "@pages": path.resolve(__dirname, "src/pages"),
        "@store": path.resolve(__dirname, "src/store"),
    };

    // Disable WebSocket connections in production build
    if (env === 'production') {
        config.devServer = {
            ...config.devServer,
            webSocketURL: 'auto://0.0.0.0:0/ws',
            client: {
                webSocketURL: 'auto://0.0.0.0:0/ws'
            }
        };
    }
    
    return config;
};
