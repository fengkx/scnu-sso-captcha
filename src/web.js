const fetch = require('node-fetch');
const Koa = require('koa');
const app = new Koa();
const Router = require('koa-router');
const koaBody = require('koa-body');
const fs = require('fs');
const {exec} = require('child_process');
const {join} = require('path');
app.use(koaBody())
const router = new Router();
router.get('/img/:id', async (ctx) => {
	const id = ctx.params.id;
	ctx.body = fs.createReadStream(`${__dirname}/dataset/codes/raw/${id}.jpg`);
})
router.post('/img', async (ctx) => {
	const {body} = ctx.request;
	const {id, code} = JSON.parse(body);
	if(code) {
		// fs.createReadStream(`${__dirname}/codes/raw/${id}.jpg`).pipe(fs.createWriteStream(`${__dirname}/codes/mark/${code}`))
		const command = `cp ${__dirname}/dataset/codes/raw/${id}.jpg ${__dirname}/dataset/codes/mark/${code}.jpeg`;
		console.log(command)
		exec(command)
	}
	ctx.body = 'ok'
})

router.get('/code/:id?', (ctx) => {
	ctx.type = 'text/html';
	ctx.body = fs.createReadStream(`${__dirname}/index.html`)
})


async function predict(id)  {
	const pic = `${__dirname}/dataset/codes/raw/${id}.jpg`;
	return new Promise((resolve, reject) => {
		exec(`python  ${join(__dirname, 'predict.py')} ${pic}`, (err, stdout) => {
			if(err) {
				reject(err)
			} else {
				resolve(stdout)
			}
		})
	})
}
router.post('/p/:id', async ctx => {
	const id = ctx.params.id;
	const data = JSON.parse(ctx.request.body).input
	const resp = await fetch(`http://localhost:8000/p/${id}?q=${JSON.stringify(data)}`, {
		method: 'GET',
	});
	const text = await resp.text();
	ctx.body = text.substring(1, text.length-1)
})

app
  .use(router.routes())
  .use(router.allowedMethods());
app.listen(3000)
