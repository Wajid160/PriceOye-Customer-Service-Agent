/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/priceoye/templates/**/*.{html,js}'],
    theme: {
        extend: {
            fontFamily: {
                poppins: ['Poppins', 'sans-serif'],
            },
            colors: {
                'priceoye-blue': '#007BFF',
                'priceoye-gray': '#6B7280',
            },
        },
    },
    plugins: [],
}