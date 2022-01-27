const {createClient} = require('redis')

class Repo {
  constructor(redisUrl) {
    if (redisUrl) {
      this.client = createClient(redisUrl)
    } else {
      this.client = createClient()
    }
    this.client.on('error', (err) => console.log('Redis Client Error', err))
  }

  connect() {
    return this.client.connect()
  }

  getRecord() {
    return this.client.get('record')
  }

  setRecord(record) {
    return this.client.set('record', record)
  }

  async getFroggers() {
    const froggers = await this.client.hGetAll('froggers')
    return Object.keys(froggers)
      .reduce((obj, id) =>
        (obj[id] = JSON.parse(froggers[id]), obj),
        {}
      )
  }

  newFrogger(id, username, frogsCount) {
    return this.client.hSet('froggers', id, JSON.stringify({
      username,
      frogsCount,
    }))
  }

  async incrementFrogsCount(id) {
    const f = JSON.parse(await this.client.hGet('froggers', String(id)))
    f.frogsCount++
    return await this.client.hSet('froggers', String(id), JSON.stringify(f))
  }

  async drop() {
    await this.client.flushAll()
  }
}

module.exports = Repo

// const repo = new Repo()
//
// repo.connect().then(async () => {
//   await repo.incrementFrogsCount(123)
//   await repo.incrementFrogsCount(123)
//   await repo.incrementFrogsCount(123)
//   await repo.incrementFrogsCount(123)
//   await repo.incrementFrogsCount(123)
//   await repo.incrementFrogsCount(123)
//   console.log(await repo.getFroggers())
// })
