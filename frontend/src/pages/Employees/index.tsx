import CategoryBar from "../../components/page/CategoryBar"
import { Outlet, useMatch } from "react-router-dom"

function EmpoloyeesPage() {
	const match = useMatch("/:any/:lastPart")

	const activeSection = match?.params?.lastPart

	return (
		<section className="flex flex-col gap-y-5">
			<CategoryBar
				categories={[
					{ url: "main", label: "Основное" },
					{ url: "vacation", label: "Отпуска" },
					{ url: "analytics", label: "Аналитика" },
					{ url: "archive", label: "Архив" },
				]}
				activeSection={activeSection}
				searchPlaceholder={"Найти в сотрудниках..."}
			/>

            <Outlet />
		</section>
	)
}

export default EmpoloyeesPage
