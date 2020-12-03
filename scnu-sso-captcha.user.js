// ==UserScript==
// @name        SCNU SSO auto captcha filler
// @name:zh-CN  SCNU SSO 验证码自动填充
// @namespace   https://github.com/fengkx/
// @match       https://sso.scnu.edu.cn/AccountService/openapi/login.html*
// @match       https://sso.scnu.edu.cn/AccountService/user/login.html
// @grant       none
// @version     1.0
// @author      fengkx
// @description 12/3/2020, 10:42:17 AM
// @supportURL https://github.com/fengkx/scnu-sso-captcha
// @run-at document-end
// @require https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@2.7.0/dist/tf.min.js
// @require https://cdn.jsdelivr.net/npm/opencv.js@1.2.1/opencv.min.js
// ==/UserScript==

const WIDTH = 100
const IDICT = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
const HEIGHT = 50

const $input = document.getElementById('rancode')
const img = document.getElementById('codeimg')

const $canvas = document.createElement('canvas')
$canvas.addEventListener('click', window.reloadcode)
$canvas.width = WIDTH
$canvas.height = HEIGHT
const isUseLite = navigator.userAgent.indexOf('Firefox') >= 0
const modelDir = isUseLite ? 'js-model-lite-1': 'js-model-3'
const MODEL_URL = 'https://cdn.jsdelivr.net/gh/fengkx/scnu-sso-captcha@0.1.0/web-model/'+ modelDir +'/model.json'
console.debug(MODEL_URL)
async function main() {
  const $img = img.cloneNode()
    $img.width = WIDTH
    $img.height = HEIGHT

    const ctx = $canvas.getContext('2d')
    $canvas.classList.add('input-addon')
    $canvas.style.right = '100px'
    $input.parentElement.appendChild($canvas)
    ctx.drawImage($img, 0, 0)
    const imageData = ctx.getImageData(0,0,WIDTH, HEIGHT)
    const mat=cv.matFromImageData(imageData)
    let dst = new cv.Mat()
    let src = mat
    cv.cvtColor(src, src, cv.COLOR_BGR2GRAY, 0)
    cv.adaptiveThreshold(src, src, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 15, 15)
    cv.medianBlur(src,dst,3)
    cv.imshow($canvas, dst);
    x=tf.browser.fromPixels($canvas)
    x = x.div(255)
    q = x.max(2)
    x=x.max(2).expandDims(2)
    console.debug(x.shape)
    x = await x.array()
    let model;
    try {
        model = await tf.loadLayersModel('indexeddb://' + modelDir)
    } catch (e ) {
        model = await tf.loadLayersModel(MODEL_URL)
        const saveResults = await model.save('indexeddb://' + modelDir);
    }
    const old = Date.now()
    let p = model.predict(tf.tensor([x]))
    const used = (Date.now() - old) / 1000
    console.debug(used)
    p = await p.array()
    p = tf.tensor(p[0])
    p = p.argMax(1)
    p = await p.array()
    p = p.map(idx => IDICT[idx]).join('')
    console.log(p)
    $input.value = p
}
const docState = document.readyState
console.log(docState)
if(docState === 'complete') {
  main()
}
img.addEventListener('load', main)