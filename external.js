function commprocess(msg, sensor) {
  if (msg.startsWith('@')){ // periodic echo
    const _tmp = msg.split(' ').slice(1).map(r => Number(r))
    sensor.button0 = Boolean(_tmp[0] & 0x1)
    sensor.button1 = Boolean(_tmp[0] & 0x2)
    sensor.button2 = Boolean(_tmp[0] & 0x3)
    sensor.gesture = _tmp[1]
    sensor.acc_x = _tmp[2]
    sensor.acc_y = _tmp[3]
    sensor.acc_z = _tmp[4];
    return true
  } else if (msg.startsWith('$')){ // req echo
  }
  return false
}

(function() {
  return {
    commprocess
  }
})()