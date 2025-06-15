export function parseDate(date: string /* DD.MM.YYYY */) {
    const parts = date.split(/[/.-]/)

    return new Date(
        parseInt(parts[2], 10),
        parseInt(parts[1], 10) - 1,
        parseInt(parts[0], 10)
    )
}
