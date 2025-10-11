module.exports = {
  plugins: [
    require('postcss-import-extens', {
      stages: ['extend-tailwindcss']
    }),
    require('tailwindcss'),
    require('postcss-nest', { strict: true })
  ]
};