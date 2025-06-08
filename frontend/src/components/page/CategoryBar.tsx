import { Link } from "react-router-dom"

function CategoryBar({ activeSection, categories, search, searchPlaceholder, searchButtonLabel, onSearch, onSearchInputChange }) {
	const searchActive = search || searchPlaceholder || onSearch || onSearchInputChange

	return (
		<div className="flex text-[16px] items-center justify-between border-b border-t border-gray-300">
			<ul className="flex space-x-5">
				{categories.map(({ url, label }) => (
					<li key={url} className={`px-3 py-[10px] cursor-pointer border-b-2 ${activeSection === url || activeSection === label ? "border-[#7816db]" : "border-transparent hover:border-[#7816db]"}`}>
						<Link to={url}>{label}</Link>
					</li>
				))}
			</ul>
			{searchActive && (
				<form className="flex h-[100%] items-center gap-2.5 px-3 py-[5px] bg-white rounded-[12.5px]">
					<input placeholder={searchPlaceholder ?? "Введите"} />
					<button>
						<svg width="26" height="26" viewBox="5 5 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M9.81288 15.1365L11.8948 13.0546L9.82842 10.9881L10.6985 10.1181L12.7649 12.1845L14.8313 10.1181L15.7118 10.9985L13.6453 13.0649L15.7118 15.1313L14.8417 16.0014L12.7753 13.935L10.6933 16.0169L9.81288 15.1365Z" fill="#616161" />
						</svg>
					</button>
					<input className="rounded-[12.5px] border px-[14.5px] py-[5px] text-[#616161] hover:bg-gray-200 duration-100" type="submit" value={searchButtonLabel ?? "Поиск"} />
				</form>
			)}
		</div>
	)
}

export default CategoryBar
