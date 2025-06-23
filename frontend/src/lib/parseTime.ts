export function parseTime(time: string) {
    const [h, m] = time.split(':').map(Number)
    return h + m / 60
}
