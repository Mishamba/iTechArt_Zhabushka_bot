const {Telegraf} = require('telegraf')
const config = require('./config')
const Repo = require('./repo')

const bot = new Telegraf(config.telegram.token, {})

const frogStickers = ['AgADIQADD27HLw', 'AgADIgADD27HLw']

// let record = 0
// const froggers = {}
let combo = 0

const repo = new Repo()
repo.connect()

function randomIntFromInterval(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min)
}

const comboBreaker = async (ctx, doReply=true) => {
  const record = await repo.getRecord()
  if (combo > 0) {
    doReply && ctx.reply(`FROG COMBO: ${combo}🐸`)
    if (combo > record) {
      await repo.setRecord(combo)
      doReply && ctx.reply(`NEW RECORD: ${combo}`)
    }
    combo = 0
  }
}

bot.command('how_much_is_the_frog', async (ctx) => {
  await comboBreaker(ctx)
  const froggers = await repo.getFroggers()
  const total = Object.values(froggers).reduce((total, f) => total + f.frogsCount, 0)
  ctx.reply(`${total}🐸 WERE SENT!!!`)
})

bot.command('my_frogs', async (ctx) => {
  await comboBreaker(ctx)
  const froggers = await repo.getFroggers()
  const frogger = froggers[ctx.update.message.from.id]
  if (frogger) {
    ctx.reply(`${frogger.username} SENT ${frogger.frogsCount}🐸!`)
  } else {
    ctx.reply(`${ctx.update.message.from.username} SENT NO 🐸(((((((((`)
  }
})

bot.command('coolest', async (ctx) => {
  await comboBreaker(ctx)
  const froggers = await repo.getFroggers()
  const coolest = Object.values(froggers).reduce((max, f) => f.frogsCount > max.frogsCount ? f : max)
  ctx.reply(`COOLEST ZHABA IN THE JUNGLE: ${coolest.username}`)
})

bot.command('record', async (ctx) => {
  await comboBreaker(ctx)
  const record = await repo.getRecord()
  ctx.reply(`GREATEST FROGS COMBO LENGTH: ${record}🐸`)
})

bot.command('sendnudes', async (ctx) => {
  await comboBreaker(ctx)
  ctx.replyWithPhoto('https://64.media.tumblr.com/4f4ffbf012cad24b336b7d206c4cafcb/tumblr_nobmgarutU1uvuwdlo1_250.jpg')
})

bot.command('kwa', async (ctx) => {
  await comboBreaker(ctx)
  ctx.reply('KWWAAAAAAAAA!!!')
})

bot.command('drop_database', async (ctx) => {
  await comboBreaker(ctx, false)
  const random = randomIntFromInterval(0, 100 - combo)
  if (random === 0) {
    await repo.drop()
    ctx.reply('Done')
  } else {
    ctx.reply('No')
  }
})


bot.guard((update) => frogStickers.includes(update.message?.sticker?.file_unique_id), async (ctx) => {
  const {id, username} = ctx.update.message.from
  const froggers = await repo.getFroggers()
  if (froggers[id]) {
    await repo.incrementFrogsCount(id)
  } else {
    await repo.newFrogger(id, username, 1)
  }
  combo++
})

bot.guard((update) => !frogStickers.includes(update?.message?.sticker?.file_unique_id), async (ctx) => {
  console.log(ctx.update)
  await comboBreaker(ctx)
})

process.once('SIGINT', () => bot.stop('SIGINT'))
process.once('SIGTERM', () => bot.stop('SIGTERM'))

bot.launch()
