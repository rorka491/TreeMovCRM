import React, { useRef, useEffect, useState, useLayoutEffect } from 'react'

export function PopUpMenu({
    open,
    setOpen,
    onClose,
    children,
    className,
}: React.PropsWithChildren<{
    open?: boolean
    setOpen?: React.Dispatch<React.SetStateAction<boolean>>
    onClose?: () => void
    className?: string
}>) {
    const ref = useRef<HTMLDivElement>(null)
    const [pos, setPos] = useState({ x: 0, y: 0 })

    useEffect(() => {
        function handleClickOutside(e: MouseEvent) {
            if (
                ref.current &&
                !ref.current.parentNode?.contains(e.target as Node)
            ) {
                setOpen?.(false)

                if (open) {
                    onClose?.()
                }
            }
        }

        document.addEventListener('click', handleClickOutside)
        return () => document.removeEventListener('click', handleClickOutside)
    }, [open])

    useLayoutEffect(() => {
        const parent = ref.current?.parentElement as HTMLElement

        if (!parent) {
            return
        }

        const selfRect = ref.current!.getBoundingClientRect()
        const parentRect = parent.getBoundingClientRect()

        selfRect.x = parentRect.left
        selfRect.y = parentRect.bottom

        const selfPosX = Math.min(
            selfRect.x,
            window.innerWidth - selfRect.width - 1
        )
        const selfPosY = Math.min(
            selfRect.y,
            window.innerHeight - selfRect.height - 1
        )

        setPos({
            x: selfPosX,
            y: selfPosY,
        })
    }, [ref, open])

    return (
        <>
            {open && (
                <div
                    ref={ref}
                    className={className + ` absolute z-10`}
                    style={{
                        top: pos.y,
                        left: pos.x,
                    }}
                >
                    {children}
                </div>
            )}
        </>
    )
}
