{
  rgb2hex: (args) => {
    var R = args.R
    var G = args.G
    var B = args.B
    return "#" + (1 << 24 | R << 16 | G << 8 | B).toString(16).slice(1)
  },
}