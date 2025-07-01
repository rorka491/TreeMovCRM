export function debounce<T extends (...args: any[]) => any>(
    f: T,
    cd: number
): (...p: Parameters<T>) => void {
    let id: NodeJS.Timeout | null = null

    if (cd <= 0) {
        return f
    }

    return (...args: any[]) => {
        console.log('debounce call', args)
        if (id !== null) {
            clearTimeout(id)
            id = null
        }

        id = setTimeout(() => f(...args), cd)
    }
}
