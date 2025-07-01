type StatisticsCardProps = {
    title: string
    value: number
    percentChange: number
    prevValue: number
    color?: string
}
function StatisticsCard({
    title,
    value,
    percentChange,
    prevValue,
    color = 'black',
}: StatisticsCardProps) {
    const percentSign = percentChange > 0 ? '+' : ''
    return (
        <li className="grid min-w-[188px] gap-y-[6px] p-[16px] bg-white rounded-[12.5px]">
            <div className="flex gap-[4px]">
                <span
                    className="w-[16px] h-[16px] rounded-full"
                    style={{ background: color }}
                />
                <span className="text-[14px] font-bold">{title}</span>
            </div>
            <span className="text-[16px]">{value}</span>
            <div className="grid">
                <span className="text-[11px] text-[#616161]">
                    {percentSign}
                    {percentChange}% за месяц
                </span>
                <span className="text-[11px] text-[#616161]">
                    ({prevValue} в прошлом месяце)
                </span>
            </div>
        </li>
    )
}

export default StatisticsCard
