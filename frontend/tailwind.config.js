module.exports = {
  purge: {
    enabled: process.env.NODE_ENV !== 'development',
    content: ['./src/**/*.{js,ts,jsx,tsx}']
  },
  theme: {
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem',
      '6xl': '4rem',
      '7xl': '5.3rem',
      '8xl': '6rem'
    },
    extend: {
      colors: {
        primary: {
          100: '#EFEDFD',
          200: '#D8D1FA',
          300: '#C0B5F7',
          400: '#00BCBC',
          500: '#009191',
          600: '#008181',
          700: '#32C8CD',
          800: '#2C2069',
          900: '#1D1546'
        },
        secondary: {
          300: '#FFF6DC',
          500: '#FBCB67',
          600: '#F59E0B'
        },
        gray: {
          100: '#F0F0F0',
          200: '#EBEBEB',
          300: '#e2e8f0',
          400: '#cbd5e0',
          500: '#BDBDBD',
          600: '#666666',
          700: '#4a5568',
          800: '#313358',
          900: '#1a202c'
        },
        green: {
          100: '#f0fff4',
          200: '#c6f6d5',
          300: '#9ae6b4',
          400: '#68d391',
          500: '#48bb78',
          600: '#38a169',
          700: '#2f855a',
          800: '#276749',
          900: '#22543d'
        },
        amber: {
          500: '#FBCB67',
          600: '#EEAA3D'
        },
        red: {
          300: '#F29C9F',
          400: '#EC6161',
          500: '#EB6161'
        },
        blue: {
          500: '#4DADF7'
        },
        whitesmoke: {
          500: '#F9F5F1'
        }
      },
      lineHeight: {
        hero: '3.7rem'
      },
      opacity: {
        10: '.1'
      },
      zIndex: {
        '-10': '-10'
      }
    }
  },
  variants: {
    margin: ['responsive', 'first'],
    display: ['group-hover']
  },
  plugins: []
}
