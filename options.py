def mainframe_opts(parser):
  group = parser.add_argument_group('Mainframe')
  group.add_argument('--private', default=True,
        help='start in private mode without voice input')
  return group
