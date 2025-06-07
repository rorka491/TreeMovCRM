const kpi = [
    {
        id: 1,
        title: 'Основные показатели KPI',
        metrics: [
            { name: 'Часы', value: '...' },
            { name: 'Эффективность', value: '...' },
            { name: 'Выполнение плана', value: '...' },
            { name: 'Качество работы', value: '...' },
            { name: 'Дисциплина', value: '...' },
        ],
    },
]

function KPICard() {
    return (
        <div className="p-2.5 bg-white rounded-[12.5px] text-xs">
            {kpi.map((section) => (
                <div key={section.id}>
                    <h3 className="mb-4 text-lg font-medium text-gray-900">
                        {section.title}
                    </h3>

                    <div className="grid gap-y-2.5">
                        {section.metrics.map((metric, index) => (
                            <div
                                key={index}
                                className="grid grid-cols-[max-content_1fr] justify-between w-full gap-x-5"
                            >
                                <span className="text-sm text-gray-600">
                                    {metric.name}
                                </span>
                                <div className="h-full bg-gray-100 rounded-full"></div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    )
}

export default KPICard
