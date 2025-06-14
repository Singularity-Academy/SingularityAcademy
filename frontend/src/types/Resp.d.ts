declare namespace Resp {
    interface Result<T = never> {
        code: number,
        message: string,
        data: T,
    }

    interface UserData {
        email: string
        id: number
        name: string
    }
}