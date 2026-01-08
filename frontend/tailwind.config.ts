import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        base: {
          50: '#F7FAFC',
          100: '#EEF3F8',
          200: '#E3ECF6',
          300: '#D4E2F0',
          400: '#C6D8EC'
        },
        accent: {
          blue: '#CDE4FF',
          green: '#D6F2D6',
          cream: '#FFF5E6',
          purple: '#E9D7FF'
        }
      },
      borderRadius: {
        xl: '1rem'
      },
      boxShadow: {
        soft: '0 8px 20px rgba(148, 163, 184, 0.15)'
      }
    }
  },
  plugins: []
}

export default config
