import { Outlet, Link, useLocation } from "react-router-dom"
import { motion } from "framer-motion"
import { Zap, Menu, X } from "lucide-react"
import { useState } from "react"
import { ThemeToggle } from "@/components/ThemeToggle"

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/app", label: "Analyze" },
  { href: "/about", label: "About Tech" },
]

export function Layout() {
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen flex flex-col bg-background bg-grid-pattern">
      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-border/50">
        <div className="container mx-auto px-4 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2 group">
              <div className="p-2 rounded-lg gradient-primary group-hover:scale-110 transition-transform">
                <Zap className="h-5 w-5 text-white" />
              </div>
              <span className="font-bold text-lg display-text">
                Skill Gap <span className="gradient-text">Analyzer</span>
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-6">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  to={link.href}
                  className={`relative text-sm font-medium transition-colors hover:text-primary ${location.pathname === link.href
                    ? "text-primary"
                    : "text-muted-foreground"
                    }`}
                >
                  {link.label}
                  {location.pathname === link.href && (
                    <motion.div
                      layoutId="navbar-indicator"
                      className="absolute -bottom-1 left-0 right-0 h-0.5 gradient-primary rounded-full"
                      initial={false}
                      transition={{ type: "spring", stiffness: 500, damping: 30 }}
                    />
                  )}
                </Link>
              ))}
            </nav>

            <div className="flex items-center gap-4">
              <ThemeToggle />

              {/* CTA Button */}
              <div className="hidden md:block">
                <Link
                  to="/app"
                  className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white rounded-lg gradient-primary btn-glow transition-all hover:opacity-90"
                >
                  Analyze Resume
                </Link>
              </div>

              {/* Mobile Menu Button */}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2 rounded-lg hover:bg-muted"
              >
                {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </button>
            </div>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden py-4 border-t border-border"
            >
              <nav className="flex flex-col gap-2">
                {navLinks.map((link) => (
                  <Link
                    key={link.href}
                    to={link.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${location.pathname === link.href
                      ? "bg-primary/10 text-primary"
                      : "hover:bg-muted text-muted-foreground"
                      }`}
                  >
                    {link.label}
                  </Link>
                ))}
                <Link
                  to="/app"
                  onClick={() => setMobileMenuOpen(false)}
                  className="mt-2 mx-4 text-center py-2 text-sm font-medium text-white rounded-lg gradient-primary"
                >
                  Analyze Resume
                </Link>
              </nav>
            </motion.div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card/50">
        <div className="container mx-auto px-4 lg:px-8 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            {/* Brand */}
            <div className="md:col-span-2">
              <Link to="/" className="flex items-center gap-2 mb-4">
                <div className="p-2 rounded-lg gradient-primary">
                  <Zap className="h-5 w-5 text-white" />
                </div>
                <span className="font-bold text-lg">Skill Gap Analyzer</span>
              </Link>
              <p className="text-muted-foreground text-sm max-w-md">
                AI-powered resume analysis with zero hallucinations. Get personalized
                learning roadmaps to bridge your skill gaps and land your dream job.
              </p>
              <div className="flex gap-2 mt-4">
                <span className="text-xs text-muted-foreground">🔒 Privacy-First</span>
                <span className="text-xs text-muted-foreground">•</span>
                <span className="text-xs text-muted-foreground">🚀 Instant Results</span>
                <span className="text-xs text-muted-foreground">•</span>
                <span className="text-xs text-muted-foreground">✨ Zero Cost</span>
              </div>
            </div>

            {/* Links */}
            <div>
              <h4 className="font-semibold mb-4 text-sm">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link to="/app" className="hover:text-primary transition-colors">Analyze Resume</Link></li>
                <li><Link to="/about" className="hover:text-primary transition-colors">About the Tech</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4 text-sm">Resources</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="https://github.com" target="_blank" rel="noopener" className="hover:text-primary transition-colors">GitHub</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Documentation</a></li>
              </ul>
            </div>
          </div>

          <div className="mt-12 pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-muted-foreground">
              © 2025 Skill Gap Analyzer. Built for Google Hackathon 2025.
            </p>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-primary/10 to-secondary/10 border border-primary/20">
              <span className="text-xs font-medium gradient-text">🏆 Hackathon Project</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
