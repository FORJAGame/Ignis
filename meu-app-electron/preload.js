const { contextBridge, ipcRenderer } = require('electron')
 
contextBridge.exposeInMainWorld('electronAPI', {
  abrirJanela: (tipo) => ipcRenderer.send('abrir-janela', tipo),
  getDados: () => ipcRenderer.invoke('get-dados'),
  adicionarEquipe: (nome) => ipcRenderer.invoke('adicionar-equipe', nome),
  removerEquipe: (id) => ipcRenderer.invoke('remover-equipe', id),
  alterarPontos: (id, valor) => ipcRenderer.invoke('alterar-pontos', { id, valor }),
  adicionarMaldicao: (dados) => ipcRenderer.invoke('adicionar-maldicao', dados),
  removerMaldicao: (id) => ipcRenderer.invoke('remover-maldicao', id),
  cumprirMaldicao: (equipeId, maldicaoId) => ipcRenderer.invoke('cumprir-maldicao', { equipeId, maldicaoId }),
  onDadosAtualizados: (callback) => ipcRenderer.on('dados-atualizados', (event, dados) => callback(dados))
})
 