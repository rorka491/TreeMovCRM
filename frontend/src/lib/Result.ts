export type Result<T = any, E = string> = [Exclude<T, null>, null] | [null, Exclude<E, null>]

export function mapResult<T, E, R = void>(
    result: Result<T, E>,
    good: (val: Exclude<T, null>) => R,
    errorF: (err: Exclude<E, null>) => R
): R
export function mapResult<T, E, R = void>(
    result: Result<T, E>,
    good: (val: Exclude<T, null>) => R,
    errorF?: undefined
): E
export function mapResult<T, E, R = void>(
    result: Result<T, E>,
    good: (val: Exclude<T, null>) => R,
    errorF?: (err: Exclude<E, null>) => R
): E | R {
    const [val, error] = result

    if (error === null) {
        // @ts-ignore
        return good(val)
    }

    if (errorF) {
        return errorF(error)
    }

    return error
}
