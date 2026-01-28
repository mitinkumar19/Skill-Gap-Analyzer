import { Moon, Sun } from "lucide-react"
import { useTheme } from "./ThemeProvider"
import { motion } from "framer-motion"

export function ThemeToggle() {
    const { setTheme, theme } = useTheme()

    return (
        <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="relative p-2 rounded-full hover:bg-muted transition-colors focus:outline-none focus-ring"
            aria-label="Toggle theme"
        >
            <div className="relative w-5 h-5">
                <motion.div
                    initial={false}
                    animate={{
                        scale: theme === "dark" ? 0 : 1,
                        rotate: theme === "dark" ? 90 : 0,
                        opacity: theme === "dark" ? 0 : 1
                    }}
                    transition={{ duration: 0.2 }}
                    className="absolute inset-0 flex items-center justify-center text-foreground"
                >
                    <Sun className="h-5 w-5" />
                </motion.div>

                <motion.div
                    initial={false}
                    animate={{
                        scale: theme === "dark" ? 1 : 0,
                        rotate: theme === "dark" ? 0 : -90,
                        opacity: theme === "dark" ? 1 : 0
                    }}
                    transition={{ duration: 0.2 }}
                    className="absolute inset-0 flex items-center justify-center text-foreground"
                >
                    <Moon className="h-5 w-5" />
                </motion.div>
            </div>
            <span className="sr-only">Toggle theme</span>
        </button>
    )
}
