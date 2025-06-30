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
    const selfRef = useRef<HTMLDivElement>(null)
    const [pos, setPos] = useState({ x: 0, y: 0 })

    useEffect(() => {
        function handleClickOutside(e: MouseEvent) {
            if (
                selfRef.current &&
                !selfRef.current.parentNode?.contains(e.target as Node)
            ) {
                setOpen?.(false)

                if (open) {
                    onClose?.()
                }
            }
        }

        document.addEventListener('click', handleClickOutside)
        window.addEventListener('resize', reposition)
        return () => {
            document.removeEventListener('click', handleClickOutside)
            window.removeEventListener('resize', reposition)
        }
    }, [])

    function reposition() {
        const parent = selfRef.current?.parentElement as HTMLElement

        if (!parent || !selfRef.current) {
            return
        }

        const selfRect = selfRef.current!.getBoundingClientRect()
        const parentRect = parent.getBoundingClientRect()

        if (window.innerHeight - parentRect.bottom > 100) {
            selfRef.current.style.maxHeight = `${window.innerHeight - parentRect.bottom}px`
        }

        selfRect.x = parentRect.left
        selfRect.y = parentRect.bottom

        if (selfRect.height > window.innerHeight - parentRect.bottom) {
            selfRect.x += 20
        }

        selfRect.x = Math.min(
            selfRect.x,
            window.innerWidth - selfRect.width - 1
        )

        if (window.innerHeight - parentRect.bottom <= 100) {
            selfRect.y = Math.min(
                selfRect.y,
                window.innerHeight - selfRect.height - 1
            )
        }

        setPos({
            x: selfRect.x,
            y: selfRect.y,
        })
    }

    useLayoutEffect(reposition, [selfRef, open])

    return (
        <>
            {open && (
                <div
                    ref={selfRef}
                    className={
                        className +
                        ` absolute z-10 max-h-[90vh] overflow-y-auto special-scroll`
                    }
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
