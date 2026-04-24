const { app, BrowserWindow, ipcMain, Menu } = require('electron')
const path = require('path')
const fs = require('fs')

const DADOS_PATH = path.join(app.getPath('userData'), 'dados.json')

function carregarDados() {
  if (!fs.existsSync(DADOS_PATH)) {
    const inicial = { equipes: [], maldicoes: [] }
    fs.writeFileSync(DADOS_PATH, JSON.stringify(inicial, null, 2))
    return inicial
  }
  return JSON.parse(fs.readFileSync(DADOS_PATH, 'utf-8'))
}

function salvarDados(dados) {
  fs.writeFileSync(DADOS_PATH, JSON.stringify(dados, null, 2))
}

let adminWin = null
let publicoWin = null

function createMainWindow() {
  const win = new BrowserWindow({
    width: 500,
    height: 400,
    resizable: false,
    title: 'Game Jam',
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })
  win.loadFile('index.html')
}

function abrirAdmin() {
  if (adminWin) return adminWin.focus()
  adminWin = new BrowserWindow({
    width: 900,
    height: 700,
    title: 'Administrador',
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })
  adminWin.loadFile('admin.html')
  adminWin.on('closed', () => adminWin = null)
}

function abrirPublico() {
  if (publicoWin) return publicoWin.focus()
  publicoWin = new BrowserWindow({
    width: 900,
    height: 700,
    title: 'Painel Público',
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })
  publicoWin.loadFile('publico.html')
  publicoWin.on('closed', () => publicoWin = null)
}

// Notifica painel público sobre atualizações
function notificarPublico() {
  if (publicoWin) {
    publicoWin.webContents.send('dados-atualizados', carregarDados())
  }
}

// IPC handlers
ipcMain.on('abrir-janela', (event, tipo) => {
  if (tipo === 'admin') abrirAdmin()
  else abrirPublico()
})

ipcMain.handle('get-dados', () => carregarDados())

ipcMain.handle('adicionar-equipe', (event, nome) => {
  const dados = carregarDados()
  if (dados.equipes.find(e => e.nome === nome)) return { erro: 'Equipe já existe!' }
  dados.equipes.push({ id: Date.now(), nome, pontos: 0 })
  salvarDados(dados)
  notificarPublico()
  return dados
})

ipcMain.handle('remover-equipe', (event, id) => {
  const dados = carregarDados()
  dados.equipes = dados.equipes.filter(e => e.id !== id)
  salvarDados(dados)
  notificarPublico()
  return dados
})

ipcMain.handle('alterar-pontos', (event, { id, valor }) => {
  const dados = carregarDados()
  const equipe = dados.equipes.find(e => e.id === id)
  if (!equipe) return { erro: 'Equipe não encontrada' }
  equipe.pontos = Math.max(0, equipe.pontos + valor)
  salvarDados(dados)
  notificarPublico()
  return dados
})

ipcMain.handle('adicionar-maldicao', (event, { titulo, descricao, pontos }) => {
  const dados = carregarDados()
  dados.maldicoes.push({ id: Date.now(), titulo, descricao, pontos, ativa: true })
  salvarDados(dados)
  notificarPublico()
  return dados
})

ipcMain.handle('remover-maldicao', (event, id) => {
  const dados = carregarDados()
  dados.maldicoes = dados.maldicoes.filter(m => m.id !== id)
  salvarDados(dados)
  notificarPublico()
  return dados
})

ipcMain.handle('cumprir-maldicao', (event, { equipeId, maldicaoId }) => {
  const dados = carregarDados()
  const equipe = dados.equipes.find(e => e.id === equipeId)
  const maldicao = dados.maldicoes.find(m => m.id === maldicaoId)
  if (!equipe || !maldicao) return { erro: 'Não encontrado' }
  equipe.pontos += maldicao.pontos
  salvarDados(dados)
  notificarPublico()
  return dados
})

app.whenReady().then(createMainWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})