const path = require("path");

module.exports = function override(config) {
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
