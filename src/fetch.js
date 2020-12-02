const got = require('got');
const fs = require('fs');

function timeout(ms) {
	return new Promise(resolve => {
		setTimeout(resolve, ms)
	})
}

(async () => {
	for(let i=5000;i<6000;i++) {
		got.stream(`https://sso.scnu.edu.cn/AccountService/user/rancode.jpg?m=${Date.now()}`).pipe(fs.createWriteStream(`${__dirname}/dataset/codes/raw/${i}.jpg`))
		if(i%10==0)
			await timeout(200)
	}

})()
