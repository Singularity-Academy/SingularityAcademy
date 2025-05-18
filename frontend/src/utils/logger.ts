/**
 * Frontend logging utility
 */

const LOG_LEVELS = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3
};

interface Logger {
    debug: (message: string, data?: any) => void;
    info: (message: string, data?: any) => void;
    warn: (message: string, data?: any) => void;
    error: (message: string, data?: any) => void;
}

const CURRENT_LOG_LEVEL = LOG_LEVELS.DEBUG;  // Set to DEBUG for development

const formatMessage = (level: string, message: string, data?: any): string => {
    const timestamp = new Date().toISOString();
    const dataStr = data ? ` ${JSON.stringify(data)}` : '';
    return `[${timestamp}] ${level}: ${message}${dataStr}`;
};

export const logger: Logger = {
    debug: (message: string, data?: any) => {
        if (CURRENT_LOG_LEVEL <= LOG_LEVELS.DEBUG) {
            console.debug(formatMessage('DEBUG', message, data));
        }
    },
    
    info: (message: string, data?: any) => {
        if (CURRENT_LOG_LEVEL <= LOG_LEVELS.INFO) {
            console.info(formatMessage('INFO', message, data));
        }
    },
    
    warn: (message: string, data?: any) => {
        if (CURRENT_LOG_LEVEL <= LOG_LEVELS.WARN) {
            console.warn(formatMessage('WARN', message, data));
        }
    },
    
    error: (message: string, data?: any) => {
        if (CURRENT_LOG_LEVEL <= LOG_LEVELS.ERROR) {
            console.error(formatMessage('ERROR', message, data));
        }
    }
};

export default logger; 