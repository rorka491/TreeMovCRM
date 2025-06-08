const stats = [
	{
		title: "Всего групп",
		count: 21,
		change: {
			value: "+10%",
			period: "за месяц",
			previousValue: 10,
		},
		color: "#007AFF",
	},
	{
		title: "Всего учеников",
		count: 520,
		change: {
			value: "+20%",
			period: "за месяц",
			previousValue: 400,
		},
		color: "#63CFE5",
	},
	{
		title: "Клиентов в обработке",
		count: 1201,
		change: {
			value: "5",
			period: "ожидаемых оплат",
		},
		color: "#FFA8A1",
	},
	{
		title: "Всего сотрудников",
		count: 601,
		change: {
			value: "5",
			period: "стажеров",
		},
		color: "#FFA8A1",
	},
]

function StatsCards() {
	return (
		<div className="grid grid-cols-4 gap-4">
			{stats.map((stat, index) => (
				<div key={index} className="p-4 bg-white grid grid-rows-[repeat(3,min-content)] gap-y-1.5 rounded-[12.5px]">
					<div className="grid grid-cols-[min-content_1fr] h-min gap-x-1">
						<div className={`w-full aspect-square rounded-full bg-[${stat.color}]`} />
						<h4 className="text-xs font-semibold">{stat.title}</h4>
					</div>
					<p className="text-sm">{stat.count}</p>
					<div className="grid text-xs text-gray-500">
						<p>{stat.change.value && `${stat.change.value} ${stat.change.period}`}</p>
						<p>{stat.change.previousValue && `(${stat.change.previousValue} в прошлом месяце)`}</p>
					</div>
				</div>
			))}
		</div>
	)
}

export default StatsCards
