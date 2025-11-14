'use client'

import Link from 'next/link'
import { Github, Linkedin, Twitter, Instagram, Code, Shield, TrendingUp } from 'lucide-react'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="flex flex-col items-center justify-center text-center">
          <h1 className="text-6xl font-bold text-white mb-4 animate-fade-in">
            Hey 👋 What's up?
          </h1>

          <div className="text-4xl font-mono text-primary-500 mb-8 animate-slide-up">
            Hi, I'm <span className="font-bold">Wallax</span>
          </div>

          <p className="text-xl text-gray-300 max-w-2xl mb-12 animate-fade-in">
            Full-Stack Developer | Ethical Hacker | Growth Hacker
          </p>

          {/* Social Links */}
          <div className="flex gap-6 mb-16 animate-slide-up">
            <a
              href="https://github.com/WallCod"
              target="_blank"
              rel="noopener noreferrer"
              className="p-4 bg-dark-700 hover:bg-dark-600 rounded-lg transition-colors"
            >
              <Github className="w-6 h-6 text-white" />
            </a>
            <a
              href="https://www.linkedin.com/in/wallax-figueiredo-41116b285/"
              target="_blank"
              rel="noopener noreferrer"
              className="p-4 bg-dark-700 hover:bg-dark-600 rounded-lg transition-colors"
            >
              <Linkedin className="w-6 h-6 text-white" />
            </a>
            <a
              href="https://x.com/black14691"
              target="_blank"
              rel="noopener noreferrer"
              className="p-4 bg-dark-700 hover:bg-dark-600 rounded-lg transition-colors"
            >
              <Twitter className="w-6 h-6 text-white" />
            </a>
            <a
              href="https://www.instagram.com/wallaxsf"
              target="_blank"
              rel="noopener noreferrer"
              className="p-4 bg-dark-700 hover:bg-dark-600 rounded-lg transition-colors"
            >
              <Instagram className="w-6 h-6 text-white" />
            </a>
          </div>

          {/* About */}
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mb-16">
            <div className="bg-dark-800 p-8 rounded-lg border border-primary-500/20 hover:border-primary-500/50 transition-colors">
              <Code className="w-12 h-12 text-primary-500 mb-4 mx-auto" />
              <h3 className="text-xl font-bold text-white mb-2">Full-Stack Developer</h3>
              <p className="text-gray-400">
                Expert in Next.js, Node.js, Python, and modern web technologies
              </p>
            </div>

            <div className="bg-dark-800 p-8 rounded-lg border border-primary-500/20 hover:border-primary-500/50 transition-colors">
              <Shield className="w-12 h-12 text-primary-500 mb-4 mx-auto" />
              <h3 className="text-xl font-bold text-white mb-2">Ethical Hacker</h3>
              <p className="text-gray-400">
                NetSec Engineer specialized in penetration testing and security
              </p>
            </div>

            <div className="bg-dark-800 p-8 rounded-lg border border-primary-500/20 hover:border-primary-500/50 transition-colors">
              <TrendingUp className="w-12 h-12 text-primary-500 mb-4 mx-auto" />
              <h3 className="text-xl font-bold text-white mb-2">Growth Hacker</h3>
              <p className="text-gray-400">
                CEO & Founder of AlphaLabs - www.alphalabs.lat
              </p>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex gap-4 flex-wrap justify-center">
            <Link
              href="/dashboard"
              className="btn btn-primary px-8 py-3 text-lg"
            >
              View Dashboard
            </Link>
            <Link
              href="/docs"
              className="btn btn-outline px-8 py-3 text-lg text-white"
            >
              API Documentation
            </Link>
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section className="container mx-auto px-4 py-20 bg-dark-800/50">
        <h2 className="text-4xl font-bold text-center text-white mb-12">My Skills</h2>

        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-primary-500 mb-4">Main Technologies</h3>
            <div className="flex flex-wrap gap-3">
              {['Vite', 'Next.js', 'Node.js', 'TailwindCSS', 'Bootstrap', 'GitHub Actions', 'PHP', 'Python'].map((skill) => (
                <span
                  key={skill}
                  className="px-4 py-2 bg-dark-700 text-white rounded-lg border border-primary-500/30 hover:border-primary-500 transition-colors"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div className="mb-8">
            <h3 className="text-2xl font-bold text-primary-500 mb-4">Databases</h3>
            <div className="flex flex-wrap gap-3">
              {['MySQL', 'Supabase', 'PostgreSQL', 'MongoDB'].map((skill) => (
                <span
                  key={skill}
                  className="px-4 py-2 bg-dark-700 text-white rounded-lg border border-primary-500/30 hover:border-primary-500 transition-colors"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-2xl font-bold text-primary-500 mb-4">Tools</h3>
            <div className="flex flex-wrap gap-3">
              {['VSCode', 'Figma', 'Postman', 'Kali Linux', 'Nmap', 'Wireshark', 'Hydra'].map((skill) => (
                <span
                  key={skill}
                  className="px-4 py-2 bg-dark-700 text-white rounded-lg border border-primary-500/30 hover:border-primary-500 transition-colors"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 text-center text-gray-400">
        <p>God 🙏 | Lyon 🦁 | CEO & Founder - AlphaLabs 🦁</p>
        <p className="mt-2">UNIFATECIE - Computer Engineer 📚 | AWARI - Full-Stack Developer | SQL | Python 📚</p>
      </footer>
    </main>
  )
}
