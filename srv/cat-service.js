const cds = require('@sap/cds')

module.exports = class CatalogService extends cds.ApplicationService {
  async init() {
    const { Books, Reviews } = this.entities

    // Validate review ratings before creating a review
    this.before('CREATE', Reviews, (req) => {
      const { rating } = req.data

      if (
        !Number.isInteger(rating) ||
        rating < 1 ||
        rating > 5
      ) {
        req.reject(400, 'Rating must be an integer between 1 and 5')
      }
    })

    // Discount label on well-stocked books
    this.after('each', Books, book => {
      if (book.stock > 100) book.title += ' -- 11% off!'
    })

    // Existing order functionality
    this.on('submitOrder', async req => {
      const { book, quantity } = req.data
      const n = await UPDATE(Books, book)
        .with`stock = stock - ${quantity}`
        .where`stock >= ${quantity}`

      if (!n) {
        return req.error(409, `${quantity} exceeds stock for book #${book}`)
      }
    })

    return super.init()
  }
}