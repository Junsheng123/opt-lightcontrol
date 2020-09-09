const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')
const { ipcMain } = require('electron')
const appRoot = require('electron-root-path').rootPath;
const isDev = require('electron-is-dev');
let tools = require('./assets/shared_tools');
let ws;
let mainWindow = null;
const taskkill = require('taskkill');
const find = require('find-process');

console.log('appRoot:', appRoot)
const curPath = path.join(appRoot, 'config.json')


function connect() {
  try {
    const WebSocket = require('ws');
    ws = new WebSocket('ws://127.0.0.1:8023');
  } catch (e) {
    console.log('Socket init error. Reconnect will be attempted in 1 second.', e.reason);
  }

  ws.on('open', () => {
    console.log('websocket in main connected')
    init_server();
  });

  ws.on('ping', () => {

    ws.send(tools.parseCmd('pong', 'from main'));
  })

  ws.on('message', (message) => {
    try {
      let msg = '';
      msg = tools.parseServerMessage(message);
      let cmd = msg.cmd;
      let data = msg.data;
      switch (cmd) {
        case 'ping':
          ws.send(tools.parseCmd('pong', data));
          break;
        case 'reply_init_ok':
          createWindow();
          break;
        case 'reply_image':
          mainWindow.webContents.send('reply_image', data)
          break;
        case 'reply_connect_controller':
          mainWindow.webContents.send('reply_connect_controller', data)
          break;
        case 'reply_read_all_intensity':
          mainWindow.webContents.send('reply_read_all_intensity', data)
          break;
        case 'reply_read_all_ch_state':
          mainWindow.webContents.send('reply_read_all_ch_state', data)
          break;
        case 'reply_loadSetting':
          mainWindow.webContents.send('reply_loadSetting', data)
          break;
        case 'reply_closed_all':
          console.log('reply_closed_all')
          app.quit();
          break;
        case 'reply_server_error':
          mainWindow.webContents.send('showMessage', data.error, 'Internal Error', 'danger')
          break;
        default:
          break;
      }
    } catch (e) {
      console.error(e)
      mainWindow.webContents.send('showMessage', e, 'Internal Error', 'danger')
    }
  });

  ws.onclose = function (e) {
    console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
    setTimeout(function () {
      connect();
    }, 5000);
  };

  ws.onerror = function (err) {
    console.error('Socket encountered error: ', err.message, 'Closing socket');
    ws.close();
  };
}

connect()

/*************************************************************
 * py process
 *************************************************************/

const PY_DIST_FOLDER = 'pyserver_dist'
const PY_FOLDER = 'public/server'
const PY_MODULE = 'api' // without .py suffix

let pyProc = null
let pyPort = null

//
const guessPackaged = () => {
  const fullPath = path.join(appRoot, PY_DIST_FOLDER)
  console.log('full server Path:')
  console.log(fullPath);
  console.log('does server existed:')
  console.log(require('fs').existsSync(fullPath))
  return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
  if (!guessPackaged()) {
    return path.join(appRoot, PY_FOLDER, PY_MODULE + '.py')
  }
  if (process.platform === 'win32') {
    return path.join(appRoot, PY_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
  }
  return path.join(appRoot, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
}

const selectPort = () => {
  pyPort = 4242
  return pyPort
}

const createPyProc = () => {
  let script = getScriptPath()
  let port = '' + selectPort()

  if (guessPackaged()) {
    pyProc = require('child_process').execFile(script, [port])
    console.log('Found server exe:')
    console.log(script);
  } else {
    pyProc = require('child_process').spawn('python', [script, port], { stdio: 'ignore' })
    // var batchFile = path.join(__dirname, PY_FOLDER,'start_python_server.bat')
    // var bat = shell.openItem(batchFile);
    // console.log(bat)
  }

  if (pyProc != null) {
    //console.log(pyProc)
    console.log('child process success on port ' + port);


  }
}

const exitPyProc = (e) => {
  console.log('before quit')
  e.preventDefault()
  find('name', 'api.exe', true)
    .then(function (list) {
      console.log('there are %s api.exe process(es)', list.length);
      const apiPids = list.map(elm => elm.pid)
      console.log('api.exe pid:', apiPids);
      if (apiPids.length > 0) {
        try {
          (async () => {
            await taskkill(apiPids, { force: true, tree: true });
            await ws.close()
            ws = null;
            app.exit(0)
          })();

        } catch (err) {
          ws.close()
          ws = null;
          app.exit(0)
        }
      } else {
        ws.close()
        ws = null;
        app.exit(0)
      }

    });
}

// init config and database
var init_server = function () {
  ws.send(tools.parseCmd('init_server', appRoot));
}

app.on('ready', createPyProc)
app.on('before-quit', exitPyProc)


/*************************************************************
 * window management
 *************************************************************/

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 1024,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  })
  mainWindow.loadURL(
    //  'http://localhost:3000' 
    isDev ? 'http://localhost:3000' : `file://${path.join(__dirname, "../build/index.html")}`
  )

  mainWindow.maximize();

  if (isDev) {
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.removeMenu();
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  })
  mainWindow.on('close', (e)=>{
    console.log('mainWindow closed');
    e.preventDefault();
    ws.send(tools.parseCmd('close'));
  })

}


app.on('window-all-closed', (e) => {
  console.log('window all closed')
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

/*************************************************************
 * iPC handler
 *************************************************************/

ipcMain.on('snap', (event) => {
  ws.send(tools.parseCmd('snap'));
})
ipcMain.on('grab', (event) => {
  ws.send(tools.parseCmd('grab'));
})
ipcMain.on('grabStop', (event) => {
  ws.send(tools.parseCmd('grabStop'));
})
ipcMain.on('connectController', (event, ip) => {
  ws.send(tools.parseCmd('connectController', ip));
})
ipcMain.on('change_intensity', (event, chId, newIntensity) => {
  ws.send(tools.parseCmd('change_intensity', { channelIndex: chId, intensity: newIntensity }));
})
ipcMain.on('enable_channel', (event, chId) => {
  ws.send(tools.parseCmd('enable_channel', { channelIndex: chId}));
})
ipcMain.on('saveSetting', (event) => {
  ws.send(tools.parseCmd('saveSetting', appRoot));
})
ipcMain.on('saveImage', (event) => {
  ws.send(tools.parseCmd('saveImage', appRoot));
})