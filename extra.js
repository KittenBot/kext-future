{
  rgb2hex: (args) => {
    var R = args.R
    var G = args.G
    var B = args.B
    return "#" + (1 << 24 | R << 16 | G << 8 | B).toString(16).slice(1)
  },
  argsHook: {
    PATH: (args,gen)=>{
      let unicode = '';
      for (let i = 0; i < args.length; i++) {
        let code = args.charCodeAt(i)
        if (code >= 0x4e00 && code <= 0x9fa5) {
          unicode += "\\u" + code.toString(16);
        } else {
          unicode += args[i];
        }
      }
      return `'${unicode}'`
    }
  }
}