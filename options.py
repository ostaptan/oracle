def mainframe_opts(parser):
  group = parser.add_argument_group('Translation')
  group.add_argument('--private', default=False,
        help='start in private mode without voice input')
  return group
