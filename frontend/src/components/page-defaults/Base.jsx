import {
    Outlet,
} from 'react-router-dom'
import Sidebar from './Sidebar'
import PageHeader from './PageHeader'
import React, { useEffect, useState } from 'react'

export function Base() {
    const [isSidebarVisible, setIsSidebarVisible] = useState(true)

    return (
        <div className="flex h-screen">
            <Sidebar
                isVisible={isSidebarVisible}
                setIsVisible={setIsSidebarVisible}
            />
            <div className="flex-1 flex flex-col items-center justify-start px-10 py-4 h-screen overflow-y-auto">
                <div className="flex flex-col space-y-4 w-full h-[100%] max-w-[1800px]">
                    <PageHeader />

                    <div className="overflow-hidden mt-2 h-[100%]">
                        <Outlet />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Base
