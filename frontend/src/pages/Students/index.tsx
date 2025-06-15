import CategoryBar from "../../components/page/CategoryBar"
import { Outlet, useMatch } from "react-router-dom"

export function StudentsPage() {
	const match = useMatch("/:any/:lastPart/*")

	const activeSection = match?.params?.lastPart

    return (
		<section className="flex h-[100%] flex-col gap-y-5">
			{activeSection !== "profile" && <CategoryBar
				categories={[
					{ url: "main", label: "Основное" },
					{ url: "grades", label: "Оценки" },
					{ url: "payments", label: "Оплаты" },
				]}
				activeSection={activeSection}
			/>}

            <Outlet />
		</section>
	)
}