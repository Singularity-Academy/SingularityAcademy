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
    
    return config;
};

module.exports.devServer = function(configFunction) {
    return function(proxy, allowedHost) {
        const config = configFunction(proxy, allowedHost);
        
        // Disable WebSocket in containerized environment
        config.webSocketURL = false;
        config.client = {
            ...config.client,
            webSocketURL: false
        };
        
        return config;
    };
};
